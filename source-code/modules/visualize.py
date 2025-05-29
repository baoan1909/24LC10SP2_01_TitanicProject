import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import re


def boxplot_show_age_pclass_chart(df):
    sns.boxplot( data=df,x='Pclass', y='Age')
    plt.title("Age Distribution by Passenger Class", color='red')
    plt.xlabel("Passenger Class",color='blue')
    plt.ylabel("Age",color='blue')
    plt.show()


def hist_show_age_chart(df):
    # vẽ histogram độ tuổi
    hist= sns.histplot(data=df, x='Age', hue='Survived', bins=40)
    hist.set_title("Histogram Age with Survived",color='red')
    hist.set_xlabel('Age', color= 'blue')
    hist.set_ylabel('Count', color= 'blue')
    plt.show()


def pie_show_survived_rate_chart(df):
    # Pie chart
    ax = df['Survived'].value_counts().plot.pie(
        autopct='%1.1f%%',         
        labels=['Not_survived', 'Survived'], 
        colors=['brown', 'lightskyblue'], 
        explode=[0.05, 0],         
        startangle=90,            
        shadow=True                
    )
    plt.title('Survival Rate on the Titanic', color= 'red')
    ax.set_ylabel('')
    ax.set_xlabel('')
    texts = ax.texts
    texts[0].set_color('blue')  
    texts[1].set_color('white')
    texts[2].set_color('blue')
    texts[3].set_color('white')
    plt.show()

def subplot_show_survival_chart(df):
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
                ax_i.set_title(f"Figure {i+1}: Survived Rate vs {cols[i]}", color='red')
                ax_i.set_xlabel(cols[i], color='blue')
                ax_i.set_ylabel('count', color='blue')
                ax_i.legend(title='',loc='upper left', labels=['Not Survived','Survived'])
    ax.flat[-1].set_visible(False) 
    plt.tight_layout()
    plt.show()

def count_plot_show_survived_by_family_size(df):
    df['Family_Size'] = df['SibSp'].astype('int') + df['Parch'].astype('int') + 1
    df['Family_Cat'] = pd.cut(df['Family_Size'], bins=[0, 1, 4, 6, 15], labels=['Solo', 'Small', 'Medium', 'Large'])

    cols = ['Family_Size', 'Family_Cat']
    n_rows = 1
    n_cols = 2

    fig, ax = plt.subplots(n_rows, n_cols, figsize=(n_cols*4, n_rows*4))
    for i in range(len(cols)):
        sns.countplot(data=df, x=cols[i], hue='Survived', palette='Blues', ax=ax[i])
        ax[i].set_title(f"Figure {i+1}: Survived Rate vs {cols[i]}", color='red')
        ax[i].set_xlabel(cols[i], color='blue')
        ax[i].set_ylabel('Count', color='blue')
        ax[i].legend(title='', loc='upper right', labels=['Not Survived', 'Survived'])

    plt.tight_layout()
    plt.show()
def countplot_show_sex_with_pclass(df):
    plt.figure(figsize=(10,6))
    sns.boxplot(x="Pclass", y="Age", hue="Sex", data=df)
    plt.title("Age distribution by Sex and Pclass")
    plt.xlabel("Hạng vé (Pclass)")
    plt.ylabel("Tuổi")
    plt.legend(title="Giới tính")
    plt.show()


def boxplot_show_sex_with_embarked(df):
    plt.figure(figsize=(9,6))
    sns.countplot(data=df, x="Embarked", hue="Sex", palette="Set2", dodge=True)
    plt.title("Number of Passengers by Sex and Embarked")
    plt.xlabel("Cảng lên tàu (Embarked)")
    plt.ylabel("Số lượng")
    plt.legend(title="Giới tính")
    plt.show()

def countplot_full(df):
    sns.catplot(
        data=df, kind="count",
        x="Embarked", hue="Sex",
        col="Pclass", palette="Set2",
        height=4, aspect=1
    )
    plt.subplots_adjust(top=0.85)
    plt.suptitle("Number of Passengers by Embarked, Sex and PClass")
    plt.show()
    

