# PredictiveMaint-Pipeline: A Data Cleansing Pipeline for Predictive Maintenance

## Master Project Progress & Documentation Report

**Course:** Data Cleansing & Migration (university)  
**Prepared for:** Four-member project team  
**Issue date:** 28 November 2026  
**Version:** 1.1  
**Current planning window:** Sprint 2 (proposed dates: 28 November–4 December 2026)  
**Development status:** Not Started, based on the latest evidence available in the prior report; no newer implementation evidence was supplied with this update.

The team plans to build a repeatable pipeline for the synthetic, CC0 Machine Degradation dataset. Data cleansing and preparation are the main focus; the final sprint includes a brief comparison of two light RUL models.

**Planning dates are proposals, not evidence that work has begun.** This revision updates the planned sprint structure to match the Agile plan. It does not claim that any development task has started or been completed.

## Contents

1. Project Overview
2. Purpose and Recordkeeping Principles
3. Current Project Progress
4. Development Roadmap and Progress Tracker
5. Pipeline Stage Record
6. Team Responsibilities and Workflow
7. Proposed Three-Sprint Workflow (Planning Only)
8. Decisions, Deliverables, and Open Record Items
9. Version History
10. Future Update Procedure

## 1. Project Overview

**Project name:** PredictiveMaint-Pipeline. **Course:** Data Cleansing & Migration (university). **Team size:** Four members. PredictiveMaint-Pipeline is a planned data-cleansing pipeline for predictive maintenance using the synthetic Machine Degradation dataset from Misata Studio, licensed CC0. The supplied project description identifies three CSV files—`readings.csv`, `units.csv`, and `ground_truth.csv`—linked by machine ID, with 46,336 rows and 20 columns in total. The planned flow is ingestion, EDA, cleaning, validation, integration, feature engineering, export, then light ML modeling. Data work is the main focus. The modeling task is limited to Linear Regression and Random Forest for Remaining Useful Life (RUL).

### 1.1 Suggested technology context

All items below are suggestions recorded in the initial project brief; final adoption has not been specified.

| Area | Suggested technology | Decision status |
|---|---|---|
| Programming | Python | Suggested; final adoption not specified |
| Data handling | pandas and NumPy | Suggested; final adoption not specified |
| Simple charts | matplotlib and seaborn; notebook charts only | Suggested; final adoption not specified |
| Modeling | scikit-learn | Suggested; final adoption not specified |
| Notebooks | Jupyter notebooks | Suggested; final adoption not specified |
| Version control | GitHub | Suggested; final adoption not specified |

## 2. Purpose and Recordkeeping Principles

This report is the central, versioned record of PredictiveMaint-Pipeline’s verified progress, decisions, and planned work. Update it when the team supplies new, confirmed information. The editable Word document is the working master; the PDF is a shareable snapshot of the same report version.

### 2.1 Updating rules

- Preserve prior completed work and important decision history.
- Add newly completed work only when the team supplies evidence; revise outdated information without erasing relevant history.
- Never mark unfinished or merely scheduled work as complete.
- Record actual work, decisions, implementation details, and results only when verified by the team.
- Keep the tracker, report, and latest project status consistent.

## 3. Current Project Progress

| Progress area | Status recorded in the available baseline |
|---|---|
| Planning | Completed — project idea, scope, team roles, and Agile Scrum plan are defined. The plan has since been revised to combine the former Sprints 1 and 2 into one extended Sprint 1. |
| Development work | Not Started in the latest supplied status. No newer development evidence was supplied with this report update. |
| Current planning stage | Sprint 2 is the current planned window (28 November–4 December 2026); actual start/progress has not been confirmed. |

### 3.1 Planning baseline

Planning defines the project idea and scope, the four-member role proposal, and the Agile Scrum plan. This update consolidates the former data inspection and cleaning sprints into one longer Sprint 1 and renumbers the remaining work as Sprints 2 and 3. It does not demonstrate implementation or completion of any data-pipeline stage.

### 3.2 Current stage boundary

