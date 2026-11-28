# Agile Scrum Plan & Project Blueprint

*A Practical Team Plan for the Predictive Maintenance Pipeline*

## Project summary

Four students will build a repeatable pipeline for the synthetic, CC0 Machine Degradation dataset. The work processes three CSV files with 46,336 rows and 20 columns, from inspection through Remaining Useful Life (RUL) modeling.

The plan now has **three sprints**: Sprint 1 combines the original data-inspection and cleaning work; Sprint 2 validates and prepares the data; Sprint 3 builds and evaluates the models and completes the submission.

**Team planning guide:** 22 November–14 December 2026

# 1. Scrum in one minute

Scrum divides a large project into short, fixed-length work periods called **sprints**. At the start, the team chooses a set of tasks. During the sprint, members share progress and raise blockers. At the end, they show what works, get feedback, and agree on one improvement for the next sprint. Each sprint should leave something useful that can be inspected.

# 2. Team and Scrum roles

| Member | Technical responsibility | Scrum responsibility |
|---|---|---|
| Member 1 | Ingestion and EDA lead | Scrum Master in Sprint 1; helps clarify the product goal and coordinate inspection and cleaning. |
| Member 2 | Cleaning lead; owns the change log | Helps remove cleaning blockers in Sprint 1; supports cleaning fixes in Sprint 2. |
| Member 3 | Validation and feature engineering lead; includes integration and RUL target | Scrum Master in Sprint 2; coordinates validation and feature readiness. |
| Member 4 | ML lead; two models, Group K-Fold, and evaluation | Scrum Master in Sprint 3; coordinates the modeling and submission window. |
| All four | Development Team; share code review, report, and presentation work | Work together to deliver each sprint goal. |

**Product Owner:** the professor, or one team member acting on the professor’s behalf. The Product Owner clarifies priorities and accepts completed work. **Scrum Master:** the rotating member who helps the team follow the plan and address blockers.

# 3. Timeline

| Sprint | Dates | Goal | Lead |
|---|---|---|---|
| 1 | Sun 22–Fri 27 Nov | We understand and clean the data | Member 1; Member 2 leads cleaning; Member 3 drafts validation rules |
| 2 | Sat 28 Nov–Fri 4 Dec | The data is validated and model-ready | Member 3; Member 2 helps |
| 3 | Sat 5–Fri 11 Dec | We have a working light model and are ready to present | Member 4; everyone helps |
| Buffer | Sat 12–Mon 14 Dec | Final fixes and submission | Everyone |

All dates are in 2026. Sprint 1 runs 22–27 November, Sprint 2 runs 28 November–4 December, and Sprint 3 runs 5–11 December. Sprint 1 combines the former inspection and cleaning work. In Sprint 3, modeling is planned for days 1–3; the report, presentation, and final code review use days 4–7. The 12–14 December buffer is reserved for final fixes and submission.

# 4. Product backlog

The backlog is the ordered list of work the team may do. Priorities put safe, reliable data preparation first and the short modeling work last.

| Priority | Workgroup | Backlog items |
|---|---|---|
| 1 — P0 | Set up and inspect | S1-1 to S1-5: create the shared workspace; read the dataset documentation; ingest and inspect all three files; complete EDA; record the problem list. |
| 2 — P0 | Clean and log | S1-6 to S1-9: choose safe per-machine missing-value methods; clean confirmed issues; save clean copies; record every change. |
| 3 — P0 | Validate and prepare | S1-10; S2-1 to S2-5: draft validation rules; validate; integrate; create the RUL target; build past-only features; export the model-ready file. |
| 4 — P1 | Model and evaluate | S1-10; S3-1 to S3-4: prepare a small-sample code scaffold early; compare the two required models with a machine-based split and report MAE and RMSE. |
| 5 — P1 | Explain and submit | S1-11; S2-6; S3-5 to S3-7: write report sections as work proceeds; finish the report and presentation; review the code and run instructions. |

# 5. Sprint 1 — Understand and clean the data

**Dates:** Sunday 22–Friday 27 November 2026  
**Goal:** We understand and clean the data  
**Scrum Master:** Member 1

During the first part of this sprint, observe and document the data before changing it. Use placeholders such as `<machine_id_column>` and `<sensor_column>` until names are confirmed from `data/raw/schema.yaml`. In the cleaning work, keep the raw files unchanged. Decide how to treat each missing-value pattern per machine and field. Never replace missing sensor readings with one global mean. If an unusual value may be a real machine event, investigate before changing it.

