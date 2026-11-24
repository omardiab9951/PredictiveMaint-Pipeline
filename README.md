---
license: mit
pretty_name: Machine Degradation with Exact Remaining Useful Life
task_categories:
  - tabular-regression
  - tabular-classification
  - time-series-forecasting
tags:
  - predictive-maintenance
  - remaining-useful-life
  - rul
  - prognostics
  - run-to-failure
  - condition-monitoring
  - degradation
  - phm
  - synthetic
  - tabular
  - industrial
size_categories:
  - 10K<n<100K
configs:
  - config_name: readings
    data_files: readings.csv
    default: true
  - config_name: units
    data_files: units.csv
  - config_name: ground_truth
    data_files: ground_truth.csv
---

# Machine Degradation with Exact Remaining Useful Life

A synthetic run-to-failure dataset: 100 machines, each followed from install to
failure, 23,118 hourly readings in total. Every row carries the true remaining
useful life, because the failure time was declared before the data was generated
rather than annotated afterwards.

That last sentence is the whole point, so it is worth being precise about what
it buys you and what it does not.

## Why this exists

AI4I 2020, the most downloaded public predictive-maintenance dataset, has a
structural problem for prognostics work: it has no unit identity and no time
index. Each of its 10,000 rows is an independent snapshot of a different
product. There is no machine you can follow, so there is no trajectory, and
there is no remaining-useful-life label to predict. It is a very good
classification dataset wearing a prognostics costume.

NASA C-MAPSS has trajectories and RUL, and remains the standard, but it is a
turbofan simulation from 2008 with a fixed set of conditions you cannot change.
If you want a different fleet size, a different failure mix, or a different
noise level, you cannot have one.

This dataset is generated from a declaration, so you can have one. The
`schema.yaml` in this repo is the entire specification and it runs as-is.

## What is in it

| file | rows | what it is |
| --- | --- | --- |
| `readings.csv` | 23,118 | one row per machine per cycle, sensors plus labels |
| `units.csv` | 100 | one row per machine: its true life, failure mode, split |
| `ground_truth.csv` | 23,118 | the latent damage value behind each reading |

`readings.csv` columns:

- `unit_id`, `cycle`: which machine, and how many cycles since install
- `rul_cycles`: **remaining useful life**, exact, counting down to 0 at failure
- `machine_failure`: 1 on the final cycle of each unit
- `failure_mode`: `tool_wear`, `heat_dissipation`, `power`, `overstrain`
- `tool_wear_min`, `vibration_mm_s`, `torque_nm`, `process_temperature_k`,
  `air_temperature_k`, `rotational_speed_rpm`: the observable sensors
- `control_type`: the machine's quality grade
- `split`: `train` (80 units) or `test` (20 units), split by unit so no machine
  appears in both

`ground_truth.csv` gives the hidden damage state, which real telemetry never
has. It is there so you can check whether a model recovered the latent process
or only fitted the sensors.

## What holds, measured on these files

Every line below was computed from the CSVs in this repo, not asserted:

- **RUL is exact on all 100 units.** It decrements by exactly 1 each cycle and
  reaches 0 on the failure cycle. There is no smoothing and no clipping.
- **Tool wear never decreases: 100% of consecutive steps.** Material does not
  come back. In AI4I, noise alone makes wear fall about as often as it rises.
- **Wear correlates +0.849 with cycle.** Something is actually progressing
  toward failure.
- **Failure mode is learnable rather than decorative.** Units that fail by
  `tool_wear` reach a mean 357 minutes of wear against 245 to 261 for the other
  modes, and `heat_dissipation` units reach 325.6 K against about 316 K. The
  mode leaves a signature in the sensors, so predicting it from telemetry is a
  real task.
- **Sensors are correlated but not collinear: mean 0.62, max 0.83** across the
  four degradation-driven channels. Each unit draws its own susceptibility per
  sensor, so the fleet does not move as one body.
- Lives range from **128 to 358 cycles**, drawn per unit.

`INTEGRITY.txt` ships the same checks so you can re-run them.

## Honest limits

Read these before citing it.

- **The physics is not validated.** The damage law is a simplified lumped model.
  This has not been checked against XJTU-SY, PRONOSTIA/FEMTO or IMS run-to-failure
  data. The defensible claim is that the labels are exact and the trajectory is
  declared, not that the degradation is faithful to a specific bearing or spindle.
- **One damage process per unit.** Real machines fail from several interacting
  mechanisms. Here the failure mode shapes a single underlying process.
- **No per-machine attributes** beyond the control type. No location, no
  maintenance history, no operator.
- **Not a drop-in replacement for C-MAPSS** in published benchmarks. Use it for
  controlled experiments, for sanity-checking a pipeline, and for cases where you
  need ground truth that real data cannot give you.

## Make your own

```bash
pip install misata
misata generate --config schema.yaml --output-dir ./data
```

Change the fleet size, the mean life, the failure mix or the sensor response,
and regenerate. The RUL stays exact because it is solved for, not labelled.

```yaml
degradations:
  - table: readings
    units: 100
    life_mean: 220
    life_std: 45
    responses:
      - {column: tool_wear_min, baseline: 0, at_failure: 250, monotonic: true}
      - {column: vibration_mm_s, baseline: 0.8, at_failure: 5.2, shape: exponential}
```

## Provenance

Generated by [Misata](https://github.com/rasinmuhammed/misata) (MIT). No real
machine data was sampled and no model was fitted to real data, so this contains
no proprietary or personal information. Landing page with a trajectory chart:
[misata.studio/datasets/machine-degradation](https://www.misata.studio/datasets/machine-degradation).

## Citation

```bibtex
@misc{misata_machine_degradation_2026,
  title  = {Machine Degradation with Exact Remaining Useful Life},
  author = {Muhammed Rasin O M},
  year   = {2026},
  note   = {Synthetic run-to-failure dataset generated declaratively with Misata},
  url    = {https://huggingface.co/datasets/rasinmuhammed/predictive-maintenance-remaining-useful-life}
}
```
