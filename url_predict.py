import os
import joblib
import pandas as pd
from brand_detection import detect_brand
from feature_extractor import extract_features

# Base Directory
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Load Models
rf = joblib.load(os.path.join(BASE_DIR, "models", "random_forest.pkl"))
scaler = joblib.load(os.path.join(BASE_DIR, "models", "scaler.pkl"))
pca = joblib.load(os.path.join(BASE_DIR, "models", "pca.pkl"))

# URL Input
url = input("Enter URL: ")

# Extract Features
features = extract_features(url)

# Convert to DataFrame
df = pd.DataFrame([features])

# Scale
scaled = scaler.transform(df)

# PCA
pca_features = pca.transform(scaled)

# Prediction
prediction = rf.predict(pca_features)[0]

brand = detect_brand(url)

if brand:
    print("\nBrand Detected :", brand)
    print("Potential Brand Impersonation : YES")

# Probability
probabilities = rf.predict_proba(pca_features)[0]

confidence = max(probabilities) * 100

# Risk Score
risk_score = probabilities[1] * 100

# Output
print("\n----------------------------")

if prediction == 1:

    print("Prediction : PHISHING")

    print("Risk Score :", round(risk_score, 2), "%")

    if risk_score >= 70:
        print("Risk Level : HIGH")
    elif risk_score >= 30:
        print("Risk Level : MEDIUM")
    else:
        print("Risk Level : LOW")

else:

    print("Prediction : LEGITIMATE")

    print("Confidence :", round(confidence, 2), "%")

print("----------------------------")