import numpy as np
import joblib
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Load Models
rf = joblib.load(os.path.join(BASE_DIR, "models", "random_forest.pkl"))
pca = joblib.load(os.path.join(BASE_DIR, "models", "pca.pkl"))
scaler = joblib.load(os.path.join(BASE_DIR, "models", "scaler.pkl"))

# Sample Input
sample_url_features = np.array([[
    23,16,0,0.8,3,1,0,0,0,18,
    0.7,2,0.1,0,0,0,0,0.1,1,0,0,0
]])

# Scale
scaled = scaler.transform(sample_url_features)

# PCA
pca_features = pca.transform(scaled)

# Prediction
prediction = rf.predict(pca_features)[0]

# Probability
probability = rf.predict_proba(pca_features)

confidence = max(probability[0]) * 100

# Output
if prediction == 1:
    print("\nPrediction : PHISHING")
else:
    print("\nPrediction : LEGITIMATE")

print("Confidence Score :", round(confidence,2), "%")