import xgboost as xgb
import joblib
import os
from data_prep import load_and_prep_data

# 🌟 DYNAMIC PATH RESOLUTION
# This finds exactly where model.py is (src/), and goes up one level to the root folder
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def train_pipeline():
    print("🚀 Starting Model Training Pipeline...")
    
    # 1. Get Data using absolute dynamic paths
    mat_path = os.path.join(ROOT_DIR, 'data', 'raw', 'student-mat.csv')
    por_path = os.path.join(ROOT_DIR, 'data', 'raw', 'student-por.csv')
    
    X_train, X_test, y_train, y_test, scaler, feature_names = load_and_prep_data(mat_path, por_path)
    
    # 2. Setup XGBoost
    ratio = float(y_train.value_counts()[0]) / y_train.value_counts()[1]
    
    model = xgb.XGBClassifier(
        objective='binary:logistic',
        scale_pos_weight=ratio,
        n_estimators=200,
        max_depth=3,
        learning_rate=0.01,
        subsample=0.7,
        random_state=42
    )
    
    # 3. Train
    print("🧠 Training XGBoost Model...")
    model.fit(X_train, y_train)
    
    # 4. Save Artifacts dynamically to the correct folder
    models_dir = os.path.join(ROOT_DIR, 'models')
    os.makedirs(models_dir, exist_ok=True)
    
    joblib.dump(model, os.path.join(models_dir, 'failsafe_xgb_model.pkl'))
    joblib.dump(scaler, os.path.join(models_dir, 'failsafe_scaler.pkl'))
    joblib.dump(feature_names, os.path.join(models_dir, 'model_features.pkl'))
    
    print("✅ Pipeline Success! Artifacts saved to /models.")

if __name__ == "__main__":
    train_pipeline()