| Task ID | Task | Owner | Input | Output file | Done when |
|---|---|---|---|---|---|
| S1-1 | Set up the shared repository and folders. | M1; all | Project brief and team agreement | `README.md`; starter tree | All members can open the project; raw files have a protected home. |
| S1-2 | Read dataset README and schema. | M1 | `data/raw/README.md`; `schema.yaml` | `logs/problem_list.md` notes | Purpose, file meanings, and real field names are recorded; questions are listed. |
| S1-3 | Load the three CSVs; check shape, columns, and types in notebook 01. | M1 | Three raw CSV files; schema | `notebooks/01_ingest.ipynb` | All files load; observed shapes and types are recorded; raw files are unchanged. |
| S1-4 | Explore all files: missingness, duplicates, outliers, distributions, cycle order, and ID/cycle alignment. | M1; M2–M4 review | Raw files; notebook 01 | `notebooks/02_eda.ipynb`; histograms and missing-value plots | Findings are documented for each file; no data is fixed during EDA; chart labels use confirmed schema names. |
| S1-5 | Write the observed issues and open questions. | M1 | EDA notes and charts | `logs/problem_list.md` | Every issue has a file, field or generic placeholder, evidence, and a question or next action. |
| S1-6 | Define a missing-value method for each affected field and machine. | M2 | `problem_list.md`; raw data; schema | Cleaning rules in `notebooks/03_cleaning.ipynb` | Method is justified; per-machine forward-fill or interpolation is considered; global mean is not used. |
| S1-7 | Resolve confirmed duplicates, outliers, and incorrect types. | M2 | Raw files; approved rules; problem list | `notebooks/03_cleaning.ipynb` | Each fix is evidence-based; real spikes are not removed as sensor errors without review. |
| S1-8 | Save cleaned copies of all three files. | M2 | Raw files; cleaning notebook | `data/clean/readings_clean.csv`; `units_clean.csv`; `ground_truth_clean.csv` | All three clean files exist; row and field changes are traceable; raw files are untouched. |
| S1-9 | Record what changed, how many rows, and why. | M2 | Cleaning steps and before/after counts | `logs/change_log.csv` | Every change has a reason and count; unchanged data is not described as changed. |
| S1-10 | Draft pass/fail validation rules. | M3 | Schema; problem list; cleaning rules | Draft in `notebooks/04_validation.ipynb` | Rules cover types, ranges, IDs, cycle consistency, and remaining missing values. |
| S1-11 | Start report sections on EDA and cleaning. | M1 and M4 | EDA notes; problem list; change log as it grows | `reports/` report source | Findings and cleaning choices are explained clearly; unknown field names are checked against the schema. |
| S1-12 | Prepare a modeling-code scaffold on a small sample. | M4 | Small sample; schema; project setup | `src/modeling.py` draft | Code can load the sample and shows where target, features, and evaluation will go; no final result is claimed. |

**Sprint review deliverables:** `notebooks/01_ingest.ipynb`, `notebooks/02_eda.ipynb`, `notebooks/03_cleaning.ipynb`, three files in `data/clean/`, `logs/problem_list.md`, `logs/change_log.csv`, draft validation rules, EDA/cleaning report sections, and the small-sample modeling scaffold. The review confirms the team understands the data, cleaning decisions are evidenced, and raw files were not edited.

# 6. Sprint 2 — Validate and prepare features

**Dates:** Saturday 28 November–Friday 4 December 2026  
**Goal:** The data is validated and model-ready  
**Scrum Master:** Member 3

A failed validation is useful evidence, not something to hide. Send failures to Member 2 for correction, then rerun the checks. Create the RUL target only after reading the dataset README for its failure definition.

| Task ID | Task | Owner | Input | Output file | Done when |
|---|---|---|---|---|---|
| S2-1 | Run validation; return failures to Member 2; record results. | M3; M2 fixes | Clean files; draft rules | `logs/validation_report.csv` | Types, ranges, IDs, cycles, and missing-value checks pass; failures have an owner and are rerun after fixes. |
| S2-2 | Combine the three cleaned files by machine ID and cycle where needed. | M3 | Clean files; validated names in schema | `notebooks/05_integration_features.ipynb` | Joins preserve intended rows; machine and cycle alignment is checked; no unplanned row multiplication occurs. |
| S2-3 | Create the RUL target using the dataset’s stated failure definition. | M3 | Integrated data; dataset README | RUL target in feature notebook | Failure definition is cited from README; target values follow that definition and are checked. |
| S2-4 | Build rolling averages, trends, and differences using past cycles only. | M3 | Integrated data with cycle order | Features in `notebooks/05_integration_features.ipynb` | Each feature uses only current or earlier cycles; no future-cycle values enter a feature. |
| S2-5 | Export the model-ready dataset. | M3 | Validated target and features | `data/processed/model_ready.csv` | File loads successfully; rows, target, feature rules, and machine IDs are documented. |
| S2-6 | Write report sections on validation and feature preparation. | All; M3 coordinates | Validation report; integration and feature notes | `reports/` report source | Pass/fail outcomes, RUL definition, and leakage safeguards are explained. |

