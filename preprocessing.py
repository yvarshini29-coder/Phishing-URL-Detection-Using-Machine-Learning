import pandas as pd
import numpy as np
from scipy.stats import zscore

def load_data(filepath):

    df = pd.read_excel(filepath)

    print("Original Dataset Shape:", df.shape)

    # Missing Values
    print("\nMissing Values:")
    print(df.isnull().sum())

    # Duplicate Values
    print("\nDuplicate Rows:", df.duplicated().sum())

    # Remove duplicates
    df.drop_duplicates(inplace=True)

    # Remove null values
    df.dropna(inplace=True)

    print("\nShape After Cleaning:", df.shape)

    # Outlier Detection
    numeric_cols = df.select_dtypes(include=np.number)

    if not numeric_cols.empty:

        z_scores = np.abs(zscore(numeric_cols))

        outliers = (z_scores > 3)

        total_outliers = np.sum(outliers)

        print("\nTotal Outlier Values Found:", total_outliers)

        df = df[(z_scores < 3).all(axis=1)]

        print("Shape After Removing Outliers:", df.shape)

    else:
        print("\nNo Numerical Columns Found Yet.")
        print("Outlier Detection will be applied after Feature Extraction.")

    return df


if __name__ == "__main__":

    filepath = r"C:\Users\HP\Desktop\Phishing_URL_Detection\dataset\Phishing_URL.xlsx"

    df = load_data(filepath)

    print("\nFirst 5 Rows:")
    print(df.head())