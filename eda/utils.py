import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import os

# Placeholder function for EDA insights
def load_insights():
    """
    Returns a list of tuples: (title, description, matplotlib figure)
    """
    insights = []

    # Example insight 1
    fig1, ax1 = plt.subplots()
    # Dummy bar plot (replace with actual EDA logic)
    departments = ['Sales', 'R&D', 'HR']
    attrition_rates = [0.25, 0.15, 0.10]
    sns.barplot(x=departments, y=attrition_rates, ax=ax1)
    ax1.set_title("Attrition by Department")
    ax1.set_ylabel("Attrition Rate")
    insights.append((
        "Attrition by Department",
        "Sales department shows the highest attrition rate.",
        fig1
    ))

    # Example insight 2
    fig2, ax2 = plt.subplots()
    work_life = ['Bad', 'Average', 'Good']
    rates = [0.30, 0.20, 0.10]
    sns.barplot(x=work_life, y=rates, ax=ax2)
    ax2.set_title("Attrition by Work-Life Balance")
    ax2.set_ylabel("Attrition Rate")
    insights.append((
        "Attrition by Work-Life Balance",
        "Poor work-life balance is a key attrition driver.",
        fig2
    ))

    return insights
