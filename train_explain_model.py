import pandas as pd
import joblib
import os

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score

# Load Dataset
df = pd.read_excel(
    r"C:\Users\HP\Desktop\Phishing_URL_Detection\dataset\Phishing_URL.xlsx"
)

df.drop_duplicates(inplace=True)
df.dropna(inplace=True)

X = df.drop("label", axis=1)
y = df["label"]

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)

rf_explain = RandomForestClassifier(
    n_estimators=100,
    random_state=42
)

rf_explain.fit(X_train, y_train)

pred = rf_explain.predict(X_test)

print("Accuracy:",
      round(accuracy_score(y_test, pred)*100,2),
      "%")

BASE_DIR = os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))
)

joblib.dump(
    rf_explain,
    os.path.join(
        BASE_DIR,
        "models",
        "rf_explain.pkl"
    )
)

print("Explainability Model Saved")