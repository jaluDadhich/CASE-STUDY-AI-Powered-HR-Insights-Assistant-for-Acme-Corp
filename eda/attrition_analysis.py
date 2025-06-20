import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import os

sns.set_theme(style="whitegrid")
plt.rcParams["figure.figsize"] = (10, 6)

def load_data(csv_path: str) -> pd.DataFrame:
    return pd.read_csv(csv_path)

def plot_attrition_by_column(df, column, top_n=None):
    attrition_counts = df[df['Attrition'] == 'Yes'][column].value_counts(normalize=True)
    if top_n:
        attrition_counts = attrition_counts.head(top_n)
    
    sns.barplot(x=attrition_counts.index, y=attrition_counts.values)
    plt.title(f'Attrition Rate by {column}')
    plt.ylabel('Proportion of Attrition')
    plt.xlabel(column)
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

def boxplot_by_attrition(df, column):
    sns.boxplot(x='Attrition', y=column, data=df)
    plt.title(f'{column} vs Attrition')
    plt.tight_layout()
    plt.show()

def perform_eda(df):
    # Attrition by Department
    plot_attrition_by_column(df, 'Department')

    # Attrition by Job Role
    plot_attrition_by_column(df, 'JobRole', top_n=10)

    # Attrition by Performance Rating
    plot_attrition_by_column(df, 'PerformanceRating')

    # Attrition by Job Satisfaction
    plot_attrition_by_column(df, 'JobSatisfaction')

    # Attrition by Work-Life Balance
    plot_attrition_by_column(df, 'WorkLifeBalance')

    # Attrition by OverTime
    plot_attrition_by_column(df, 'OverTime')

    # Years at Company vs Attrition
    boxplot_by_attrition(df, 'YearsAtCompany')

    # Monthly Income vs Attrition
    boxplot_by_attrition(df, 'MonthlyIncome')

def generate_insights(df):
    print("Actionable Insights:")
    
    # 1. Overtime is a strong predictor
    overtime_attrition = df.groupby('OverTime')['Attrition'].value_counts(normalize=True).unstack().fillna(0)
    print(f"Employees with Overtime have {round(overtime_attrition.loc['Yes']['Yes']*100, 2)}% attrition rate vs {round(overtime_attrition.loc['No']['Yes']*100, 2)}% without overtime")

    # 2. Low Work-Life Balance linked to high attrition
    wlb = df[df['Attrition'] == 'Yes']['WorkLifeBalance'].value_counts(normalize=True)
    top_wlb = wlb.idxmax()
    print(f"Most employees who left had a Work-Life Balance rating of {top_wlb} (rating scale 1–4).")

    # 3. Job Roles with high attrition
    high_attr_roles = df[df['Attrition'] == 'Yes']['JobRole'].value_counts().head(3)
    print(f"Top roles with highest attrition: {', '.join(high_attr_roles.index.tolist())}")

def main():
    file_path = "employee_attrition.csv"  # Replace with your actual path if needed
    if not os.path.exists(file_path):
        print(f" File not found: {file_path}")
        return

    df = load_data(file_path)
    perform_eda(df)
    generate_insights(df)

if __name__ == "__main__":
    main()
