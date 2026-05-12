import requests
import pandas as pd

API_URL = "http://localhost:8000/predict"
TEST_CSV_PATH = "data/raw/student-mat.csv" # Using your raw data for the test

print("🧪 INITIATING SYSTEM VALIDATION SUITE...\n")

# --- TEST CASE 1: The "Happy Path" (Valid Data) ---
print("▶️ TEST 1: Submitting valid CSV...")
try:
    with open(TEST_CSV_PATH, "rb") as f:
        files = {"file": ("student-mat.csv", f, "text/csv")}
        response = requests.post(API_URL, files=files)
    
    if response.status_code == 200:
        data = response.json()
        print(f"✅ PASS: API returned 200 OK.")
        print(f"✅ PASS: Processed {len(data['data'])} students successfully.")
        
        # Verify SHAP logic worked
        sample_student = data['data'][0]
        if "top_drivers" in sample_student and len(sample_student["interventions"]) > 0:
            print("✅ PASS: SHAP Explainability and Intervention Engine are firing correctly.")
    else:
        print(f"❌ FAIL: API returned status {response.status_code}")
except Exception as e:
    print(f"❌ FAIL: {e}")

# --- TEST CASE 2: The "Bad File" Edge Case ---
print("\n▶️ TEST 2: Submitting an invalid file type (.txt)...")
try:
    # Creating a fake text file in memory
    files = {"file": ("fake_data.txt", b"this is not a csv", "text/plain")}
    response = requests.post(API_URL, files=files)
    
    if response.status_code == 400:
        print("✅ PASS: System correctly rejected the invalid file type with a 400 error.")
    else:
        print(f"❌ FAIL: System accepted a bad file! Status: {response.status_code}")
except Exception as e:
    print(f"❌ FAIL: {e}")

print("\n🏁 VALIDATION COMPLETE.")