Development status remains Not Started based on the latest status supplied in the prior report; no subsequent progress evidence was provided. Sprint and buffer dates are proposed planning dates only. A scheduled date never changes a status. No data profiling, cleaning, validation, feature engineering, modeling, code review, test, or delivery evidence is recorded in the supplied baseline.

## 4. Development Roadmap and Progress Tracker

The dates below are proposed windows. A completion date is recorded only when completion is verified; none has been supplied for this baseline.

| Stage / sprint | Status | Main deliverables / record | Completion date |
|---|---|---|---|
| Project planning | Completed | Idea, scope, roles, and revised three-sprint Agile Scrum plan are defined. | Not provided |
| Sprint 1 — 22–27 Nov 2026 (proposed) | Not Started, based on latest supplied status | Ingestion, EDA, problem list, cleaning decisions, cleaned copies, change log, draft validation rules, EDA/cleaning report sections, and small-sample modeling scaffold. | Not provided |
| Sprint 2 — 28 Nov–4 Dec 2026 (proposed) | Not Started | Validation, integration, README-based RUL target, past-cycle features, and `data/processed/model_ready.csv`. | Not provided |
| Sprint 3 — 5–11 Dec 2026 (proposed) | Not Started | Linear Regression and Random Forest; machine-based Group K-Fold; MAE and RMSE; final report, presentation, and code review. | Not provided |
| Buffer — 12–14 Dec 2026 (proposed) | Not Started | Final fixes and submission. | Not provided |

**Status key:** **Completed** means supplied evidence confirms the listed work is complete. **Planned (proposal)** means scheduled or intended work only. **In Progress** means verified work has begun but is unfinished. **Not Started** means no work is reported as begun. The sprint and buffer dates remain proposals; the available development status is Not Started.

## 5. Pipeline Stage Record

Every pipeline stage below is **Not Started** according to the latest supplied project status. Inputs and outputs are planned; no file or result listed here is claimed to exist.

### 5.1 Ingestion

**Responsible:** Member 1. **Purpose:** Load and inventory the three supplied CSVs without changing source data. **Planned input:** `readings.csv`, `units.csv`, `ground_truth.csv`, dataset README, and `schema.yaml` when available. **Planned output:** `notebooks/01_ingest.ipynb` with observed shapes, fields, and types. **Status:** Not Started.

### 5.2 EDA

**Responsible:** Member 1; others may review. **Purpose:** Observe and document data quality only—no fixing or cleaning during EDA. **Planned input:** Read-only raw files and ingestion notes. **Planned output:** `logs/problem_list.md` and simple notebook charts. **Status:** Not Started.

### 5.3 Cleaning

**Responsible:** Member 2; owns the change log. **Purpose:** Apply justified, per-machine treatment to confirmed issues. Consider forward-fill or interpolation where appropriate; never replace missing readings with a global mean. **Planned input:** Raw files, problem list, and confirmed schema. **Planned output:** Cleaned copies plus `logs/change_log.csv` recording each change and its reason/count. **Planned sprint:** Sprint 1. **Status:** Not Started.

### 5.4 Validation

**Responsible:** Member 3. **Purpose:** Check schema, types, ranges, IDs, cycle consistency, and remaining missing values; return failures for correction and recheck. **Planned input:** Cleaned files and draft rules. **Planned output:** `logs/validation_report.csv`. Draft validation rules are planned in Sprint 1; validation execution is planned in Sprint 2. **Status:** Not Started.

### 5.5 Integration

**Responsible:** Member 3. **Purpose:** Combine cleaned files using confirmed machine identifiers and cycle alignment where needed. **Planned input:** Validated cleaned files and schema names. **Planned output:** Integrated working data in the feature notebook. **Planned sprint:** Sprint 2. **Status:** Not Started.

### 5.6 Feature Engineering

**Responsible:** Member 3. **Purpose:** Create the RUL target only after checking the dataset README for its failure definition; construct features from current or past cycles only, preventing future-data leakage. **Planned input:** Integrated data, cycle order, and README definition. **Planned output:** Documented target and past-only features. **Planned sprint:** Sprint 2. **Status:** Not Started.

