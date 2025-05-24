import pandas as pd
import numpy as np
import missingno as msno
import matplotlib.pyplot as plt

# === Xử lý dữ liệu ===

def merge_and_clean_data(current_df=None):
    """
    Clean the dataset. Can work with current dataframe (including user changes) 
    or merge from original files.
    
    Args:
        current_df: If provided, clean this dataframe. If None, load and merge from original files.
    
    Returns the cleaned dataframe and saves it to 'dataset/titanic/cleaned.csv'
    """
    
    if current_df is not None:
        print("=== CLEANING CURRENT DATA (including user changes) ===")
        df = current_df.copy()
    else:
        print("=== LOADING AND MERGING FROM ORIGINAL FILES ===")
        # Load the original 3 files
        train_df = pd.read_csv('dataset/titanic/train.csv')
        test_df = pd.read_csv('dataset/titanic/test.csv')
        gender_submission_df = pd.read_csv('dataset/titanic/gender_submission.csv')
        
        # Merge test with gender_submission to add Survived column
        merged_test_df = test_df.merge(gender_submission_df, on="PassengerId", how="left")
        
        # Combine train and test data
        df = pd.concat([train_df, merged_test_df], ignore_index=True)
    
    # Remove duplicates
    df = df.drop_duplicates()
    
    print("=== BEFORE CLEANING ===")
    print("Missing values:")
    print(df.isnull().sum())
    print(f"Dataset shape: {df.shape}")
    
    # Validate data types
    print("\nData types:")
    print(df.dtypes)
    
    # Check for invalid entries in numeric columns
    numeric_cols = df.select_dtypes(include=['int64', 'float64']).columns.tolist()
    invalid_entries = []
    for col in numeric_cols:
        converted = pd.to_numeric(df[col], errors='coerce')
        mask = converted.isna() & df[col].notna()
        for idx in df.index[mask]:
            invalid_entries.append((idx, col, df.at[idx, col]))
    
    if invalid_entries:
        print("Invalid entries found:")
        for idx, col, val in invalid_entries:
            print(f"  - row {idx}, column '{col}': value = {val}")
    else:
        print("No invalid entries found in numeric columns.")
    
    # Validate Sex column
    print("\nSex distribution:")
    print(df['Sex'].value_counts())
    
    # Fill missing values in Age with median
    df['Age'] = df['Age'].fillna(df['Age'].median())
    
    # Fill missing values in Fare with median
    df['Fare'] = df['Fare'].fillna(df['Fare'].median())
    
    # Fill missing values in Cabin with most frequent value
    if df['Cabin'].notna().any():
        most_frequent_cabin = df['Cabin'].mode()[0]
        df['Cabin'] = df['Cabin'].fillna(most_frequent_cabin)
    
    # Fill missing values in Embarked with most frequent value
    if df['Embarked'].notna().any():
        most_frequent_embarked = df['Embarked'].mode()[0]
        df['Embarked'] = df['Embarked'].fillna(most_frequent_embarked)
    
    print("\n=== AFTER CLEANING ===")
    print("Missing values:")
    print(df.isnull().sum())
    print(f"Dataset shape: {df.shape}")
    
    # Save cleaned dataset
    df.to_csv('dataset/titanic/cleaned.csv', index=False)
    print("\nCleaned data saved to 'dataset/titanic/cleaned.csv'")
    
    return df

def load_cleaned_data():
    """
    Load cleaned data from cleaned.csv
    If file doesn't exist, return None
    """
    try:
        df = pd.read_csv('dataset/titanic/cleaned.csv')
        print(f"Loaded cleaned data: {df.shape}")
        return df
    except FileNotFoundError:
        print("cleaned.csv not found. Please run data cleaning first.")
        return None
