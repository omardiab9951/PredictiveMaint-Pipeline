# Data Quality Problem List

**Project:** Industrial Predictive Maintenance  
**Sprint:** 1 — Ingestion & EDA  
**Dataset:** [Machine Degradation (Hugging Face)](https://huggingface.co/datasets/rasinmuhammed/predictive-maintenance-remaining-useful-life)

## 1. Identified Data Quality Issues

| ID | Table | Column | Issue | Affected values | Percentage |
|---|---|---|---|---:|---:|
| P01 | readings | vibration_mm_s | Missing measurements | 9,347 | 40.43% |
| P02 | readings | torque_nm | Missing measurements | 7,501 | 32.45% |
| P03 | readings | air_temperature_k | Missing measurements | 6,270 | 27.12% |
| P04 | readings | tool_wear_min | Negative tool wear values | 25 | 0.11% |

Percentages are calculated relative to the 23,118 rows in `readings.csv`. Negative tool wear values are physically inconsistent with a nonnegative accumulated usage duration; the minimum recorded value is -2 minutes.

### Missingness Pattern

| Control type | Missing sensor | Missing within control type |
|---|---|---:|
| A | Vibration | 100% |
| B | Torque | 100% |
| C | Air temperature | 100% |

All 100 machines use all three control types. No deviations from the expected missingness pattern were detected in the three affected sensor columns. The missingness is structural and consistent with MAR. MCAR is not supported by the observed pattern; no supporting evidence for MNAR was identified, although the observed data alone cannot rule it out.

## 2. Potential Statistical Outliers

The IQR method (1.5 × IQR) flagged the following measurements:

| Sensor | Outlier count | Percentage of non-missing values |
|---|---:|---:|
| tool_wear_min | 33 | 0.14% |
| vibration_mm_s | 647 | 4.70% |
| torque_nm | 65 | 0.42% |
| process_temperature_k | 2,323 | 10.05% |
| air_temperature_k | 98 | 0.58% |
| rotational_speed_rpm | 170 | 0.74% |

These are potential statistical outliers, not confirmed data errors. Extreme sensor readings may reflect genuine degradation. Counts refer to individual sensor values, not unique records.

## 3. Additional Modeling Considerations

- The failure flag is imbalanced: 23,018 non-failure records (99.57%) and 100 failure records (0.43%). This is relevant to failure classification, not necessarily RUL regression.
- The dataset is synthetic, which limits conclusions about real industrial machines.

## 4. Validation Checks Passed

- No complete duplicate records or missing primary keys were detected.
- No duplicate primary keys or invalid foreign keys were detected.
- All 23,118 machine-cycle combinations match between readings and ground truth.
- Internal cycle continuity, RUL progression, final RUL, failure flag and failure mode checks passed.
- No missing values were detected in `units.csv` or `ground_truth.csv`.

## 5. Handoff Status

The issues are documented for the Data Cleaning phase. No raw values were modified, and no cleaning methods are prescribed in this log.

Evidence: saved outputs of Notebook 01 (Data Ingestion and Profiling), Notebook 02 (Data Validation and Missingness), and the final executed Notebook 03 (Exploratory Data Analysis). The IQR counts and percentages were cross-checked against the final Notebook 03 outputs.
