#!/usr/bin/env python3
"""
Industrial Predictive Maintenance
Notebook 04 -> script: Data Cleaning & Reproducible Preparation
================================================================

Creates traceable clean copies of readings / units / ground_truth while
preserving every machine-cycle record and never fabricating sensor values.

Cleaning policy
---------------
1. Structural missingness (control A -> no vibration, B -> no torque,
   C -> no air temperature) is PRESERVED as NaN. No imputation.
2. Negative `tool_wear_min` is physically invalid -> set to NaN, row kept.
   The conversion is recorded in an explicit flag column
   (`tool_wear_invalid_negative`) so downstream code can tell these NaNs
   (non-structural) apart from the structural ones.
3. Accumulated tool wear must be monotonic non-decreasing per unit. Violations
   are FLAGGED (`tool_wear_nonmonotonic`) and reported; values are not altered
   because no approved domain rule exists to repair them.
4. IQR outliers are RETAINED. They are reviewed per control_type (all sensors)
   and per life-position decile (tool wear), plus globally for comparison.
5. RUL, failure labels, machine metadata and ground-truth damage are untouched.
6. Raw files are read-only: SHA-256 hashes are verified before and after.

Outputs
-------
<clean_dir>/readings_clean.csv, units_clean.csv, ground_truth_clean.csv
<log_dir>/change_log.csv        every transformation AND every check
<log_dir>/structural_audit.csv  structural-missingness audit
<log_dir>/outlier_review.csv    IQR review (global / control_type / life decile)
<log_dir>/run_manifest.json     seed, versions, input hashes, row counts

Usage
-----
python data_cleaning.py                       # auto-detect data/raw or ../data/raw
python data_cleaning.py --raw-dir path/to/raw --clean-dir out/clean --log-dir out/logs
python data_cleaning.py --strict              # data-quality warnings abort the run
"""

from __future__ import annotations

import argparse
import hashlib
import json
import platform
import sys
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
import pandas as pd

# --------------------------------------------------------------------------- #
# Constants
# --------------------------------------------------------------------------- #
RANDOM_SEED = 2026

SENSOR_COLUMNS = [
    "tool_wear_min", "vibration_mm_s", "torque_nm",
    "process_temperature_k", "air_temperature_k", "rotational_speed_rpm",
]

STRUCTURAL_MISSING_MAP = {          # sensor -> control_type that never acquires it
    "vibration_mm_s": "A",
    "torque_nm": "B",
    "air_temperature_k": "C",
}

REQUIRED_COLUMNS = {
    "readings": {
        "unit_id", "cycle", "rul_cycles", "machine_failure", "failure_mode",
        "tool_wear_min", "vibration_mm_s", "torque_nm",
        "process_temperature_k", "air_temperature_k",
        "rotational_speed_rpm", "control_type", "split",
    },
    "units": {"unit_id", "life_cycles", "split", "failure_mode"},
    "ground_truth": {"unit_id", "cycle", "damage"},
}

KEYS = {
    "readings": ["unit_id", "cycle"],
    "units": ["unit_id"],
    "ground_truth": ["unit_id", "cycle"],
}

FLAG_INVALID = "tool_wear_invalid_negative"
FLAG_NONMONO = "tool_wear_nonmonotonic"


# --------------------------------------------------------------------------- #
# Change log (records transformations AND checks)
# --------------------------------------------------------------------------- #
class ChangeLog:
    COLUMNS = [
        "timestamp_utc", "step", "table", "column", "operation",
        "affected_rows", "status", "reason", "method",
    ]

    def __init__(self) -> None:
        self.entries: list[dict] = []
        self.warnings: list[str] = []

    def add(self, step, table, column, operation, affected_rows, reason, method,
            status="applied") -> None:
        self.entries.append({
            "timestamp_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
            "step": step,
            "table": table,
            "column": column,
            "operation": operation,
            "affected_rows": int(affected_rows),
            "status": status,
            "reason": reason,
            "method": method,
        })

    def warn(self, step, table, column, operation, affected_rows, reason, method) -> None:
        msg = f"[{step}] {table}.{column}: {operation} ({int(affected_rows)} rows) - {reason}"
        self.warnings.append(msg)
        print("WARNING:", msg)
        self.add(step, table, column, operation, affected_rows, reason, method, status="warning")

    def frame(self) -> pd.DataFrame:
        return pd.DataFrame(self.entries, columns=self.COLUMNS)


