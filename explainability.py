import shap
import joblib
import os
import pandas as pd

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Load trained model
model = joblib.load(
    os.path.join(BASE_DIR, "models", "rf_explain.pkl")
)

# Create SHAP Explainer
explainer = shap.TreeExplainer(model)

def get_explanation(feature_df):

    shap_values = explainer.shap_values(feature_df)

    return shap_values