### 5.7 Export

**Responsible:** Member 3. **Purpose:** Save a validated, documented modeling dataset with machine identifiers retained. **Planned input:** Validated target and approved features. **Planned output:** `data/processed/model_ready.csv`. **Planned sprint:** Sprint 2. **Status:** Not Started.

### 5.8 ML Modeling

**Responsible:** Member 4. **Purpose:** Briefly compare exactly two models: Linear Regression (baseline) and Random Forest. Use Group K-Fold split by machine, never random rows, with a fixed random seed; report MAE and RMSE. **Planned input:** Model-ready data with machine IDs. **Planned output:** Two model files and `reports/model_results.csv`. A small-sample code scaffold is planned in Sprint 1; model training and evaluation are planned in Sprint 3. **Status:** Not Started.

## 6. Team Responsibilities and Workflow

The following technical roles are proposed until the four-member team confirms them. Report, presentation, and code review are shared by all members.

### 6.1 Technical roles

| Member | Proposed technical role | Primary planned responsibility |
|---|---|---|
| Member 1 | Ingestion & EDA Lead | Source inventory, observational EDA, and problem list. Scrum Master for Sprint 1. |
| Member 2 | Cleaning Lead; owns change log | Per-machine cleaning and traceable change records; supports validation fixes. |
| Member 3 | Validation & Feature Engineering Lead | Draft validation rules in Sprint 1; validation, integration, RUL target, past-only features, and model-ready export in Sprint 2. Scrum Master for Sprint 2. |
| Member 4 | ML Lead | Modeling scaffold in Sprint 1; two-model comparison, machine-based Group K-Fold, and metrics in Sprint 3. Scrum Master for Sprint 3. |
| All four | Shared project work | Final report, presentation, and code review. |

### 6.2 Scrum roles

**Product Owner:** the professor or one member acting on the professor’s behalf; clarifies priorities and accepts completed work. **Scrum Master:** rotates by sprint—Member 1 in Sprint 1, Member 3 in Sprint 2, and Member 4 in Sprint 3. Member 2 remains the cleaning lead and supports cleaning-related blockers. **Development Team:** all four members.

### 6.3 Handoff chain

`logs/problem_list.md` → three cleaned files + `logs/change_log.csv` → `logs/validation_report.csv` + `data/processed/model_ready.csv` → trained models + `reports/model_results.csv`. The receiving member checks the incoming files and evidence before relying on them. The cleaning handoff and initial cleaning outputs are part of Sprint 1; validation and model-ready outputs are planned in Sprint 2.

### 6.4 Reopening agreed decisions

Any member may raise a concern. The team votes; a simple majority may reopen an agreed decision. Record the concern, vote, reason for reopening, and final outcome alongside the original decision.

### 6.5 Who owns what

| Topic | Proposed owner | Boundary |
|---|---|---|
| Problem list | Member 1 | Record observed issues and evidence; do not fix data during EDA. |
| Cleaned files and change log | Member 2 | Keep raw sources unchanged; explain each applied change. |
| Validation rules and model-ready data | Member 3 | Draft rules during Sprint 1; validate and prepare model-ready data in Sprint 2. Use confirmed schema; check README before defining RUL; prevent future-cycle leakage. |
| Models and results | Member 4 | Exactly two agreed models; Group K-Fold by machine; fixed seed; MAE and RMSE. |
| Final report and presentation | All four | Use verified pipeline evidence and disclose that the dataset is synthetic. |

## 7. Proposed Three-Sprint Workflow (Planning Only)

The schedule is a proposal, not evidence that a sprint has started. Sprint 1 runs 22–27 November and combines the former Sprint 1 ingestion/EDA work and former Sprint 2 cleaning work into one sprint. Sprint 2 runs 28 November–4 December and covers validation and feature engineering. Sprint 3 runs 5–11 December and reserves days 1–3 for the short ML task and days 4–7 for the report, presentation, and code review. The 12–14 December buffer is for final fixes and submission.