def banner(title: str) -> None:
    print(f"\n{'=' * 78}\n{title}\n{'=' * 78}")


# --------------------------------------------------------------------------- #
# Paths and hashing
# --------------------------------------------------------------------------- #
def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def resolve_dirs(args: argparse.Namespace) -> tuple[Path, Path, Path]:
    here = Path(__file__).resolve().parent
    if args.raw_dir:
        raw = Path(args.raw_dir)
    else:
        candidates = [Path("data/raw"), Path("../data/raw"),
                      here / "data/raw", here.parent / "data/raw"]
        raw = next((p for p in candidates if p.is_dir()), None)
        if raw is None:
            raise FileNotFoundError(
                "Could not find data/raw. Pass --raw-dir or place readings.csv, "
                "units.csv and ground_truth.csv in data/raw/."
            )
    raw = raw.resolve()
    clean = Path(args.clean_dir).resolve() if args.clean_dir else raw.parent / "clean"
    logs = Path(args.log_dir).resolve() if args.log_dir else raw.parent.parent / "logs"
    if clean == raw:
        raise ValueError("clean_dir must differ from raw_dir; raw data is read-only.")
    return raw, clean, logs


# --------------------------------------------------------------------------- #
# Steps
# --------------------------------------------------------------------------- #
def load_raw(raw_dir: Path):
    files = {n: raw_dir / f"{n}.csv" for n in ("readings", "units", "ground_truth")}
    missing = [str(p) for p in files.values() if not p.is_file()]
    if missing:
        raise FileNotFoundError(f"Missing raw files: {missing}")
    hashes = {n: sha256(p) for n, p in files.items()}
    frames = {n: pd.read_csv(p) for n, p in files.items()}
    return frames, hashes, files


def validate_schema(frames: dict, log: ChangeLog) -> None:
    for name, required in REQUIRED_COLUMNS.items():
        absent = required - set(frames[name].columns)
        if absent:
            raise ValueError(f"{name} is missing required columns: {sorted(absent)}")
        log.add("schema", name, "*", "schema_check", len(frames[name]),
                "Required columns present.", "Set difference against documented schema.",
                status="passed")
    print("Schema check passed.")


def baseline_report(frames: dict, log: ChangeLog) -> None:
    rows = []
    for name, df in frames.items():
        rows.append({
            "table": name, "rows": len(df), "columns": df.shape[1],
            "complete_duplicate_rows": int(df.duplicated().sum()),
            "missing_cells": int(df.isna().sum().sum()),
        })
        log.add("baseline", name, "*", "baseline_profile", len(df),
                f"cols={df.shape[1]}, exact_duplicates={int(df.duplicated().sum())}, "
                f"missing_cells={int(df.isna().sum().sum())}",
                "pandas profile of raw table.", status="info")
    print(pd.DataFrame(rows).to_string(index=False))
    print("\nMissing counts, sensor columns:")
    print(frames["readings"][SENSOR_COLUMNS].isna().sum().rename("missing_count").to_string())


def validate_keys(frames: dict, log: ChangeLog) -> None:
    for name, keys in KEYS.items():
        df = frames[name]
        if df[keys].isna().any().any():
            raise ValueError(f"{name}: missing values in key columns {keys}.")
        n_dup = int(df.duplicated(keys).sum())
        if n_dup:
            raise ValueError(f"{name}: {n_dup} duplicate key rows {keys}; resolve explicitly.")
        log.add("keys", name, ",".join(keys), "primary_key_check", len(df),
                "Keys non-null and unique.", "isna / duplicated on key columns.",
                status="passed")

    known = set(frames["units"]["unit_id"])
    for name in ("readings", "ground_truth"):
        unknown = set(frames[name]["unit_id"]) - known
        if unknown:
            raise ValueError(f"{name}: unit_id not in units: {sorted(unknown)[:5]} ...")
        log.add("keys", name, "unit_id", "foreign_key_check", len(frames[name]),
                "All unit_id exist in units.", "Set inclusion.", status="passed")

    rk = pd.MultiIndex.from_frame(frames["readings"][KEYS["readings"]])
    gk = pd.MultiIndex.from_frame(frames["ground_truth"][KEYS["ground_truth"]])
    if not (rk.isin(gk).all() and gk.isin(rk).all()):
        raise ValueError("readings and ground_truth machine-cycle keys do not match exactly.")
    log.add("keys", "readings|ground_truth", "unit_id,cycle", "key_alignment_check",
            len(rk), "Machine-cycle keys match exactly across tables.",
            "MultiIndex bidirectional inclusion.", status="passed")
    print("Primary keys, foreign keys and cross-table alignment passed.")


