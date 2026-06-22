import pandas as pd
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
import joblib

# Load Dataset
df = pd.read_excel(
    r"C:\Users\HP\Desktop\Phishing_URL_Detection\dataset\Phishing_URL.xlsx"
)

# Remove duplicates
df.drop_duplicates(inplace=True)

# Remove missing values
df.dropna(inplace=True)

# Features and Label
X = df.drop("label", axis=1)
y = df["label"]

# Standardization
scaler = StandardScaler()

X_scaled = scaler.fit_transform(X)

# PCA

pca = PCA(n_components=10)

X_pca = pca.fit_transform(X_scaled)

print("Original Features :", X.shape[1])
print("Reduced Features :", X_pca.shape[1])

# Save

joblib.dump(pca, "C:\\Users\\HP\\Desktop\\Phishing_URL_Detection\\models\\pca.pkl")
joblib.dump(scaler, "C:\\Users\\HP\\Desktop\\Phishing_URL_Detection\\models\\scaler.pkl")

print("PCA Model Saved")