**Sprint review deliverables:** `logs/validation_report.csv`, `data/processed/model_ready.csv`, and report sections for validation and features. Member 3 hands the accepted model-ready file and its checks to Member 4.

# 7. Sprint 3 — Compare two light models and finish

**Dates:** Saturday 5–Friday 11 December 2026  
**Goal:** We have a working light model and are ready to present  
**Scrum Master:** Member 4

**Days 1–3:** complete the modeling tasks. **Days 4–7:** focus on the report, presentation, code review, and run instructions. Keep the ML section short; the report should emphasize the data pipeline and its evidence.

| Task ID | Task | Owner | Input | Output file | Done when |
|---|---|---|---|---|---|
| S3-1 | Train the Linear Regression baseline. | M4 | `model_ready.csv`; fixed seed | `models/baseline_linear_regression.pkl` | Training and prediction run; baseline metrics are saved. |
| S3-2 | Train the Random Forest main model. | M4 | `model_ready.csv`; fixed seed | `models/random_forest.pkl` | Training and prediction run; settings are recorded; no future-cycle features are used. |
| S3-3 | Use Group K-Fold split by machine; never random rows. | M4; M3 reviews | Model-ready data with machine IDs | Fold results in `reports/model_results.csv` | The same machine never appears in training and validation folds; seed and fold method are recorded. |
| S3-4 | Evaluate both models with MAE and RMSE. | M4 | Predictions from both models; group folds | `reports/model_results.csv` | Both metrics are reported for both models; comparison and limitations are stated. |
| S3-5 | Finish the report: EDA, cleaning, logs, validation, before/after, short ML comparison, and synthetic-data limitation. | All; M1 and M2 coordinate | Sprint evidence; model results | `reports/final_report.pdf` | Pipeline is the main story; one model-results table and a short conclusion are included. |
| S3-6 | Prepare and deliver the presentation. | All | Final report; clean figures; model results | `reports/presentation.pptx` | Key pipeline decisions and results are clear; the synthetic-data limitation is disclosed. |
| S3-7 | Review the code, README, and end-to-end run command. | All; M4 coordinates | Source files; notebooks; README; requirements | `src/run_pipeline.py`; `README.md` | A teammate reviews changes; instructions work from a clean start; pipeline stages run in order. |

**Sprint review deliverables:** two trained models; `reports/model_results.csv` with MAE and RMSE; final report and presentation; reviewed source code and run instructions. Use the 12–14 December buffer for final fixes and submission.

# 8. Scrum events and team habits

| Event | When / length | What the team does |
|---|---|---|
| Sprint Planning | First day; 30–45 min | Agree on the sprint goal, choose tasks, confirm owners and outputs, and identify dependencies. |
| Daily Standup | Every 1–2 days; 10 min | Each person answers: What did I finish? What will I do next? What is blocking me? |
| Sprint Review | Last day; 20–30 min | Show working files or results, compare them with the goal, and gather feedback. |
| Retrospective | Right after review; 15 min | Discuss how the teamwork went and choose one practical improvement for the next sprint. |

**Quick retrospective template:** **Went well:** `________` | **Could improve:** `________` | **One action for next sprint:** `________` | **Owner:** `________` | **Check by:** `________`

# 9. Definition of Done

A task or deliverable is Done only when all relevant checks are true:

- Code runs from top to bottom without errors, or the non-code output is complete and readable.
- Results and decisions are documented in the agreed file.
- Another member has reviewed it and the review comments are resolved.
- The approved work is merged to the shared main branch.
- Raw data files are never modified; every cleaning change is traceable.

# 10. Project structure

The tree below is the agreed target layout. The raw folder is read-only. File names and field names must match the dataset documentation and schema.