def audit_structural_missingness(readings: pd.DataFrame, log: ChangeLog,
                                 strict: bool) -> pd.DataFrame:
    rows = []
    for sensor, ctrl in STRUCTURAL_MISSING_MAP.items():
        miss = readings[sensor].isna()
        exp = readings["control_type"].eq(ctrl)
        row = {
            "sensor": sensor,
            "expected_control_type": ctrl,
            "total_missing": int(miss.sum()),
            "expected_structural_missing": int((miss & exp).sum()),
            "unexpected_missing": int((miss & ~exp).sum()),
            "unexpectedly_observed_in_control": int((~miss & exp).sum()),
        }
        rows.append(row)
        log.add("structural", "readings", sensor, "preserved_structural_missingness",
                row["total_missing"],
                f"Sensor not acquired for control_type {ctrl}; NaN is not zero.",
                "Retained as NaN; no imputation.", status="preserved")
        if row["unexpected_missing"] or row["unexpectedly_observed_in_control"]:
            log.warn("structural", "readings", sensor, "structural_pattern_deviation",
                     row["unexpected_missing"] + row["unexpectedly_observed_in_control"],
                     "Deviation from Sprint 1 acquisition design.",
                     "Cross-tab of NaN mask vs control_type.")
    audit = pd.DataFrame(rows)
    print(audit.to_string(index=False))
    if audit[["unexpected_missing", "unexpectedly_observed_in_control"]].any().any():
        if strict:
            raise ValueError("Structural missingness deviates from Sprint 1 pattern (--strict).")
    else:
        print("Structural missingness pattern matches the Sprint 1 handoff.")
    return audit


def fix_negative_tool_wear(readings: pd.DataFrame, log: ChangeLog) -> int:
    mask = readings["tool_wear_min"].lt(0)
    n = int(mask.sum())
    readings[FLAG_INVALID] = mask.astype("int8")
    if n:
        readings.loc[mask, "tool_wear_min"] = np.nan
    log.add("tool_wear", "readings", "tool_wear_min", "invalid_negative_to_missing", n,
            "Negative accumulated tool wear is physically invalid (baseline 0, "
            "monotonic accumulation).",
            "Set values < 0 to NaN; rows retained; no interpolation.")
    log.add("tool_wear", "readings", FLAG_INVALID, "flag_column_added", len(readings),
            "Separates non-structural NaNs (invalid wear) from structural NaNs.",
            "int8 indicator: 1 where raw tool_wear_min < 0.")
    print(f"Negative tool-wear values converted to NaN: {n}")
    return n


def flag_nonmonotonic_tool_wear(readings: pd.DataFrame, log: ChangeLog,
                                strict: bool) -> int:
    """Flag rows whose wear is below the running maximum of earlier cycles of the
    same unit. Values are not modified."""
    view = readings[["unit_id", "cycle", "tool_wear_min"]].sort_values(["unit_id", "cycle"])
    running_prev_max = view.groupby("unit_id", sort=False)["tool_wear_min"].transform(
        lambda s: s.cummax().ffill().shift()
    )
    violation = (view["tool_wear_min"] < running_prev_max)
    flags = violation.reindex(readings.index).fillna(False)
    readings[FLAG_NONMONO] = flags.astype("int8")

    n = int(flags.sum())
    units_affected = int(readings.loc[flags, "unit_id"].nunique()) if n else 0
    log.add("tool_wear", "readings", FLAG_NONMONO, "monotonicity_flag_added", n,
            f"Wear below earlier running max within unit; {units_affected} unit(s) affected.",
            "Per-unit cummax (NaN-aware) comparison, ordered by cycle; values unchanged.",
            status="flagged")
    if n:
        log.warn("tool_wear", "readings", "tool_wear_min", "monotonicity_violations", n,
                 f"{units_affected} unit(s) show decreasing accumulated wear.",
                 "Flagged only; no repair rule approved.")
        if strict:
            raise ValueError("Tool wear monotonicity violated (--strict).")
    else:
        print("Tool wear is monotonic non-decreasing within every unit.")
    return n