| Sprint | Proposed dates | Proposed goal | Scrum Master |
|---|---|---|---|
| 1 | 22–27 Nov 2026 | Understand and clean the data; produce EDA evidence, cleaned copies, change log, draft validation rules, and a small-sample modeling scaffold. | Member 1 |
| 2 | 28 Nov–4 Dec 2026 | Validate and prepare model-ready features, including integration, RUL target, and past-only features. | Member 3 |
| 3 | 5–11 Dec 2026 | Train and evaluate two models; complete the final report, presentation, and code review. | Member 4 |
| Buffer | 12–14 Dec 2026 | Final fixes and submission. | Everyone |

### 7.1 Scrum events

| Event | Timing | Purpose |
|---|---|---|
| Sprint Planning | Day 1; 30–45 min | Agree on the sprint goal, selected work, owners, and outputs. |
| Daily Standup | Every 1–2 days; 10 min | Share completed work, next task, and blockers. |
| Sprint Review | Last day; 20–30 min | Show actual outputs and compare them with the goal. |
| Retrospective | After review; 15 min | Discuss teamwork and choose one practical improvement. |

### 7.2 Definition of Done

A work item is Done only when the code runs top to bottom; results and decisions are documented; another member has reviewed it; approved work is merged on GitHub; and raw data remains unchanged. For data changes, the relevant checks and records must also be complete.

### 7.3 Planned project folder structure

```text
PredictiveMaint-Pipeline/
├── data/
│   ├── raw/          (read-only source files)
│   ├── clean/
│   └── processed/
├── notebooks/
├── src/
├── logs/
├── models/
├── reports/
└── docs/
```

## 8. Decisions, Deliverables, and Open Record Items

| Record item | Current record / open information |
|---|---|
| Sprint plan | Revised from four sprints to three: Sprint 1 combines inspection and cleaning; Sprint 2 covers validation and feature engineering; Sprint 3 covers modeling and final submission. |
| Dataset column names | Not yet known; obtain actual names from `schema.yaml` after the data is opened. |
| Missing-value strategy | Not yet decided; determine by field and machine after examining evidence. |
| RUL definition | Use the failure definition in the dataset README before creating the target. |
| Project name | Final project name: PredictiveMaint-Pipeline. |
| Technology stack | Python, pandas, NumPy, matplotlib/seaborn, scikit-learn, Jupyter, and GitHub are suggested; final adoption not specified. |
| Implementation assignments | Proposed roles only until the team confirms them. |
| Implementation and results evidence | No new evidence supplied with this update. The latest status in the prior report says no code, loaded/profiled/cleaned data, metrics, or model is reported. |
| Synthetic-data disclosure | Mandatory: identify the Machine Degradation dataset as synthetic in the final report and presentation. |

## 9. Version History

| Version | Issue date | Summary |
|---|---|---|
| 1.0 | 19 November 2026 | Initial baseline recording project scope, proposed roles, four-sprint plan, pipeline stages, and development status as Not Started. |
| 1.1 | 28 November 2026 | Updated planned workflow to three sprints: combined the former Sprints 1 and 2 into Sprint 1; renumbered validation/feature work and modeling/submission to Sprints 2 and 3; updated sprint dates to 22 Nov–11 Dec and the buffer to 12–14 Dec; updated Scrum Master rotation. No implementation progress was added. |

## 10. Future Update Procedure

When new verified project information is supplied, update this report in a controlled sequence:

1. Read the latest report and preserve completed work, decisions, and relevant history.
2. Identify which stage the new information concerns; separate a plan from actual implementation.
3. Add the verified work and evidence—for example, the problem list, change log, validation report, model results, or review record.
4. After each sprint review, update the tracker status and enter a completion date only when work is confirmed complete.
5. Keep unfinished work marked In Progress or Not Started; never infer completion from a scheduled date.
6. Update the version history and keep the editable Word master and PDF snapshot aligned.
7. Replace the shareable PDF with the latest version while retaining prior version history and relevant decisions.
