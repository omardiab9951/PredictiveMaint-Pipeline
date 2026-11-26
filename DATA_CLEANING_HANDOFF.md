# Industrial Predictive Maintenance: Data Cleaning Handoff

**Stage:** Notebook 04, Data Cleaning & Reproducible Preparation
**Owner:** Member 2, Data Cleaning Lead
**Receiver:** Member 3
**Script:** `data_cleaning.py` (supersedes `04_Data_Cleaning.ipynb`)
**Status:** Complete. Last run: 0 warnings, all integrity checks passed.

---

## 1. Purpose

Create traceable, reproducible clean copies of the three Sprint 1 source tables while:

- preserving every machine-cycle record,
- never fabricating sensor measurements,
- recording every transformation and every check in a change log.

Raw files are treated as read-only. SHA-256 hashes are verified before and after each run.

---

## 2. Inputs and outputs

### Inputs (`data/raw/`)

| File | Rows | Columns |
|---|---|---|
| `readings.csv` | 23,118 | 13 |
| `units.csv` | 100 | 4 |
| `ground_truth.csv` | 23,118 | 3 |

### Outputs

| Path | Content |
|---|---|
| `data/clean/readings_clean.csv` | Cleaned readings (+ 2 flag columns) |
| `data/clean/units_clean.csv` | Units with normalised dtypes |
| `data/clean/ground_truth_clean.csv` | Ground truth with normalised dtypes |
| `logs/change_log.csv` | Every transformation and check (40 entries in the last run) |
| `logs/structural_audit.csv` | Structural-missingness audit per sensor |
| `logs/outlier_review.csv` | IQR review: global, per `control_type`, per life-position decile (tool wear) |
| `logs/run_manifest.json` | Seed, library versions, raw hashes, row counts, warnings |

---

## 3. How to run

```bash
python data_cleaning.py                                   # auto-detects data/raw or ../data/raw
python data_cleaning.py --raw-dir path/to/raw --clean-dir out/clean --log-dir out/logs
python data_cleaning.py --strict                          # abort on any data-quality warning
```

Requirements: Python 3, `pandas`, `numpy`. No installs happen inside the script.
Seed: `2026` (recorded in the manifest).

---

## 4. Cleaning policy

| # | Rule | Treatment |
|---|---|---|
| 1 | Structural missingness | **Preserved as NaN.** Control A: no vibration. Control B: no torque. Control C: no air temperature. No imputation. |
| 2 | Negative `tool_wear_min` | Physically invalid. Set to NaN, **row kept**, flagged in `tool_wear_invalid_negative`. |
| 3 | Non-monotonic tool wear | Per-unit check ordered by `cycle`. Violations flagged in `tool_wear_nonmonotonic`; values unchanged. |
| 4 | IQR outliers | **Retained.** Potential statistical outliers, not confirmed errors. |
| 5 | Duplicates | Checked on full rows and keys. Conflicting keys stop the run; exact duplicates would be dropped and logged. |
| 6 | Labels and metadata | RUL, failure labels, machine metadata and ground-truth damage untouched. |
| 7 | Data types | Keys and categoricals as `string`; counts, RUL and failure flag as `int64`; sensors and damage as `float64`. |

---

## 5. Results (last run on the real data)

| Check | Result |
|---|---|
| Row counts | 23,118 / 100 / 23,118, unchanged |
| Primary keys, foreign keys, cross-table alignment | Passed |
| Structural missingness | Exact match: 0 unexpected missing, 0 unexpectedly observed |
| Negative tool wear converted to NaN | 25 |
| Non-monotonic tool-wear rows flagged | 0 (monotonic in all 100 units) |
| Exact duplicates removed | 0 |
| Missing cells in readings | 23,118 → 23,143 (+25 from invalid wear) |
| IQR outliers retained (global) | 3,336 |
| Consistency checks | All passed |
| Raw file hashes before vs. after | Identical |

### Structural missingness

| Sensor | Missing | Control type |
|---|---|---|
| `vibration_mm_s` | 9,347 | A |
| `torque_nm` | 7,501 | B |
| `air_temperature_k` | 6,270 | C |

### Global IQR review (retained, unchanged)

| Sensor | Observed | Potential outliers | % |
|---|---|---|---|
| `tool_wear_min` | 23,093 | 33 | 0.143 |
| `vibration_mm_s` | 13,771 | 647 | 4.698 |
| `torque_nm` | 15,617 | 65 | 0.416 |
| `process_temperature_k` | 23,118 | 2,323 | 10.048 |
| `air_temperature_k` | 16,848 | 98 | 0.582 |
| `rotational_speed_rpm` | 23,118 | 170 | 0.735 |

Process temperature at about 10% flagged suggests distinct operating regimes rather than errors. Review the per-`control_type` rows in `outlier_review.csv` before any treatment.

---

## 6. Schema of `readings_clean.csv`

All original columns are unchanged except `tool_wear_min` (negatives → NaN). Two columns were added:

| Column | Type | Meaning |
|---|---|---|
| `tool_wear_invalid_negative` | int8 | 1 where the raw `tool_wear_min` was negative (25 rows) |
| `tool_wear_nonmonotonic` | int8 | 1 where wear fell below the unit's earlier running maximum (0 rows) |

---

## 7. Checks performed (all logged in `change_log.csv`)

- Required columns present in every table.
- Keys non-null and unique; foreign keys valid; readings and ground-truth machine-cycle keys match exactly.
- Structural missingness audit against the control-type design.
- Per-unit monotonicity of accumulated tool wear.
- `rul_cycles >= 0`, `machine_failure` in {0, 1}, `damage` finite, `life_cycles > 0`.
- Max observed cycle per unit does not exceed `life_cycles`.
- `split` consistent between `readings` and `units`.
- A unit's `failure_mode` in `units` appears among that unit's labels in `readings`.
- Every original column verified unchanged except `tool_wear_min`.
- `tool_wear_min` changed only where raw < 0, and only to NaN.
- Structural NaN mask identical to the raw data.
- Raw SHA-256 unchanged after the run.

---

## 8. Modelling notes for Member 3

1. **Structural NaNs are by design, not random failures.** Use control-aware modelling or explicit missingness indicators. Do not impute with global means or zeros.
2. **`tool_wear_min` NaNs are non-structural.** Identify them with `tool_wear_invalid_negative`.
3. **Leakage:** keep `failure_mode`, `machine_failure`, `life_cycles` and `damage` out of RUL input features.
4. **Splitting:** split by `unit_id`, never by random cycles, to avoid leakage across cycles of the same unit.
5. **Outliers:** treat them as potential extremes. Decide per sensor and per control type whether any treatment is warranted.

---

## 9. Handoff checklist

- [x] `readings_clean.csv`, `units_clean.csv`, `ground_truth_clean.csv` exist
- [x] Row counts and machine-cycle keys match the raw source
- [x] No negative observed `tool_wear_min` values remain
- [x] Structural missingness unchanged and documented
- [x] IQR outliers not deleted or clipped
- [x] RUL, failure labels, machine metadata and ground-truth damage preserved
- [x] `change_log.csv` records the cleaning decisions
- [x] Raw files verified unmodified
- [ ] Member 3 review of the clean outputs before model development

---

## 10. Repository notes

Commit the script, `change_log.csv`, `structural_audit.csv`, `outlier_review.csv` and `run_manifest.json`. Do **not** commit raw data to the cleaning branch unless the team policy changes.
