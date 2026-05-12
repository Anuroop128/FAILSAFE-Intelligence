import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

def load_and_prep_data(mat_path, por_path):
    """Loads, cleans, and prepares data for early risk prediction."""
    print("⚙️ Loading and merging datasets...")
    df_mat = pd.read_csv(mat_path, sep=';')
    df_por = pd.read_csv(por_path, sep=';')
    
    df_mat['subject'] = 'Math'
    df_por['subject'] = 'Portuguese'
    df = pd.concat([df_mat, df_por], ignore_index=True)
    
    # Clean headers and strings
    df.columns = df.columns.str.strip()
    for col in df.select_dtypes(include=['object']).columns:
        df[col] = df[col].str.replace('"', '').str.strip()
        
    df['G1'] = pd.to_numeric(df['G1'])
    df['G2'] = pd.to_numeric(df['G2'])
    
    # Target Variable (Risk: G3 < 10)
    df['Risk'] = (pd.to_numeric(df['G3']) < 10).astype(int)
    df = df.drop(columns=['G3'])
    
    # Binary Mapping
    binary_cols = ['schoolsup', 'famsup', 'paid', 'activities', 'nursery', 'higher', 'internet', 'romantic']
    for col in binary_cols:
        df[col] = df[col].map({'yes': 1, 'no': 0})
        
    # Feature Engineering
    df['support_index'] = df['schoolsup'] + df['famsup'] + df['higher']
    df['risk_behavior'] = df['Dalc'] + df['Walc'] + df['goout']
    
    # Drop non-causal demographic/identity features before encoding.
    # These features (school, sex, address, age) are not behavioural predictors —
    # they cannot be acted upon by an intervention system and introduce demographic bias.
    # The UCI EDA confirms the real drivers are failures, studytime, absences, alcohol, support, etc.
    DEMOGRAPHIC_COLS = ['school', 'sex', 'address', 'age']
    df = df.drop(columns=DEMOGRAPHIC_COLS, errors='ignore')

    # One-Hot Encoding & Drop Leaky Variables
    df_encoded = pd.get_dummies(df, drop_first=True)
    X = df_encoded.drop(columns=['G1', 'G2', 'Risk'], errors='ignore')
    y = df_encoded['Risk']
    
    # Split & Scale
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)
    
    scaler = StandardScaler()
    X_train_scaled = pd.DataFrame(scaler.fit_transform(X_train), columns=X_train.columns)
    X_test_scaled = pd.DataFrame(scaler.transform(X_test), columns=X_test.columns)
    
    print("✅ Data preparation complete.")
    return X_train_scaled, X_test_scaled, y_train, y_test, scaler, X.columns.tolist()

if __name__ == "__main__":
    import os
    # Test the module if run directly
    ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    test_mat = os.path.join(ROOT_DIR, 'data', 'raw', 'student-mat.csv')
    test_por = os.path.join(ROOT_DIR, 'data', 'raw', 'student-por.csv')
    
    load_and_prep_data(test_mat, test_por)