```text
predictive-maintenance-pipeline/
├── README.md
├── requirements.txt
├── .gitignore
├── data/
│   ├── raw/                (NEVER edited)
│   │   ├── readings.csv
│   │   ├── units.csv
│   │   ├── ground_truth.csv
│   │   ├── README.md       (dataset's own documentation)
│   │   └── schema.yaml
│   ├── clean/
│   │   ├── readings_clean.csv
│   │   ├── units_clean.csv
│   │   └── ground_truth_clean.csv
│   └── processed/
│       └── model_ready.csv
├── notebooks/
│   ├── 01_ingest.ipynb
│   ├── 02_eda.ipynb
│   ├── 03_cleaning.ipynb
│   ├── 04_validation.ipynb
│   ├── 05_integration_features.ipynb
│   └── 06_modeling.ipynb
├── src/
│   ├── __init__.py
│   ├── config.py           (paths and constants)
│   ├── ingest.py
│   ├── cleaning.py
│   ├── validation.py
│   ├── integration.py
│   ├── features.py
│   ├── modeling.py
│   └── run_pipeline.py     (runs all stages in order)
├── logs/
│   ├── problem_list.md
│   ├── change_log.csv
│   └── validation_report.csv
├── models/
│   ├── baseline_linear_regression.pkl
│   └── random_forest.pkl
├── reports/
│   ├── figures/
│   ├── model_results.csv
│   ├── final_report.pdf
│   └── presentation.pptx
└── docs/
    ├── sprint_board.md
    ├── definition_of_done.md
    └── retrospectives.md
```

# 11. File and folder guide

| Name | Purpose | Owner | Created in sprint |
|---|---|---|---|
| `predictive-maintenance-pipeline/` | Shared project root and working copy. | All | S1 |
| `README.md` | How to set up and run the work; final methods and results summary. | M1 + M4 | S1; update S3 |
| `requirements.txt` | Lists Python packages needed to run notebooks and code. | M4 | S1; update S3 |
| `.gitignore` | Keeps temporary files and unsuitable large files out of version control. | M1 | S1 |
| `data/` | Top-level home for untouched, cleaned, and processed data. | M1 | S1 |
| `data/raw/` and source CSVs | Read-only copy of supplied source files and documentation. | M1 | S1 |
| `data/raw/README.md`; `schema.yaml` | Dataset provider’s instructions, failure definition, field names, types, and schema notes. | M1 | S1 |
| `data/clean/` and `*_clean.csv` | Clean copies kept separate from the original data. | M2 | S1 |
| `data/processed/model_ready.csv` | Validated features and RUL target for modeling. | M3 | S2 |
| `notebooks/` | Ordered, readable records of the analysis steps. | All | S1–S3 |
| `01_ingest.ipynb` | Load source files and record shapes, fields, and types. | M1 | S1 |
| `02_eda.ipynb` | Inspect data and make simple histograms and missing-value plots. | M1 | S1 |
| `03_cleaning.ipynb` | Apply documented cleaning rules and record checks. | M2 | S1 |
| `04_validation.ipynb` | Run pass/fail rules and produce validation results. | M3 | S1 draft; S2 run |
| `05_integration_features.ipynb` | Join cleaned files and create target and past-only features. | M3 | S2 |
| `06_modeling.ipynb` | Train and evaluate the two required models. | M4 | S3 |
| `src/` | Reusable Python code called by notebooks and the full run command. | All | S1–S3 |
| `__init__.py`; `config.py`; `ingest.py` | Python package marker, project paths/constants, and reusable file-loading checks. | M1; M4 | S1 |
| `cleaning.py` | Reusable cleaning functions that follow approved rules. | M2 | S1 |
| `validation.py` | Reusable pass/fail data checks. | M3 | S1–S2 |
| `integration.py`; `features.py` | Reusable joins with row/key checks; RUL target and past-only feature functions. | M3 | S2 |
| `modeling.py` | Training, machine-group evaluation, and metric functions. | M4 | S1 draft; S3 |
| `run_pipeline.py` | Runs the pipeline stages in the correct order. | M4 | S3 |
| `logs/` | Evidence of observed problems, changes, and validation. | All | S1–S2 |
| `problem_list.md` | Issues found during EDA, before anything is fixed. | M1 | S1 |
| `change_log.csv` | What changed, how many rows, and why. | M2 | S1 |
| `validation_report.csv` | Pass/fail outcomes and any returned failures. | M3 | S2 |
| `models/` | Saved fitted model files for reproducibility. | M4 | S3 |
| `baseline_linear_regression.pkl`; `random_forest.pkl` | Saved Linear Regression baseline and Random Forest model. | M4 | S3 |
| `reports/figures/` | Simple notebook charts used to support EDA and reporting. | M1 | S1; update S3 |
| `model_results.csv` | Both models’ Group K-Fold MAE and RMSE results. | M4 | S3 |
| `final_report.pdf` | Pipeline findings, data-quality evidence, brief model results, and limitations. | All | S3; draft sections in S1–S2 |
| `presentation.pptx` | Short presentation of the pipeline and findings. | All | S3 |
| `docs/` | Short team process notes and agreements. | All | S1–S3 |
| `sprint_board.md`; `definition_of_done.md`; `retrospectives.md` | Task status, shared quality checklist, and notes/action items from retrospectives. | Scrum Master | S1–S3 |

