
import pandas as pd
import matplotlib.pyplot as plt

CSV_PATH = r"IBM_HR_Attrition_Intelligence\WA_Fn-UseC_-HR-Employee-Attrition.csv"

df = pd.read_csv(CSV_PATH)

# =====================================================
# ATTRITION RATE
# =====================================================

attrition = df["Attrition"].value_counts()

plt.figure(figsize=(6,6))
plt.pie(
    attrition.values,
    labels=attrition.index,
    autopct="%1.1f%%"
)
plt.title("Employee Attrition Rate")
plt.savefig("attrition_rate.png")
plt.close()

# =====================================================
# OVERTIME VS ATTRITION
# =====================================================

ot = pd.crosstab(
    df["OverTime"],
    df["Attrition"]
)

ot.plot(kind="bar")

plt.title("Overtime vs Attrition")
plt.tight_layout()
plt.savefig("overtime_vs_attrition.png")
plt.close()

# =====================================================
# INCOME VS ATTRITION
# =====================================================

income = df.groupby(
    "Attrition"
)["MonthlyIncome"].mean()

income.plot(kind="bar")

plt.title("Average Income by Attrition")
plt.ylabel("Monthly Income")

plt.tight_layout()
plt.savefig("income_vs_attrition.png")
plt.close()

# =====================================================
# JOB ROLE ATTRITION
# =====================================================

job_attr = (
    df[df["Attrition"]=="Yes"]
    ["JobRole"]
    .value_counts()
)

job_attr.plot(
    kind="barh"
)

plt.title(
    "Attrition by Job Role"
)

plt.tight_layout()

plt.savefig(
    "jobrole_attrition.png"
)

plt.close()

# =====================================================
# AGE DISTRIBUTION
# =====================================================

plt.figure(figsize=(8,5))

plt.hist(
    df["Age"],
    bins=15
)

plt.title(
    "Age Distribution"
)

plt.tight_layout()

plt.savefig(
    "age_distribution.png"
)

plt.close()

# =====================================================
# SATISFACTION HEATMAP
# =====================================================

heat = pd.crosstab(
    df["JobSatisfaction"],
    df["Attrition"]
)

plt.figure(figsize=(6,4))

plt.imshow(
    heat,
    aspect="auto"
)

plt.xticks(
    range(len(heat.columns)),
    heat.columns
)

plt.yticks(
    range(len(heat.index)),
    heat.index
)

plt.colorbar()

plt.title(
    "Job Satisfaction Heatmap"
)

plt.tight_layout()

plt.savefig(
    "satisfaction_heatmap.png"
)

plt.close()

# =====================================================
# EXECUTIVE DASHBOARD
# =====================================================

fig, axs = plt.subplots(
    2,
    2,
    figsize=(14,10)
)

attrition.plot(
    kind="bar",
    ax=axs[0,0]
)

axs[0,0].set_title(
    "Attrition"
)

income.plot(
    kind="bar",
    ax=axs[0,1]
)

axs[0,1].set_title(
    "Income"
)

job_attr.head(10).plot(
    kind="bar",
    ax=axs[1,0]
)

axs[1,0].set_title(
    "Job Roles"
)

axs[1,1].hist(
    df["Age"],
    bins=15
)

axs[1,1].set_title(
    "Age"
)

plt.tight_layout()

plt.savefig(
    "executive_dashboard.png"
)

plt.close()

print("HR Attrition Analysis Completed Successfully.")