import pandas as pd
import joblib
import os

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report

# Load Dataset
df = pd.read_excel(
    r"C:\Users\HP\Desktop\Phishing_URL_Detection\dataset\Phishing_URL.xlsx"
)

# Preprocessing
df.drop_duplicates(inplace=True)
df.dropna(inplace=True)

# Features and Label
X = df.drop("label", axis=1)
y = df["label"]

# Scaling
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# PCA
pca = PCA(n_components=10)
X_pca = pca.fit_transform(X_scaled)

# Split
X_train, X_test, y_train, y_test = train_test_split(
    X_pca,
    y,
    test_size=0.2,
    random_state=42
)

# Random Forest
rf = RandomForestClassifier(
    n_estimators=100,
    random_state=42
)

rf.fit(X_train, y_train)

# Prediction
y_pred = rf.predict(X_test)

# Accuracy
accuracy = accuracy_score(y_test, y_pred)

print("\nAccuracy:", round(accuracy * 100, 2), "%")

print("\nClassification Report:")
print(classification_report(y_test, y_pred))

# Save Models
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

joblib.dump(
    rf,
    os.path.join(BASE_DIR, "models", "random_forest.pkl")
)

joblib.dump(
    scaler,
    os.path.join(BASE_DIR, "models", "scaler.pkl")
)

joblib.dump(
    pca,
    os.path.join(BASE_DIR, "models", "pca.pkl")
)

print("\nModel Saved Successfully")