# 12. Handoff chain

| From | To | Files | Checklist before handoff / what the receiver confirms |
|---|---|---|---|
| M1 and M2 | M3 | `logs/problem_list.md`; three clean files; `logs/change_log.csv` | Issues have evidence, source file, and field/cycle reference; cleaning decisions or reasons for no change are documented. M3 checks file names, row counts, log coverage, and suitability for validation. |
| M3 | M4 | `logs/validation_report.csv`; `data/processed/model_ready.csv` | Validation passes or failures are documented; the failure definition comes from README; features use past cycles only; machine IDs remain available. M4 confirms target, features, groups, and evaluation inputs are clear. |
| M4 | Whole team | Two model files; `reports/model_results.csv` | Both models have MAE/RMSE; folds are split by machine; seed and limitations are recorded. The team checks results are reproducible and ready to explain. |

# 13. GitHub workflow

Use one branch per person per task. Naming examples: `member1/s1-eda`, `member2/s1-cleaning`, `member3/s2-features`, and `member4/s3-modeling`. Open a pull request and ask another member to review it before merging to `main`. Use short commit messages such as `S1-8: save cleaned readings`. Never edit `data/raw/` or commit large raw-data changes.

Track work in a simple task board, such as Trello or GitHub Projects, with columns: **To Do → In Progress → In Review → Done**.

# 14. Notebook and code conventions

- Keep the numbered notebook order and give each notebook one purpose. Add a Markdown header with title, author, date, purpose, input, and output.
- Put reusable functions in `src/`; use notebooks to run steps and explain results.
- Use a fixed random seed for repeatable modeling and evaluation. Record it in the run instructions.
- Use generic placeholders such as `<sensor_column>` or `<machine_id_column>` until real names are checked in `data/raw/schema.yaml`.
- Include these packages in `requirements.txt`: `pandas`, `numpy`, `matplotlib`, `seaborn`, `scikit-learn`, and `jupyter`.

# 15. Sprint deliverables

| Sprint | Deliverable | Evidence to show at review |
|---|---|---|
| 1 | EDA, problem list, cleaned files, and change log | `01_ingest.ipynb`, `02_eda.ipynb`, `03_cleaning.ipynb`, simple charts, `problem_list.md`, three clean copies, cleaning decisions, `change_log.csv`, draft validation rules |
| 2 | Validation report and model-ready data | `validation_report.csv`, joined features, RUL target, and leakage checks |
| 3 | Model results, report, and presentation | Two models with MAE/RMSE; report and presentation disclose the synthetic-data limitation. |

# 16. Risks and mitigation

| Risk | Mitigation |
|---|---|
| A later task is blocked by an earlier task. | Keep handoffs explicit; raise blockers at standups; send validation failures back for correction and rerun checks. |
| Work takes longer than planned. | Use the 12–14 December buffer and keep a visible list of unfinished must-do tasks. |
| The last sprint becomes too heavy. | Start report writing in Sprint 1 and Sprint 2; limit modeling to the two agreed models and a short results section. |
| Feature work delays evaluation. | Member 4 prepares the modeling scaffold in Sprint 1; if time is short, simplify features while retaining both models. |

# 17. Final submission checklist

- [ ] Three cleaned files, with the original raw files unchanged.
- [ ] Reproducible pipeline code and a README explaining how to run it.
- [ ] `change_log.csv` and `validation_report.csv` complete.
- [ ] Before-versus-after data-quality report included.
- [ ] Two trained models with machine-based Group K-Fold MAE and RMSE results.
- [ ] Final report and presentation disclose the synthetic dataset; a teammate reviewed the code and checked the full run.