def handle_duplicates(frames: dict, log: ChangeLog) -> dict[str, int]:
    removed = {}
    for name, df in frames.items():
        n_key = int(df.duplicated(KEYS[name]).sum())
        if n_key:
            raise ValueError(f"{name}: {n_key} duplicate key rows; automatic deletion unsafe.")
        n_exact = int(df.duplicated().sum())
        removed[name] = n_exact
        if n_exact:
            df.drop_duplicates(inplace=True)
            log.add("duplicates", name, "*", "removed_exact_duplicate_rows", n_exact,
                    "Exact full-row duplicates add no observations.",
                    "drop_duplicates; key uniqueness revalidated.")
        else:
            log.add("duplicates", name, "*", "duplicate_check", 0,
                    "No exact duplicate rows or duplicate keys.",
                    "DataFrame.duplicated on full row and key.", status="passed")
            print(f"{name}: no duplicates; nothing removed.")
    return removed


def _cast_int(df: pd.DataFrame, col: str, table: str) -> None:
    numeric = pd.to_numeric(df[col], errors="raise")
    if numeric.isna().any():
        raise ValueError(f"{table}.{col} unexpectedly contains missing values.")
    if not np.all(np.equal(numeric, np.floor(numeric))):
        raise ValueError(f"{table}.{col} contains non-integer values.")
    df[col] = numeric.astype("int64")


def normalize_dtypes(readings, units, ground_truth, log: ChangeLog) -> None:
    for col in ("cycle", "rul_cycles", "machine_failure"):
        _cast_int(readings, col, "readings")
    _cast_int(units, "life_cycles", "units")
    _cast_int(ground_truth, "cycle", "ground_truth")

    for col in SENSOR_COLUMNS:
        readings[col] = pd.to_numeric(readings[col], errors="raise").astype("float64")
    ground_truth["damage"] = pd.to_numeric(ground_truth["damage"], errors="raise").astype("float64")

    for df in (readings, units, ground_truth):
        df["unit_id"] = df["unit_id"].astype("string")
    for df, cols in ((readings, ["failure_mode", "control_type", "split"]),
                     (units, ["failure_mode", "split"])):
        for col in cols:
            df[col] = df[col].astype("string")

    log.add("dtypes", "readings", "cycle,rul_cycles,machine_failure", "cast_int64",
            len(readings), "Integer fields validated (no NaN, no fractions).",
            "to_numeric + integrality check.")
    log.add("dtypes", "readings", ",".join(SENSOR_COLUMNS), "cast_float64", len(readings),
            "Sensor measurements normalised to float64.", "to_numeric(errors='raise').")
    log.add("dtypes", "units", "life_cycles", "cast_int64", len(units),
            "Integer field validated.", "to_numeric + integrality check.")
    log.add("dtypes", "ground_truth", "cycle,damage", "cast_int64_float64", len(ground_truth),
            "Key and damage dtypes normalised.", "to_numeric(errors='raise').")
    log.add("dtypes", "*", "unit_id + categoricals", "cast_string", 0,
            "Keys and categorical labels stored as pandas string dtype; labels unchanged.",
            "astype('string').")
    print("Data types normalized.")
    print(readings.dtypes.astype(str).rename("dtype").to_string())


