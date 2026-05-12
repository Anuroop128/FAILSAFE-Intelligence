import shap
from src.rules import get_label

# Demographic features that must NEVER appear as risk drivers —
# they are identity markers, not actionable predictors.
DEMOGRAPHIC_FEATURES = {'school', 'sex', 'address', 'age', 'school_MS', 'sex_M', 'address_U'}


def get_top_risk_drivers(explainer, student_features, feature_names, top_n=3):
    """
    Calculates SHAP values for a single student and returns the top N risk factors.

    Only features with a POSITIVE SHAP impact (pushing toward failure risk) are included.
    Demographic identity features are excluded even if present in the model.
    Each driver includes the internal feature name, its human-readable label, and the SHAP impact score.
    """
    shap_vals = explainer.shap_values(student_features)[0]

    impacts = []
    for i, feature in enumerate(feature_names):
        # Skip demographic features — they are non-actionable and bias the output
        if feature in DEMOGRAPHIC_FEATURES:
            continue
        # Only surface features pushing the student TOWARD failure (positive SHAP)
        if shap_vals[i] > 0:
            impacts.append({
                "feature": feature,
                "label": get_label(feature),
                "impact": round(float(shap_vals[i]), 4),
            })

    # Sort by highest risk impact and return top N
    top_drivers = sorted(impacts, key=lambda x: x["impact"], reverse=True)[:top_n]
    return top_drivers