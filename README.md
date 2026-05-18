<div align="center">

# ⚡ FAILSAFE
### Advanced Early Student Risk Detection & Intelligence Engine

[![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-2.0-009688?style=for-the-badge&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![XGBoost](https://img.shields.io/badge/XGBoost-ML%20Engine-F7931E?style=for-the-badge)](https://xgboost.readthedocs.io/)
[![React](https://img.shields.io/badge/React-19-61DAFB?style=for-the-badge&logo=react&logoColor=black)](https://react.dev/)
[![Tailwind CSS](https://img.shields.io/badge/Tailwind_CSS-v4-06B6D4?style=for-the-badge&logo=tailwindcss&logoColor=white)](https://tailwindcss.com/)
[![SHAP](https://img.shields.io/badge/SHAP-Explainability-FF6B6B?style=for-the-badge)](https://shap.readthedocs.io/)

<br/>

> **FAILSAFE** is a production-grade, end-to-end AI system that predicts student academic failure risk and delivers bias-free, actionable, educator-facing intervention plans — powered by XGBoost, SHAP explainability, and a prescriptive intelligence engine.

<br/>

![FAILSAFE Dashboard Preview](https://placehold.co/900x450/1a1a2e/e2e8f0?text=FAILSAFE+Intelligence+Dashboard&font=montserrat)

</div>

---

## 📌 Table of Contents

- [The Problem](#-the-problem)
- [Why FAILSAFE is Different](#-why-failsafe-is-different)
- [System Architecture](#-system-architecture)
- [Features](#-features)
- [Tech Stack](#-tech-stack)
- [Dataset](#-dataset)
- [ML Pipeline](#-ml-pipeline)
- [Risk Scoring & Tiers](#-risk-scoring--tiers)
- [SHAP Explainability](#-shap-explainability)
- [Prescriptive Intervention Engine](#-prescriptive-intervention-engine)
- [Ethical Design: Bias-Free by Architecture](#-ethical-design-bias-free-by-architecture)
- [API Reference](#-api-reference)
- [Frontend](#-frontend)
- [Project Structure](#-project-structure)
- [Getting Started](#-getting-started)
- [Testing](#-testing)
- [Author](#-author)

---

## 🎯 The Problem

Traditional student performance systems are **reactive** — they flag a student only after they have already failed. By that point, meaningful intervention is too late.

Academic advisors are left asking:
- *Which students are heading toward failure — right now?*
- *Why exactly is this specific student at risk?*
- *What concrete action should I take, today?*

**FAILSAFE answers all three.**

---

## 💡 Why FAILSAFE is Different

Most student risk projects stop at "predict the grade." FAILSAFE is engineered to a fundamentally different standard:

| Capability | Average Project | FAILSAFE |
|---|---|---|
| **Prediction** | Direct grade regression | Binary risk classification (fail / pass) |
| **Explainability** | None / global feature importance | Per-student SHAP value decomposition |
| **Actionability** | None | 35+ mapped, real-world intervention plans |
| **Fairness** | Uses age, sex, address as features | Demographic features excluded by design |
| **Interface** | None / Jupyter notebook | Full React + Tailwind v4 dashboard |
| **API** | None | FastAPI with structured JSON responses |
| **Data Timing** | Uses all grades (leakage) | Three distinct temporal models |

> This is not a prototype. FAILSAFE is designed as a **deployable academic intelligence tool**.

---

## 🏗️ System Architecture

```
                     ┌──────────────────────────────────────────┐
                     │           CSV Upload (Faculty)           │
                     └─────────────────┬────────────────────────┘
                                       │
                     ┌─────────────────▼────────────────────────┐
                     │         FastAPI Backend (/predict)        │
                     │   app/api.py  ·  app/main.py              │
                     └──┬────────────────────────────────────┬──┘
                        │                                    │
           ┌────────────▼──────────┐        ┌───────────────▼────────────┐
           │   Data Preprocessing  │        │     Feature Engineering     │
           │   src/data_prep.py    │        │  support_index, risk_behavior│
           └────────────┬──────────┘        └───────────────┬────────────┘
                        │                                    │
                        └──────────────┬─────────────────────┘
                                       │
                     ┌─────────────────▼────────────────────────┐
                     │        XGBoost Binary Classifier          │
                     │     models/failsafe_xgb_model.pkl         │
                     │     models/failsafe_scaler.pkl            │
                     └─────────────────┬────────────────────────┘
                                       │
                     ┌─────────────────▼────────────────────────┐
                     │         SHAP TreeExplainer                │
                     │         src/explain.py                    │
                     │  → Top 3 risk drivers per student         │
                     │  → Demographic features blocked           │
                     └─────────────────┬────────────────────────┘
                                       │
                     ┌─────────────────▼────────────────────────┐
                     │      Prescriptive Intervention Engine     │
                     │         src/rules.py                      │
                     │  → Maps each driver → specific action     │
                     └─────────────────┬────────────────────────┘
                                       │
                     ┌─────────────────▼────────────────────────┐
                     │         Structured JSON Response          │
                     │  risk_probability · risk_tier · drivers   │
                     │  interventions · behavioural context      │
                     └─────────────────┬────────────────────────┘
                                       │
                     ┌─────────────────▼────────────────────────┐
                     │         React + Tailwind v4 Dashboard     │
                     │  Risk cards · Tier filters · Search       │
                     │  Dark/Light mode · Animated UI            │
                     └──────────────────────────────────────────┘
```

---

## ✨ Features

### 🧠 Machine Learning Core
- **XGBoost binary classifier** trained on the UCI Student Performance dataset
- **Class imbalance handling** via `scale_pos_weight` — no oversampling hacks
- **StandardScaler** for robust feature normalization
- **Three temporal data splits** (`before_G1`, `after_G1`, `after_G2`) for model design validation
- Trained to predict **failure risk** (`G3 < 10`) rather than raw grade regression

### 🔍 SHAP-Powered Explainability
- Per-student **SHAP value decomposition** using `TreeExplainer`
- Only **positive SHAP values** (pushing toward failure) are surfaced — noise is suppressed
- **Demographic features are programmatically blocked** from appearing as drivers
- Returns top 3 most impactful risk factors with human-readable labels

### 📋 Prescriptive Intervention Engine
- **35+ feature-mapped intervention rules** covering academic, lifestyle, family, and logistical domains
- Each intervention is:
  - Categorized (ACADEMIC / HABIT / LIFESTYLE / FAMILY / SUPPORT / WELLBEING / LOGISTICAL / RESOURCE)
  - Specific and actionable — not generic advice
  - Written from an academic advisor's perspective
- Falls back to a sensible generic action if a new feature is encountered

### 🌐 REST API (FastAPI)
- Single `POST /predict` endpoint — upload a CSV, receive a full intelligence report
- Handles messy real-world CSVs (quote-wrapped values, inconsistent separators)
- Validates file type (`.csv` only) with descriptive HTTP error codes
- Full CORS support for frontend integration
- Auto-generates interactive documentation at `/docs`

### 🖥️ React Dashboard
- **Drag-and-drop CSV upload** with real-time file name and size preview
- **Four live stat counters**: Total, Critical, Alert, On Track
- **Clickable tier filters** to isolate risk groups
- **Student search** by ID or Roll Number
- **StudentCard component** with animated risk progress bar, top risk drivers as tags, and full AI action plan
- **Dark / Light mode** toggle with smooth CSS transitions and `localStorage` persistence
- Built with **React 19** + **Vite 8** + **Tailwind CSS v4**

---

## 🛠️ Tech Stack

### Backend
| Component | Technology |
|---|---|
| API Framework | FastAPI 2.0 |
| ML Model | XGBoost (binary:logistic) |
| Explainability | SHAP (TreeExplainer) |
| Data Processing | Pandas, NumPy |
| Preprocessing | Scikit-learn (StandardScaler) |
| Model Persistence | Joblib (.pkl) |
| Server | Uvicorn (ASGI) |

### Frontend
| Component | Technology |
|---|---|
| Framework | React 19 |
| Build Tool | Vite 8 |
| Styling | Tailwind CSS v4 |
| Icons | Lucide React |
| State Management | React Hooks (useState, useEffect, useRef, useCallback) |

### Development & Data
| Component | Technology |
|---|---|
| EDA & Modeling | Jupyter Notebook |
| Visualization | Matplotlib, Seaborn |
| Dataset | UCI ML Repository — Student Performance |
| Language | Python 3.10+ |

---

## 📊 Dataset

**Source:** [UCI Machine Learning Repository — Student Performance Data Set](https://archive.ics.uci.edu/ml/datasets/Student+Performance)
**Citation:** P. Cortez and A. Silva. "Using Data Mining to Predict Secondary School Student Performance." 2008.

### Dataset Overview

| Property | Detail |
|---|---|
| Subjects Covered | Mathematics (`student-mat.csv`), Portuguese (`student-por.csv`) |
| Total Records | ~1,044 (combined, post-deduplication) |
| Features | 30 input attributes + 3 grade columns (G1, G2, G3) |
| Target Variable | Binary: `Risk = 1` if `G3 < 10` (fail), else `0` |

### Key Feature Categories

| Category | Features |
|---|---|
| **Academic Behavior** | `studytime`, `failures`, `absences` |
| **Social & Lifestyle** | `goout`, `Dalc` (workday alcohol), `Walc` (weekend alcohol), `romantic` |
| **Support Network** | `schoolsup`, `famsup`, `higher`, `paid`, `internet` |
| **Family Context** | `Medu`, `Fedu`, `Mjob`, `Fjob`, `famrel`, `Pstatus`, `guardian` |
| **Logistical** | `traveltime`, `health`, `freetime`, `nursery`, `activities` |
| **Excluded (Demographic Bias)** | `school`, `sex`, `age`, `address` *(removed by design)* |

### Engineered Features

Two composite features are derived during preprocessing to capture multi-dimensional risk signals:

```python
# Composite support score: school support + family support + higher education aspiration
support_index = schoolsup + famsup + higher

# Risk behaviour index: social exposure + alcohol consumption
risk_behavior  = Dalc + Walc + goout
```

### Temporal Data Strategy

Three CSV test splits reflect real academic lifecycle timing:

| Split | Features Available | Use Case |
|---|---|---|
| `before_G1.csv` | Demographics + behaviours only | Semester-start early warning |
| `after_G1.csv` | + First period grade (G1) | Mid-semester check |
| `after_G2.csv` | + G1 and G2 | Late-semester prediction |

This design mirrors how academic intervention systems would be triggered in practice.

---

## 🤖 ML Pipeline

### 1. Data Loading & Merging (`src/data_prep.py`)
```python
df_mat['subject'] = 'Math'
df_por['subject'] = 'Portuguese'
df = pd.concat([df_mat, df_por], ignore_index=True)
```
Both subjects are merged into a single dataset with a `subject` feature, allowing the model to learn cross-subject patterns.

### 2. Target Engineering
```python
df['Risk'] = (pd.to_numeric(df['G3']) < 10).astype(int)
df = df.drop(columns=['G3'])
```
Converts the continuous grade into a binary failure indicator. `G3` is dropped to prevent direct target leakage.

> **Design Decision**: `G1` and `G2` are also dropped in the `before_G1` scenario to build a genuinely *early* warning model. The trained model (`failsafe_xgb_model.pkl`) operates without period grades — making it deployable at semester start.

### 3. Preprocessing
- **Binary mapping**: Yes/No columns → 1/0
- **Demographic removal**: `school`, `sex`, `address`, `age` dropped before encoding
- **One-hot encoding** via `pd.get_dummies(drop_first=True)`
- **Feature alignment**: API dynamically aligns inference columns to training schema

### 4. Model Training (`src/model.py`)
```python
model = xgb.XGBClassifier(
    objective='binary:logistic',
    scale_pos_weight=ratio,   # handles class imbalance
    n_estimators=200,
    max_depth=3,              # shallow trees prevent overfitting on small data
    learning_rate=0.01,
    subsample=0.7,
    random_state=42
)
```

**Why XGBoost?**
- Superior performance on small, tabular, mixed-type datasets
- Native handling of feature interactions
- Fast inference suitable for batch API predictions
- Compatible with SHAP's `TreeExplainer` for exact Shapley values

### 5. Artifact Persistence
All model artifacts are saved to `models/`:
- `failsafe_xgb_model.pkl` — the trained classifier
- `failsafe_scaler.pkl` — the fitted StandardScaler
- `model_features.pkl` — ordered list of training feature names (ensures inference alignment)

---

## 📈 Risk Scoring & Tiers

The API returns a `risk_probability` (0–100%) for every student, classified into three actionable tiers:

| Tier | Threshold | Meaning | Educator Action |
|---|---|---|---|
| 🔴 **Critical Intervention** | ≥ 65% | High probability of failure | Immediate escalation, structured remediation |
| 🟡 **Academic Alert** | 40–64% | Elevated risk, early warning | Proactive check-in, targeted support |
| 🟢 **On Track** | < 40% | Low failure risk | Monitor, no immediate action required |

These thresholds are calibrated for the educational domain, where false negatives (missing an at-risk student) carry higher cost than false positives.

---

## 🔬 SHAP Explainability

FAILSAFE uses **SHAP (SHapley Additive exPlanations)** to provide per-student, model-agnostic explanations.

```python
# src/explain.py
shap_vals = explainer.shap_values(student_features)[0]

# Only surface risk-increasing factors (positive SHAP impact)
if shap_vals[i] > 0:
    impacts.append({"feature": feature, "label": get_label(feature), "impact": round(float(shap_vals[i]), 4)})
```

**Key design choices:**
1. **Positive-only filter**: Only features *pushing the student toward failure* are shown — educators see drivers, not noise.
2. **Demographic block**: `school`, `sex`, `age`, `address` and their encoded variants are programmatically excluded from surfacing — even if present in the model, they will never appear in outputs.
3. **Human-readable labels**: All internal feature names are mapped to plain English via `FEATURE_LABELS` in `src/rules.py` (e.g., `Walc` → `"Weekend Alcohol Consumption"`).
4. **Top 3 drivers**: The three highest-impact risk factors are returned — actionable precision, not information overload.

---

## 🎯 Prescriptive Intervention Engine

The intervention engine (`src/rules.py`) transforms SHAP drivers into **specific, actionable, educator-ready guidance**.

Every feature maps to a structured intervention string with:
- A **category tag** (e.g., `ACADEMIC:`, `LIFESTYLE:`, `FAMILY:`)
- A **context sentence** explaining why the feature matters
- A concrete **ACTION →** directive

### Sample Interventions

```
failures →
  ACADEMIC: Student has prior class failure(s) — the strongest single predictor
  of future failure. ACTION → Mandate immediate enrollment in a structured peer-
  tutoring or remedial support programme. Schedule bi-weekly check-ins with the
  form tutor to monitor progress.

absences →
  ATTENDANCE: High number of school absences recorded. ACTION → Trigger an
  automated academic advisor check-in within 48 hours. Draft an Attendance
  Improvement Contract and notify the guardian.

risk_behavior →
  LIFESTYLE: Elevated risk behaviour index (alcohol consumption + social going-
  out frequency). ACTION → Schedule a confidential wellness counselling session.
  Introduce student to structured after-school activities as a positive alternative.
```

**Coverage**: 35+ features fully mapped, with a sensible fallback for any unmapped feature:
```python
return INTERVENTION_MAP.get(
    feature_name,
    f"GENERAL: Discuss the impact of '{get_label(feature_name)}' during the next advising session."
)
```

---

## ⚖️ Ethical Design: Bias-Free by Architecture

FAILSAFE was deliberately architected to prevent demographic bias from influencing risk predictions or intervention recommendations.

### What Was Excluded and Why

| Feature | Type | Reason for Exclusion |
|---|---|---|
| `sex` | Identity | Not a behavioural predictor; cannot be acted upon |
| `age` | Identity | Correlated with grade level, not individual risk |
| `school` | Identity | Institutional bias; not an actionable student attribute |
| `address` | Socioeconomic proxy | Introduces geographic/socioeconomic bias |

These features are removed in **two layers**:
1. **Training time** (`src/data_prep.py`): Excluded before model sees any data
2. **Inference time** (`app/api.py`): Dropped from the uploaded CSV before feature engineering
3. **SHAP output** (`src/explain.py`): Blocked from surfacing even if residually encoded

> This ensures FAILSAFE generates the same risk assessment for students of different backgrounds with identical behavioural profiles — a critical property for deployment in any real educational institution.

---

## 🌐 API Reference

**Base URL:** `http://localhost:8000`

Interactive documentation auto-generated at: [`http://localhost:8000/docs`](http://localhost:8000/docs)

---

### `POST /predict`

Accepts a student dataset CSV file and returns a complete risk intelligence report.

**Request**
```
Content-Type: multipart/form-data
Body: file=<student_data.csv>
```

**CSV Format** (semicolon-delimited, matching UCI student dataset schema):
```
school; sex; age; address; famsize; Pstatus; Medu; Fedu; Mjob; Fjob; reason; guardian;
traveltime; studytime; failures; schoolsup; famsup; paid; activities; nursery; higher;
internet; romantic; famrel; freetime; goout; Dalc; Walc; health; absences; subject
```

**Response (200 OK)**
```json
{
  "status": "success",
  "data": [
    {
      "student_id": 0,
      "context": {
        "absences": 8,
        "failures": 1,
        "studytime": 1,
        "studytime_label": "<2 hrs/week",
        "goout": 5,
        "dalc": 5,
        "walc": 5,
        "subject": "Portuguese"
      },
      "risk_probability": 78.4,
      "risk_tier": "Critical Intervention",
      "top_drivers": [
        {
          "feature": "failures",
          "label": "Prior Class Failures",
          "impact": 0.4821
        },
        {
          "feature": "risk_behavior",
          "label": "Risk Behaviour Index (Alcohol + Social)",
          "impact": 0.2914
        },
        {
          "feature": "studytime",
          "label": "Weekly Study Time",
          "impact": 0.1337
        }
      ],
      "interventions": [
        {
          "trigger": "failures",
          "label": "Prior Class Failures",
          "action": "ACADEMIC: Student has prior class failure(s)..."
        }
      ]
    }
  ]
}
```

**Error Responses**
| Status | Condition |
|---|---|
| `400 Bad Request` | File is not a `.csv` |
| `500 Internal Server Error` | Model artifact not found or corrupt |

---

## 🖥️ Frontend

The FAILSAFE dashboard is a standalone **React 19 + Vite 8** single-page application styled with **Tailwind CSS v4** (OKLCH color system).

### Interface Sections

**1. Hero Header**
- Bold typographic `FAILSAFE` wordmark with gradient fade
- Subtitle: *"Advanced Early Student Risk Detection & Intelligence Engine"*

**2. Data Acquisition Panel**
- Drag-and-drop / click-to-browse CSV upload zone
- Live file name and size display on selection
- "Execute AI Analysis" button triggers the backend call

**3. Live Stat Counters (Filterable)**
Four stat cards that double as filter buttons:
- Total Managed, Critical Priority, Early Alert, Stable/On Track

**4. Intelligence Report Grid**
Responsive card grid (1 → 2 → 3 → 4 columns) of `StudentCard` components, each showing:
- Student ID + Roll Number (`R-{1000 + id}`)
- Risk tier badge with colour-coded icon
- Animated risk probability progress bar
- Top risk driver tags with SHAP impact scores
- Full AI Action Plan (all intervention text)

**5. Search**
Real-time filter by Student ID or Roll Number.

**6. Dark/Light Mode**
Toggle button persists theme preference in `localStorage`.

### Design System
- **OKLCH colour palette** — perceptually uniform, accessible
- **Apple system font stack** (`-apple-system`, `SF Pro Display`, `Helvetica Neue`)
- **`fade-up` animation** on card mount with staggered delays
- **`theme-transition`** class for smooth background/foreground colour interpolation

---

## 📁 Project Structure

```
FailSafe/
├── app/
│   ├── __init__.py
│   ├── api.py              # FastAPI app — prediction endpoint & full inference pipeline
│   └── main.py             # Uvicorn entry point
│
├── src/
│   ├── __init__.py
│   ├── data_prep.py        # Data loading, cleaning, feature engineering, train/test split
│   ├── model.py            # XGBoost training pipeline — produces model artifacts
│   ├── explain.py          # SHAP TreeExplainer — per-student top risk driver extraction
│   └── rules.py            # Feature label map + 35+ intervention action rules
│
├── frontend/
│   ├── src/
│   │   ├── App.jsx         # Main application shell — state, upload, filtering, layout
│   │   ├── App.css         # Component-scoped styles
│   │   ├── index.css       # Global Tailwind v4 design system + OKLCH tokens
│   │   ├── main.jsx        # React root mount
│   │   └── components/
│   │       ├── StudentCard.jsx   # Per-student risk card with tier badge, drivers, actions
│   │       └── AppSidebar.jsx    # Sidebar navigation component
│   ├── package.json
│   └── vite.config.js
│
├── models/
│   ├── failsafe_xgb_model.pkl   # Trained XGBoost classifier
│   ├── failsafe_scaler.pkl      # Fitted StandardScaler
│   └── model_features.pkl       # Training feature name list (for inference alignment)
│
├── data/
│   ├── raw/
│   │   ├── student-mat.csv      # UCI Mathematics dataset
│   │   ├── student-por.csv      # UCI Portuguese dataset
│   │   ├── student-merge.R      # R script for finding overlapping students
│   │   └── student.txt          # Official UCI attribute descriptions
│   └── test/
│       ├── before_G1.csv        # Test CSV: semester-start scenario (no grades)
│       ├── after_G1.csv         # Test CSV: mid-semester (with G1)
│       └── after_G2.csv         # Test CSV: late-semester (with G1, G2)
│
├── notebooks/
│   ├── 01_EDA.ipynb             # Full exploratory data analysis — distributions, correlations, feature importance
│   └── 02_DataProcessing.ipynb      # Data cleaning, feature engineering, and model training notebook
├── test_system.py               # End-to-end API validation suite (happy path + edge cases)
├── requirements.txt             # Python dependencies
└── README.md
```

---

## 🚀 Getting Started

### Prerequisites

- Python 3.10+
- Node.js 18+
- npm 9+

### 1. Clone the Repository

```bash
git clone https://github.com/Anuroop128/FAILSAFE-Intelligence.git
cd FAILSAFE-Intelligence
```

### 2. Set Up the Python Backend

```bash
# Create and activate virtual environment
python -m venv .venv

# Windows
.venv\Scripts\activate

# macOS / Linux
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 3. (Optional) Retrain the Model

The repository ships with pre-trained model artifacts in `models/`. To retrain from scratch:

```bash
cd src
python model.py
```

### 4. Start the API Server

```bash
# From the project root
python app/main.py
```

The FastAPI server starts at `http://localhost:8000`.
Interactive API docs: [`http://localhost:8000/docs`](http://localhost:8000/docs)

### 5. Set Up and Start the Frontend

```bash
cd frontend
npm install
npm run dev
```

The React dashboard opens at `http://localhost:5173`.

### 6. Run a Prediction

Upload one of the test CSVs from `data/test/` via the dashboard, or call the API directly:

```bash
curl -X POST "http://localhost:8000/predict" \
  -F "file=@data/test/before_G1.csv"
```

---

## 🧪 Testing

### Automated API Validation

`test_system.py` provides an end-to-end validation suite against the running API:

```bash
# Ensure the API is running first (python app/main.py)
python test_system.py
```

**Test Cases:**

| # | Scenario | Expected Outcome |
|---|---|---|
| 1 | Valid CSV upload (`student-mat.csv`) | `200 OK`, all students processed, SHAP + interventions populated |
| 2 | Invalid file type (`.txt`) | `400 Bad Request`, file rejected with descriptive error |

**Expected Output:**
```
🧪 INITIATING SYSTEM VALIDATION SUITE...

▶️ TEST 1: Submitting valid CSV...
✅ PASS: API returned 200 OK.
✅ PASS: Processed 395 students successfully.
✅ PASS: SHAP Explainability and Intervention Engine are firing correctly.

▶️ TEST 2: Submitting an invalid file type (.txt)...
✅ PASS: System correctly rejected the invalid file type with a 400 error.

🏁 VALIDATION COMPLETE.
```

### Exploratory Data Analysis

The full EDA is documented in `notebooks/01_EDA.ipynb`, covering:
- Grade distributions (G1, G2, G3) and class imbalance analysis
- Correlation heatmaps
- Feature-by-feature risk analysis (failures, absences, alcohol, study time)
- SHAP global feature importance plots

---

## 🏆 Design Philosophy

FAILSAFE was built on three non-negotiable principles:

**1. Real-world deployability over academic novelty**
Every design decision — from the temporal data splits to the CORS-enabled API — is made to produce a system that could be handed to a school administrator today.

**2. Explainability is not optional**
A black-box risk score is dangerous in an educational context. Every prediction surfaces its top drivers in plain English, attached to a concrete action.

**3. Fairness by architecture, not by policy**
Demographic features are not "controlled for" after the fact — they are structurally absent from the entire pipeline, from training data to SHAP output. The system cannot discriminate because it literally does not see the information required to do so.

---

## 👤 Author

**Gugaloth Anuroop Singh**

Built as a portfolio-grade end-to-end ML system demonstrating:
- Production ML pipeline design (data → features → model → API)
- Responsible AI principles (bias mitigation, explainability)
- Full-stack development (FastAPI backend + React frontend)
- Real-world educational domain knowledge

---

<div align="center">

**FAILSAFE Intelligence v1.2**


</div>