def consistency_checks(readings, units, ground_truth, log: ChangeLog, strict: bool) -> None:
    """Additional semantic checks. Findings are logged as warnings (abort with --strict)."""
    def check(ok_count, total, table, column, operation, reason, method):
        bad = total - ok_count
        if bad:
            log.warn("consistency", table, column, operation, bad, reason, method)
            if strict:
                raise ValueError(f"{table}.{column}: {operation} ({bad} rows) [--strict]")
        else:
            log.add("consistency", table, column, operation, 0, reason, method, status="passed")

    check(int(readings["rul_cycles"].ge(0).sum()), len(readings), "readings", "rul_cycles",
          "rul_nonnegative_check", "RUL must be >= 0.", "rul_cycles >= 0")
    check(int(readings["machine_failure"].isin([0, 1]).sum()), len(readings), "readings",
          "machine_failure", "binary_label_check", "Failure flag must be 0/1.", "isin([0,1])")
    check(int(np.isfinite(ground_truth["damage"]).sum()), len(ground_truth), "ground_truth",
          "damage", "finite_damage_check", "Damage must be finite.", "np.isfinite")
    check(int(units["life_cycles"].gt(0).sum()), len(units), "units", "life_cycles",
          "positive_life_check", "Lifetime must be > 0.", "life_cycles > 0")

    per_unit = readings.groupby("unit_id")["cycle"].max()
    life = units.set_index("unit_id")["life_cycles"].reindex(per_unit.index)
    check(int((per_unit <= life).sum()), len(per_unit), "readings|units", "cycle,life_cycles",
          "cycle_within_life_check", "Max observed cycle should not exceed unit lifetime.",
          "groupby max(cycle) <= life_cycles")

    u = units.set_index("unit_id")
    r_first = readings.drop_duplicates("unit_id").set_index("unit_id")
    check(int((r_first["split"].reindex(u.index) == u["split"]).sum()), len(u),
          "readings|units", "split", "split_consistency_check",
          "Unit split must match between tables.", "Per-unit equality.")
    # readings.failure_mode may be a row-level label (e.g. "none" until the failure
    # cycle), so compare against ALL labels the unit has in readings, not the first row.
    modes_by_unit = readings.groupby("unit_id")["failure_mode"].agg(lambda s: set(s.dropna()))
    ok_mode = sum(
        1 for uid, mode in u["failure_mode"].items()
        if mode in modes_by_unit.get(uid, set())
    )
    check(ok_mode, len(u), "readings|units", "failure_mode", "failure_mode_consistency_check",
          "Unit failure mode (units) must appear among that unit's labels in readings.",
          "Per-unit membership of units.failure_mode in set(readings.failure_mode).")
    print("Consistency checks complete.")


def _iqr_stats(values: pd.Series) -> dict | None:
    v = values.dropna()
    if v.empty:
        return None
    q1, q3 = v.quantile(0.25), v.quantile(0.75)
    iqr = q3 - q1
    lo, hi = q1 - 1.5 * iqr, q3 + 1.5 * iqr
    n_out = int(((v < lo) | (v > hi)).sum())
    return {
        "observed_values": int(len(v)),
        "lower_iqr_bound": float(lo), "upper_iqr_bound": float(hi),
        "potential_outliers": n_out,
        "outlier_percentage": 100.0 * n_out / len(v),
    }


def review_outliers(readings: pd.DataFrame, units: pd.DataFrame, log: ChangeLog) -> pd.DataFrame:
    """IQR review only. Nothing is clipped, removed or replaced."""
    rows = []

    def add(scope, sensor, series):
        s = _iqr_stats(series)
        if s:
            rows.append({"scope": scope, "sensor": sensor, **s})

    for sensor in SENSOR_COLUMNS:
        add("global", sensor, readings[sensor])

    for sensor in SENSOR_COLUMNS:
        for ctrl, grp in readings.groupby("control_type", observed=True):
            add(f"control_type={ctrl}", sensor, grp[sensor])

    # Tool wear accumulates with age, so compare within life-position deciles.
    life = readings["unit_id"].map(units.set_index("unit_id")["life_cycles"])
    pos = (readings["cycle"] / life.where(life > 0)).clip(0, 1)
    decile = pd.cut(pos, bins=np.linspace(0, 1, 11), include_lowest=True)
    for dec, idx in readings.groupby(decile, observed=True).groups.items():
        add(f"life_decile={dec}", "tool_wear_min", readings.loc[idx, "tool_wear_min"])

    summary = pd.DataFrame(rows)
    log.add("outliers", "readings", ",".join(SENSOR_COLUMNS), "iqr_review_only",
            int(summary.loc[summary["scope"] == "global", "potential_outliers"].sum()),
            "Potential statistical outliers, not confirmed errors; retained unchanged.",
            "1.5*IQR global, per control_type, and per life-position decile (tool wear).",
            status="reviewed")
    print(summary[summary["scope"] == "global"].round(3).to_string(index=False))
    print("Outliers retained unchanged; see outlier_review.csv for grouped views.")
    return summary


def assert_columns_preserved(clean: pd.DataFrame, raw: pd.DataFrame, name: str,
                             exceptions: tuple[str, ...] = ()) -> None:
    raw_aligned = raw.loc[clean.index]
    for col in raw.columns:
        if col in exceptions:
            continue
        a, b = clean[col], raw_aligned[col]
        if pd.api.types.is_numeric_dtype(b):
            same = np.array_equal(a.to_numpy(dtype="float64", na_value=np.nan),
                                  b.to_numpy(dtype="float64"), equal_nan=True)
        else:
            same = a.astype("string").equals(b.astype("string"))
        if not same:
            raise AssertionError(f"{name}.{col} changed unexpectedly.")


