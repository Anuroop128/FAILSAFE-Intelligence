# FAILSAFE Intelligence: Comprehensive Project Report

## 1. Executive Summary
**FAILSAFE** is a production-grade, end-to-end AI system designed to proactively identify students at risk of academic failure. Unlike traditional reactive systems, FAILSAFE utilizes advanced machine learning to provide early warnings, explainable risk drivers, and actionable intervention plans. The system is built on three core pillars: predictive accuracy using XGBoost, transparency through SHAP explainability, and ethical integrity via a demographically-blind architecture.

---

## 2. Technical Approach & Backend Architecture
The backend is the "intelligence engine" of FAILSAFE, engineered for real-world academic deployment.

### A. Data Engineering & Preprocessing
- **Source:** UCI Student Performance Dataset (Math & Portuguese).
- **Target Engineering:** Instead of raw grade regression, FAILSAFE uses a binary classification target: `Risk = 1` if `G3 < 10` (fail), else `0`.
- **Temporal Strategy:** Data is split into three temporal scenarios (`before_G1`, `after_G1`, `after_G2`) to ensure the model can be deployed at the very start of a semester.
- **Feature Engineering:** 
    - `support_index`: Composite score of school support, family support, and higher education aspirations.
    - `risk_behavior`: Composite index of workday alcohol, weekend alcohol, and social frequency.

### B. Machine Learning Pipeline (XGBoost)
FAILSAFE uses an **XGBoost Binary Classifier** (`binary:logistic`) as its core model.
- **Imbalance Handling:** Uses `scale_pos_weight` to address the minority of at-risk students without synthetic oversampling.
- **Robustness:** Incorporates `StandardScaler` for normalization and shallow trees (`max_depth=3`) to prevent overfitting.
- **Alignment:** The API dynamically aligns incoming CSV data to the training schema using `model_features.pkl`.

### C. SHAP Explainability Engine
The system integrates **SHAP (SHapley Additive exPlanations)** via `TreeExplainer` to provide per-student transparency.
- **Positive-Only Filter:** Only surfaces features pushing a student *toward* failure.
- **Driver Extraction:** Returns the top 3 most impactful risk factors.
- **Noise Suppression:** Programmatically suppresses low-impact "noise" features.

### D. Prescriptive Intervention Engine (`src/rules.py`)
This custom-built engine transforms raw ML outputs into educator-ready guidance.
- **Mapping:** Over 35 features are mapped to specific intervention strings.
- **Categorization:** Interventions are tagged as ACADEMIC, LIFESTYLE, WELLBEING, etc.
- **Specific Actions:** Each rule provides a concrete "ACTION ->" directive (e.g., "Draft an Attendance Improvement Contract").

### E. REST API (FastAPI)
- **Endpoint:** `POST /predict` handles multipart CSV uploads.
- **Robustness:** Manages messy CSVs (quote-wrapped, semicolon-delimited) and validates file types.
- **Performance:** Asynchronous processing with Uvicorn; auto-generates interactive Swagger documentation at `/docs`.

---

## 3. Ethical Design: Bias-Free by Architecture
A critical backend mandate is the structural exclusion of demographic bias.
- **Exclusion:** Features like `sex`, `age`, `school`, and `address` are dropped at training, inference, and SHAP output layers.
- **Integrity:** Ensures identical behavioral profiles receive identical risk scores regardless of student background.

---

## 4. Key Metrics & Calibration
- **Risk Tiers:** 
    - **Critical (≥65%)**: Immediate structured remediation.
    - **Alert (40-64%)**: Proactive advisor check-in.
    - **On Track (<40%)**: Low risk, routine monitoring.
- **Optimization:** The system is calibrated for high **Recall**, ensuring that no at-risk student is missed, even if it results in slightly more "false alarms" (alerts).

---

## 5. Future Scope
1. **Longitudinal Tracking:** Database integration to monitor risk trends over multiple semesters.
2. **LMS Connectors:** Direct API integration with Canvas/Moodle for automated data syncing.
3. **Sentiment Analysis:** NLP-based risk detection from advisor notes and student feedback.
4. **Fairness Auditing:** Continuous automated parity checks using tools like AIF360.
5. **Collaborative Case Management:** Multi-user workflows for advisor collaboration.
