import pandas as pd
import numpy as np
import missingno as msno
import matplotlib.pyplot as plt


df = pd.read_csv('dataset/titanic/merged_titanic.csv')
df = df.drop_duplicates()
print(df.isnull().sum())
print(df.shape)
print(df.head())

#validate the data types
print(df.dtypes)
numeric_cols = df.select_dtypes(include=['int64', 'float64']).columns.tolist()
invalid_entries = []
for col in numeric_cols:
    converted = pd.to_numeric(df[col], errors='coerce')
    mask = converted.isna() & df[col].notna()
    for idx in df.index[mask]:
        invalid_entries.append((idx, col, df.at[idx, col]))
if invalid_entries:
    print("Invalid entries:")
    for idx, col, val in invalid_entries:
        print(f"  - row {idx}, column '{col}': value = {val}")
else:
    print("No invalid entries found in numeric columns.")

#validate column Sex
print(df['Sex'].value_counts())

# use missingno to visualize the missing data
plt.figure(figsize=(10, 6))
msno.bar(df)
plt.title("Missing Data")
plt.subplots_adjust(top=0.8, bottom=0.2)
# plt.show()

# fill missing values at column Age with the median value
df['Age'] = df['Age'].fillna(df['Age'].median())

# fill missing values at column Fare with the median value
df['Fare'] = df['Fare'].fillna(df['Fare'].median())

# fill missing values at column Cabin with the most frequent value
print(df['Cabin'].value_counts())
df['Cabin'] = df['Cabin'].fillna(df['Cabin'].mode()[0])

# fill missing values at column Embarked with the most frequent value
df['Embarked'] = df['Embarked'].fillna(df['Embarked'].mode()[0])


# use missingno to review the missing data
plt.figure(figsize=(10, 6))
msno.bar(df)
plt.title("Missing Data")
plt.subplots_adjust(top=0.8, bottom=0.2)
# plt.show()

# save the cleaned dataset
df.to_csv('dataset/titanic/cleaned_titanic.csv', index=False)
print("\nCleaned data saved to 'dataset/titanic/cleaned_titanic.csv'")
print(df.isnull().sum())