def final_integrity_checks(readings, units, ground_truth, raw: dict, removed: dict,
                           negative_count: int, log: ChangeLog) -> None:
    exp_rows = {n: len(raw[n]) - removed[n] for n in raw}
    for name, df in (("readings", readings), ("units", units), ("ground_truth", ground_truth)):
        assert len(df) == exp_rows[name], f"{name} row count changed unexpectedly."

    assert units["unit_id"].is_unique
    assert not readings.duplicated(KEYS["readings"]).any()
    assert not ground_truth.duplicated(KEYS["ground_truth"]).any()

    # Every original column preserved, except tool_wear_min (checked below).
    assert_columns_preserved(readings, raw["readings"], "readings", exceptions=("tool_wear_min",))
    assert_columns_preserved(units, raw["units"], "units")
    assert_columns_preserved(ground_truth, raw["ground_truth"], "ground_truth")

    # tool_wear_min: only negatives may differ, and only by becoming NaN.
    rw = raw["readings"].loc[readings.index, "tool_wear_min"].astype("float64")
    cw = readings["tool_wear_min"]
    changed = ~((rw == cw) | (rw.isna() & cw.isna()))
    assert changed.sum() == negative_count, "Unexpected number of tool_wear_min changes."
    assert (rw[changed] < 0).all() and cw[changed].isna().all(), \
        "tool_wear_min changed other than negative -> NaN."
    assert not cw.dropna().lt(0).any(), "Negative observed tool wear remains."
    assert int(readings[FLAG_INVALID].sum()) == negative_count, "Invalid flag count mismatch."

    # Structural missingness must be exactly what the raw data had.
    for sensor in STRUCTURAL_MISSING_MAP:
        raw_mask = raw["readings"].loc[readings.index, sensor].isna().to_numpy()
        assert np.array_equal(readings[sensor].isna().to_numpy(), raw_mask), \
            f"Structural missingness changed in {sensor}."

    log.add("final", "*", "*", "final_integrity_checks", 0,
            "Row counts, keys, labels, metadata, ground truth, structural NaNs, and "
            "tool-wear-only-negative-to-NaN invariants verified.",
            "Assertions against raw copies.", status="passed")
    print("All final integrity checks passed.")


