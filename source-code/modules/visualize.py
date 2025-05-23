import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
def show_survival_chart(df):
     # Chuyển các dữ liệu về dạng phân loại   
    features = ["Survived", "Pclass", "Sex", "SibSp", "Parch", "Embarked"]
    def convert_cat(df, features):
        for feature in features:
            df[feature] =  df[feature].astype("category")
    convert_cat(df, features)

    # Vẽ biểu đồ 
    cols = ['Sex', 'Embarked', 'Pclass', 'SibSp', 'Parch']
    n_rows = 2
    n_cols = 3
    fig, ax = plt.subplots(n_rows, n_cols, figsize=(n_cols*3.5, n_rows*3.5))
    for r in range(0, n_rows):
        for c in range(0, n_cols):
            i = r*n_cols +c
            if i < len(cols):
                ax_i = ax[r,c]
                sns.countplot(data=df, x=cols[i], hue='Survived', palette='Blues', ax=ax_i)
                ax_i.set_title(f"Figure {i+1}: Survived Rate vs {cols[i]}")
                ax_i.legend(title='',loc='upper left', labels=['Not Survived','Survived'])
    ax.flat[-1].set_visible(False) #remove last subplot
    plt.tight_layout()
    plt.show()

def show_gender_chart():
    # vẽ biểu đồ pie giới tính
    pass

def show_age_chart(df):
    # vẽ histogram độ tuổi
    hist= sns.histplot(data=df, x='Age', hue='Survived', bins=40, palette='Blues')
    hist.set_title("Histogram Age with Survived")
    plt.show()
   