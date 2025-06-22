import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import os

def load_insights():
    """
    Load and generate insights from the employee attrition dataset.
    Returns:
        list: A list of tuples containing insight titles, descriptions, and matplotlib figures.
    """

    insights = []
    df = pd.read_csv('employee_attrition.csv')
    df['Attrition_Flag'] = df['Attrition'].map({'Yes': 1, 'No': 0})

    # Overall attrition percentage (pie chart)
    fig1, ax1 = plt.subplots(figsize=(6, 6))
    df['Attrition'].value_counts().plot(kind="pie", autopct='%1.1f%%', colors=["#1f77b4", "#ff7f0e"], startangle=90, ax=ax1)
    ax1.set_title("Employee Attrition Percentage")
    ax1.set_ylabel("")
    insights.append((
        "Overall Attrition Rate",
        "Out of 10,000 employees, 16.15% have left the company due to various reasons.",
        fig1,
        ""
    ))

    # Job Satisfaction
    fig2, ax2 = plt.subplots()
    df[df['Attrition'] == 'Yes']['JobSatisfaction'].value_counts().plot(kind="bar", color=sns.color_palette("Set2"), ax=ax2)
    ax2.set_title("Job Satisfaction of Employees who left the company")
    ax2.set_xlabel("Job Satisfaction")
    ax2.set_ylabel("Count")

    
    insights.append((
        "Factor 1: Low Job Satisfaction of Employees who left",
        "Out of those 16.15% who have left , the majority(75%) have left with the reason of Job Satisfaction being very low ( 1/4).",
        fig2,
        """
        Retention Strategy:
        1. Implement regular one-on-one feedback sessions to understand role-specific dissatisfaction.
        2. Provide clear career progression paths, skill development programs, and internal mobility opportunities.
        3. Redesign low-satisfaction roles by aligning responsibilities with employee strengths and interests.

        """   
    ))

    fig2in, ax2in = plt.subplots(figsize=(8, 6))
    sns.countplot(data=df, x="JobSatisfaction", hue="Attrition", palette="Set2", ax=ax2in)
    ax2in.set_title("Attrition by Job Satisfaction")
    ax2in.set_xlabel("Job Satisfaction")
    ax2in.set_ylabel("Count")
    ax2in.legend(title='Attrition')
    insights.append((
        "Factor 1: Low Job Satisfaction Category with Attrition",
        "Employees with Job Satisfaction = 1 have a 49% attrition rate. All other groups are under 6%.",
        fig2in,
        ""
    ))

    fig3, ax3 = plt.subplots()
    overtime_causing_attrition = df[(df['OverTime'] == 'Yes') & (df['Attrition'] == 'Yes')].shape[0] / df[df['OverTime'] == 'Yes'].shape[0] * 100
    no_overtime = df[(df['OverTime'] == 'No') & (df['Attrition'] == 'Yes')].shape[0] / df[df['OverTime'] == 'No'].shape[0] * 100

    values = [round(overtime_causing_attrition, 1), round(no_overtime, 1)]
    labels = ['Overtime & Attrition', 'No Overtime & Attrition']
    colors = sns.color_palette("Set2")

    ax3.bar(labels, values, color=colors)
    ax3.set_title("Attrition by Overtime")
    ax3.set_ylabel("Attrition Rate (%)")

    insights.append((
        "Factor 2: Overtime",
        "Employees working overtime have a 22.2% attrition rate vs 13.6% without overtime.",
        fig3,
        """
        Retention Strategy:
        1. Introduce workload balancing and enforce maximum working hour policies to prevent burnout.
        2. Offer compensatory time off or flexible work schedules for employees consistently logging overtime.
        3. Invest in automation or staffing solutions in high-overtime roles to reduce dependency on extended hours. 
        """
    ))


    fig3in, ax3in = plt.subplots()
    pd.crosstab(df['OverTime'], df['Attrition']).plot(kind='bar', stacked=True, color=sns.color_palette("Set2"),title='Attrition due to OverTime', ax = ax3in)
    ax3in.set_xlabel("OverTime")
    ax3in.set_ylabel("Count")
    insights.append((
        "Overtime Category with Attrition",
        "Employees working overtime have a 22.2% attrition rate vs 13.6% without overtime.",
        fig3in,
        ""
    ))

    # Work-Life Balance
    ### 3rd Factor. Poor Work-Life Balance Drives Attrition
    ### Employees rating WorkLifeBalance = 1 have 24.1% attrition
    ### Those with rating = 4 have just 12.2% attrition
    ### Recomendation : Improve flexibility, time-off policies.

    fig4, ax4 = plt.subplots(figsize=(8, 5))
    sns.countplot(
        data=df,
        x="WorkLifeBalance",
        hue="Attrition",
        palette="Set2",
        ax=ax4
    )
    ax4.set_title("Attrition by Work-Life Balance")
    ax4.set_xlabel("Work-Life Balance")
    ax4.set_ylabel("Count")
    insights.append((
        "Factor 3: Work-Life Balance",
        "Employees with the worst Work-Life Balance (rating = 1) have over 24% attrition.",
        fig4,
        """
        Retention Strategy:
        1. Promote flexible work arrangements such as hybrid schedules, remote work, or adjustable start/end times.
        2. Encourage a culture where managers respect boundaries outside of core working hours.
        3. Provide wellness initiatives like no-meeting days, mental health days, and access to employee assistance programs.
        """
        
    ))

    # Attrition of different job roles with respect to Department
    fig5, ax5 = plt.subplots(figsize=(10, 6))
    
    job_role_counts = df['JobRole'].value_counts()
    df_attrition = df[df['Attrition'] == 'Yes']
    attrition_percent = (df_attrition['JobRole'].value_counts() / job_role_counts * 100).reindex(df['JobRole'].unique())
   
    # Plot
    attrition_percent.plot(kind="bar", color=sns.color_palette("Set2"), ax=ax5)
    ax5.set_title("Attrition Percentage by Job Role")
    ax5.set_xlabel("Job Role")
    ax5.set_ylabel("Attrition Percentage (%)")
    ax5.tick_params(axis='x', rotation=45)
    plt.tight_layout()

    insights.append((
        "Factor 4: Attrition of different Job Roles across Departments.",
        "Certain roles like Manager show high attrition rates, indicating role-specific risks.",
        fig5,
        """
        Retention Strategy:
        1. Standardize recognition and rewards programs to ensure all roles feel valued, regardless of department.
        2. Offer cross-functional training and upskilling to enhance job satisfaction and internal mobility.
        3. Conduct regular stay interviews to proactively identify role-specific concerns and address them early.        
        """
    ))

    df['Attrition_Flag'] = df['Attrition'].map({'Yes': 1, 'No': 0})
    role_attrition = df.groupby(['Department', 'JobRole'])['Attrition_Flag'].mean().reset_index()
    role_attrition['AttritionRate_%'] = (role_attrition['Attrition_Flag'] * 100).round(2)
    top_roles_by_dept = role_attrition.sort_values(['Department', 'AttritionRate_%'], ascending=[True, False])
    top_attrition_roles = top_roles_by_dept.groupby('Department').first().reset_index()
    top_attrition_roles = top_attrition_roles.drop(columns='Attrition_Flag')
    df_plot = top_attrition_roles.copy()
    df_plot["Dept_Role"] = df_plot["Department"] + " - " + df_plot["JobRole"]

    plt.figure(figsize=(10, 6))
    sns.barplot(data=df_plot, y="Dept_Role", x="AttritionRate_%", palette="Reds_r")
    plt.xlabel("Attrition Rate (%)")
    plt.ylabel("Department & Job Role")
    plt.title("Highest Attrition Role in Each Department")
    plt.tight_layout()
    insights.append((
        "Highest Attrition Role in Each Department",
        "Within each department, different job role with the highest attrition rate in each department, highlighting specific risks.",
        plt.gcf(),  # Use current figure,
        "Retention Strategy: Several startegies can be developed across different departments to address the attrition issue."
    ))

    # Create attrition flag if not already done
    df['Attrition_Flag'] = df['Attrition'].map({'Yes': 1, 'No': 0})

    # Prepare summary
    years_summary = df.groupby('YearsAtCompany')['Attrition_Flag'].mean().reset_index()
    years_summary['AttritionRate'] = years_summary['Attrition_Flag'] * 100

    # Plot using fig, ax
    fig6, ax6 = plt.subplots(figsize=(10, 5))
    sns.lineplot(data=years_summary, x='YearsAtCompany', y='AttritionRate', marker='o', color='red', ax=ax6)
    ax6.set_title("Attrition Rate (%) by Years at Company")
    ax6.set_xlabel("Years at Company")
    ax6.set_ylabel("Attrition Rate (%)")
    ax6.grid(True)
    plt.tight_layout()

    # Add to insights
    insights.append((
        "Factor 5 : Attrition by Years at Company",
        "Attrition is highest during the first 2–3 years of tenure, then gradually declines with long-term retention.",
        fig6,
        """
        Retention Strategy : 
        1. Strengthen onboarding with structured mentoring, realistic job previews, and 30-60-90 day check-ins.
        2. Create early career growth plans with clear milestones, feedback, and internal opportunity visibility.
        3. Build a strong sense of belonging through team integration activities and early recognition of contributions
"""
        
    ))


    return insights