def save_outputs(clean_dir: Path, log_dir: Path, readings, units, ground_truth,
                 log: ChangeLog, structural_audit, outlier_summary) -> list[Path]:
    clean_dir.mkdir(parents=True, exist_ok=True)
    log_dir.mkdir(parents=True, exist_ok=True)
    paths = {
        clean_dir / "readings_clean.csv": readings,
        clean_dir / "units_clean.csv": units,
        clean_dir / "ground_truth_clean.csv": ground_truth,
        log_dir / "structural_audit.csv": structural_audit,
        log_dir / "outlier_review.csv": outlier_summary,
    }
    for path, df in paths.items():
        df.to_csv(path, index=False)
    log.add("save", "*", "*", "outputs_written", len(paths),
            "Clean tables and review reports written to clean_dir / log_dir.",
            "DataFrame.to_csv(index=False).")
    log_path = log_dir / "change_log.csv"
    log.frame().to_csv(log_path, index=False)
    return list(paths) + [log_path]


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--raw-dir", help="Folder with readings.csv, units.csv, ground_truth.csv")
    parser.add_argument("--clean-dir", help="Output folder for clean CSVs (default: <raw>/../clean)")
    parser.add_argument("--log-dir", help="Output folder for logs (default: <raw>/../../logs)")
    parser.add_argument("--seed", type=int, default=RANDOM_SEED)
    parser.add_argument("--strict", action="store_true",
                        help="Abort on any data-quality warning")
    args = parser.parse_args()

    np.random.seed(args.seed)
    log = ChangeLog()

    banner("1. Locate and load immutable raw data")
    raw_dir, clean_dir, log_dir = resolve_dirs(args)
    print(f"raw  : {raw_dir}\nclean: {clean_dir}\nlogs : {log_dir}")
    raw, hashes_before, raw_files = load_raw(raw_dir)
    readings = raw["readings"].copy(deep=True)
    units = raw["units"].copy(deep=True)
    ground_truth = raw["ground_truth"].copy(deep=True)
    for n, df in raw.items():
        log.add("load", n, "*", "raw_loaded", len(df),
                f"sha256={hashes_before[n][:16]}...", "pandas.read_csv; working on deep copy.",
                status="info")

    banner("2. Schema and baseline")
    validate_schema(raw, log)
    baseline_report(raw, log)

    banner("3. Key validation")
    validate_keys(raw, log)

    banner("4. Structural missingness (preserved)")
    structural_audit = audit_structural_missingness(readings, log, args.strict)

    banner("5. Invalid negative tool wear")
    negative_count = fix_negative_tool_wear(readings, log)

    banner("6. Tool wear monotonicity")
    flag_nonmonotonic_tool_wear(readings, log, args.strict)

    banner("7. Duplicates")
    removed = handle_duplicates(
        {"readings": readings, "units": units, "ground_truth": ground_truth}, log)

    banner("8. Data type normalisation")
    normalize_dtypes(readings, units, ground_truth, log)

    banner("9. Consistency checks")
    consistency_checks(readings, units, ground_truth, log, args.strict)

    banner("10. Outlier review (retain only)")
    outlier_summary = review_outliers(readings, units, log)

    banner("11. Final integrity checks")
    final_integrity_checks(readings, units, ground_truth, raw, removed, negative_count, log)

    banner("12. Save outputs")
    # Raw must be byte-identical after the run.
    hashes_after = {n: sha256(p) for n, p in raw_files.items()}
    assert hashes_after == hashes_before, "Raw files were modified during the run!"
    log.add("final", "*", "*", "raw_immutability_check", 0,
            "Raw file SHA-256 identical before and after run.", "hashlib.sha256.",
            status="passed")
    written = save_outputs(clean_dir, log_dir, readings, units, ground_truth,
                           log, structural_audit, outlier_summary)

    manifest = {
        "run_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "seed": args.seed,
        "strict": args.strict,
        "python": platform.python_version(),
        "pandas": pd.__version__,
        "numpy": np.__version__,
        "raw_sha256": hashes_after,
        "rows_raw": {n: len(df) for n, df in raw.items()},
        "rows_clean": {"readings": len(readings), "units": len(units),
                       "ground_truth": len(ground_truth)},
        "negative_tool_wear_to_nan": negative_count,
        "nonmonotonic_tool_wear_flagged": int(readings[FLAG_NONMONO].sum()),
        "warnings": log.warnings,
    }
    manifest_path = log_dir / "run_manifest.json"
    manifest_path.write_text(json.dumps(manifest, indent=2))
    written.append(manifest_path)
    print("Saved:")
    for p in written:
        print("-", p)

    banner("13. Before/after summary and handoff")
    summary = pd.DataFrame([
        {"table": n,
         "raw_rows": len(raw[n]),
         "clean_rows": len(df),
         "raw_missing_cells": int(raw[n].isna().sum().sum()),
         "clean_missing_cells": int(df.isna().sum().sum())}
        for n, df in (("readings", readings), ("units", units), ("ground_truth", ground_truth))
    ])
    print(summary.to_string(index=False))
    print(f"\nInvalid negative tool-wear values converted : {negative_count}")
    print(f"Non-monotonic tool-wear rows flagged        : {int(readings[FLAG_NONMONO].sum())}")
    print(f"Potential IQR outliers retained (global)    : "
          f"{int(outlier_summary.loc[outlier_summary['scope'] == 'global', 'potential_outliers'].sum())}")
    print(f"Logged entries                              : {len(log.entries)}")
    print(f"Warnings                                    : {len(log.warnings)}")
    print("Structural sensor missing values intentionally retained.")

    print("""
Handoff notes for modelling
---------------------------
* Structural NaNs (vibration/torque/air temperature) reflect acquisition design by
  control_type; model them control-aware or with explicit missingness indicators.
* tool_wear_min NaNs are NON-structural: use `tool_wear_invalid_negative` to identify them.
* `tool_wear_nonmonotonic` marks rows whose wear decreased within a unit; values unchanged.
* Keep failure_mode, machine_failure, life_cycles and damage out of RUL input features
  (target / post-failure leakage). Prefer unit-level splits to avoid leakage across cycles.
""")
    return 0


if __name__ == "__main__":
    sys.exit(main())