import os
import sys
import io
import joblib
import pandas as pd
import shap
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware

# 1. SETUP PATHS
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(BASE_DIR)
if PROJECT_ROOT not in sys.path:
    sys.path.append(PROJECT_ROOT)

# 2. LOCAL IMPORTS (Must be after sys.path update)
from src.rules import get_intervention, get_label
from src.explain import get_top_risk_drivers

# 3. INITIALIZE APP
app = FastAPI(title="FAILSAFE API", version="2.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 4. LOAD MODELS
MODELS_DIR = os.path.join(PROJECT_ROOT, 'models')

try:
    model = joblib.load(os.path.join(MODELS_DIR, 'failsafe_xgb_model.pkl'))
    scaler = joblib.load(os.path.join(MODELS_DIR, 'failsafe_scaler.pkl'))
    expected_features = joblib.load(os.path.join(MODELS_DIR, 'model_features.pkl'))
    explainer = shap.TreeExplainer(model)
except Exception as e:
    print(f"❌ ERROR LOADING MODELS: {e}")
    model = scaler = expected_features = explainer = None

# Demographic columns — not sent to the model, but kept in raw_df for display context only
DEMOGRAPHIC_COLS = ['school', 'sex', 'address', 'age']


@app.post("/predict")
async def predict_risk(file: UploadFile = File(...)):
    if not file.filename.endswith('.csv'):
        raise HTTPException(status_code=400, detail="Only CSV files allowed.")

    contents = await file.read()
    df = pd.read_csv(io.StringIO(contents.decode('utf-8')), sep=r'\s*;\s*', engine='python')

    # ─── Meticulous Cleaning ───────────────────────────────────────────────────
    df.columns = df.columns.str.strip().str.replace('"', '')
    for col in df.select_dtypes(include=['object']).columns:
        df[col] = df[col].astype(str).str.replace('"', '').str.strip()

    raw_df = df.copy()  # Keep raw values for display in response

    # ─── Feature Engineering (Matching Training Pipeline) ─────────────────────
    # 1. Binary Mapping
    binary_cols = ['schoolsup', 'famsup', 'paid', 'activities', 'nursery', 'higher', 'internet', 'romantic']
    for col in binary_cols:
        if col in df.columns:
            df[col] = df[col].map({'yes': 1, 'no': 0}).fillna(0)

    # 2. Derived Features
    df['support_index'] = df.get('schoolsup', pd.Series(0, index=df.index)) + \
                          df.get('famsup', pd.Series(0, index=df.index)) + \
                          df.get('higher', pd.Series(0, index=df.index))
    df['risk_behavior'] = df.get('Dalc', pd.Series(0, index=df.index)) + \
                          df.get('Walc', pd.Series(0, index=df.index)) + \
                          df.get('goout', pd.Series(0, index=df.index))

    # 3. Drop demographic columns — not used by the model
    df = df.drop(columns=DEMOGRAPHIC_COLS, errors='ignore')

    # 4. One-Hot Encoding
    if 'subject' not in df.columns:
        df['subject'] = 'Math'
    df_encoded = pd.get_dummies(df, drop_first=True)

    # 5. Pipeline Alignment — ensure all training features are present
    for col in expected_features:
        if col not in df_encoded.columns:
            df_encoded[col] = 0

    X_app = df_encoded[expected_features]

    # 6. Scaling
    X_scaled = pd.DataFrame(scaler.transform(X_app), columns=expected_features)

    # ─── Predict & Build Response ──────────────────────────────────────────────
    probabilities = model.predict_proba(X_scaled)[:, 1]

    results = []
    for idx in range(len(probabilities)):
        prob = float(probabilities[idx])
        raw_row = raw_df.iloc[idx]

        # Risk Tier Classification
        if prob >= 0.65:
            tier = "Critical Intervention"
        elif prob >= 0.40:
            tier = "Academic Alert"
        else:
            tier = "On Track"

        # SHAP-based top risk drivers (demographic-free, human-labelled)
        top_drivers = get_top_risk_drivers(explainer, X_scaled.iloc[[idx]], expected_features)

        # Map each driver to a specific real-world intervention
        interventions = [
            {
                "trigger": d["feature"],
                "label": d["label"],
                "action": get_intervention(d["feature"])
            }
            for d in top_drivers
        ]

        # ── Student Context (behavioural summary for the frontend) ──────────
        # Raw values that are meaningful and actionable — no demographic info
        def _safe_int(val, default=0):
            try:
                return int(val)
            except (ValueError, TypeError):
                return default

        failures_val   = _safe_int(raw_row.get('failures', 0))
        studytime_val  = _safe_int(raw_row.get('studytime', 0))
        absences_val   = _safe_int(raw_row.get('absences', 0))
        goout_val      = _safe_int(raw_row.get('goout', 0))
        dalc_val       = _safe_int(raw_row.get('Dalc', 0))
        walc_val       = _safe_int(raw_row.get('Walc', 0))

        # Studytime label lookup (UCI encoding)
        studytime_labels = {1: '<2 hrs/week', 2: '2–5 hrs/week', 3: '5–10 hrs/week', 4: '>10 hrs/week'}
        studytime_label = studytime_labels.get(studytime_val, f'Level {studytime_val}')

        results.append({
            "student_id": idx,

            # ── Behavioural Summary (replaces demographic age/school) ────────
            "context": {
                "absences":        absences_val,
                "failures":        failures_val,
                "studytime":       studytime_val,
                "studytime_label": studytime_label,
                "goout":           goout_val,
                "dalc":            dalc_val,
                "walc":            walc_val,
                "subject":         str(raw_row.get('subject', 'Unknown')),
            },

            # ── Risk Assessment ──────────────────────────────────────────────
            "risk_probability": round(prob * 100, 1),
            "risk_tier":        tier,
            "top_drivers":      top_drivers,
            "interventions":    interventions,
        })

    return {"status": "success", "data": results}