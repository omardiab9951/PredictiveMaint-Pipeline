

## Sprint 1 — Data Ingestion & Exploratory Data Analysis

This branch covers data ingestion, profiling, validation, missingness analysis, and exploratory data analysis (EDA). Its purpose is to understand the raw data and document observed quality issues. No raw data is modified, and no cleaning methods are prescribed.

## Dataset

The Machine Degradation dataset is synthetic and contains observations from 100 simulated machines.

**Source:** [Machine Degradation dataset on Hugging Face](https://huggingface.co/datasets/rasinmuhammed/predictive-maintenance-remaining-useful-life/tree/main) (Misata-generated dataset). 
| File | Rows | Columns | Description |
| --- | ---: | ---: | --- |
| `readings.csv` | 23,118 | 13 | Sensor measurements, operating cycles, RUL and failure labels |
| `units.csv` | 100 | 4 | Machine identifiers, lifetimes, failure modes and split assignments |
| `ground_truth.csv` | 23,118 | 3 | Simulated internal damage per machine and cycle |
| **Total** | **46,336** | **20** | Three related tables |

The tables are linked using `unit_id`; `readings.csv` and `ground_truth.csv` are matched using the composite key (`unit_id`, `cycle`). The six sensor variables describe tool wear, vibration, torque, process temperature, air temperature and rotational speed.

## Local Project Structure

The raw dataset is maintained separately in the shared [`dataset` branch](https://github.com/omardiab9951/PredictiveMaint-Pipeline/tree/dataset). The structure below shows the local project after placing the shared CSV files in `data/raw/`.

```text
PredictiveMaint-Pipeline/
├── data/
│       ├── readings.csv
│       ├── units.csv
│       └── ground_truth.csv
├── notebooks/
│   ├── 01_Data_Ingestion_and_Profiling.ipynb
│   ├── 02_Data_Validation_and_Missingness.ipynb
│   └── 03_Exploratory_Data_Analysis.ipynb
├── logs/
│   └── problem_list.md
├── requirements.txt
└── README.md
```

## Notebooks

| Notebook | Main tasks |
| --- | --- |
| [01 — Data Ingestion and Profiling](notebooks/01_Data_Ingestion_and_Profiling.ipynb) | Load CSV files, inspect dimensions and data types, document columns, calculate descriptive statistics, identify missing values and duplicate records. |
| [02 — Data Validation and Missingness](notebooks/02_Data_Validation_and_Missingness.ipynb) | Validate keys, cross-table consistency, cycle continuity, RUL and failure labels; inspect invalid sensor values and analyze missingness by control type, including MCAR/MAR/MNAR. |
| [03 — Exploratory Data Analysis](notebooks/03_Exploratory_Data_Analysis.ipynb) | Examine sensor distributions, IQR outliers, failure modes, machine lifetimes, correlations, sensor behavior near failure and damage progression. Model-related correlation analysis uses training machines only. |

## Key Findings

- No complete duplicate records, duplicate primary keys, missing primary keys or invalid foreign keys were detected.
- All 23,118 machine-cycle combinations match between the readings and ground truth tables.
- Cycle continuity, RUL progression and failure consistency checks passed.
- 25 negative tool wear values were detected, with a minimum of -2 minutes.
- Missing sensor values follow a structural pattern associated with the observed `control_type`, consistent with MAR. Observed data alone cannot rule out MNAR.

| Sensor | Missing values | Percentage | Associated control type |
| --- | ---: | ---: | --- |
| Vibration | 9,347 | 40.43% | A |
| Torque | 7,501 | 32.45% | B |
| Air temperature | 6,270 | 27.12% | C |

The IQR analysis identifies potential statistical outliers, which are not necessarily measurement errors. The full issue list and supporting counts are documented in [logs/problem_list.md](logs/problem_list.md).

## Getting Started

1. Clone the repository and switch to the `ingestion-eda` branch once it is available.

   ```bash
   git clone https://github.com/omardiab9951/PredictiveMaint-Pipeline.git
   cd PredictiveMaint-Pipeline
   git switch ingestion-eda
   ```

2. Create and activate a Python virtual environment (Windows PowerShell):

   ```powershell
   python -m venv .venv
   .\.venv\Scripts\Activate.ps1
   python -m pip install -r requirements.txt
   ```

3. Download `readings.csv`, `units.csv`, and `ground_truth.csv` from the shared [`dataset` branch](https://github.com/omardiab9951/PredictiveMaint-Pipeline/tree/dataset). Create the local `data/raw/` directory if needed and place the three CSV files inside it. Use the shared dataset version rather than downloading a separate copy from an external source. The raw files do not need to be committed to the `ingestion-eda` branch.

4. Open the project in VS Code with the Python and Jupyter extensions, select the `.venv` kernel, and run the notebooks in numerical order. The first two notebooks expect the working directory to be `notebooks/`.

## Limitations and Scope

- The dataset is simulated; findings do not establish performance on real industrial machines.
- Correlation does not imply causation, and statistical outliers are not confirmed errors.
- RUL is the prediction target. Failure labels, final machine lifetime and simulated internal damage are not intended as RUL input features.
- Data cleaning, SQL migration, feature engineering, model training and dashboard development belong to subsequent project stages.

## Sprint 1 Deliverables

- Data ingestion and profiling notebook
- Data validation and missingness notebook
- Exploratory data analysis notebook
- Data quality problem list
- Dependency file (`requirements.txt`)

The documented findings are provided as a handoff to the Data Cleaning phase. Treatment decisions remain with the cleaning team.
