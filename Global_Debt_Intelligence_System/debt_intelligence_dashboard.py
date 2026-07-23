
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

np.random.seed(42)

# ======================================
# SYNTHETIC DATA
# ======================================

countries = [
    "Brazil",
    "India",
    "Mexico",
    "Indonesia",
    "Nigeria",
    "Colombia",
    "Argentina",
    "Pakistan",
    "Egypt",
    "Vietnam",
    "Kenya",
    "Turkey"
]

regions = [
    "South America",
    "Asia",
    "North America",
    "Asia",
    "Africa",
    "South America",
    "South America",
    "Asia",
    "Africa",
    "Asia",
    "Africa",
    "Europe"
]

debt = np.random.uniform(
    2_000_000_000,
    30_000_000_000,
    len(countries)
)

forgiven = np.random.uniform(
    1_000_000,
    500_000_000,
    len(countries)
)

df = pd.DataFrame({
    "Country": countries,
    "Region": regions,
    "Debt": debt,
    "Forgiven": forgiven
})

# ======================================
# TOP DEBTORS
# ======================================

top = df.sort_values(
    "Debt",
    ascending=False
)

plt.figure(figsize=(10,6))

plt.barh(
    top["Country"],
    top["Debt"]/1e9
)

plt.title(
    "Most Indebted Countries"
)

plt.xlabel(
    "Debt (Billions USD)"
)

plt.tight_layout()

plt.savefig(
    "top_debtors.png"
)

plt.close()

# ======================================
# DEBT BY REGION
# ======================================

region = (
    df.groupby("Region")["Debt"]
    .sum()/1e9
)

plt.figure(figsize=(8,5))

region.plot(kind="bar")

plt.title(
    "Debt by Region"
)

plt.ylabel(
    "Billions USD"
)

plt.tight_layout()

plt.savefig(
    "debt_by_region.png"
)

plt.close()

# ======================================
# DEBT VS FORGIVEN
# ======================================

plt.figure(figsize=(8,5))

plt.scatter(
    df["Debt"]/1e9,
    df["Forgiven"]/1e6
)

plt.title(
    "Debt vs Forgiveness"
)

plt.xlabel(
    "Debt (Billions USD)"
)

plt.ylabel(
    "Forgiven (Millions USD)"
)

plt.tight_layout()

plt.savefig(
    "debt_vs_forgiveness.png"
)

plt.close()

# ======================================
# DEBT CONCENTRATION
# ======================================

top5 = (
    top.head(5)["Debt"]
    .sum()
)

global_debt = (
    df["Debt"].sum()
)

others = global_debt - top5

plt.figure(figsize=(7,7))

plt.pie(
    [top5, others],
    labels=[
        "Top 5 Countries",
        "Rest of World"
    ],
    autopct="%1.1f%%"
)

plt.title(
    "Global Debt Concentration"
)

plt.savefig(
    "debt_concentration.png"
)

plt.close()

# ======================================
# DEBT STRUCTURE
# ======================================

structure = pd.Series({
    "Long-Term":35,
    "Short-Term":20,
    "Multilateral":18,
    "Bilateral":15,
    "Private":12
})

plt.figure(figsize=(8,5))

structure.plot(kind="bar")

plt.title(
    "Debt Structure"
)

plt.tight_layout()

plt.savefig(
    "debt_structure.png"
)

plt.close()

# ======================================
# EXECUTIVE DASHBOARD
# ======================================

fig, axs = plt.subplots(
    2,
    2,
    figsize=(14,10)
)

top.head(10).plot(
    x="Country",
    y="Debt",
    kind="bar",
    ax=axs[0,0]
)

axs[0,0].set_title(
    "Top Debtors"
)

region.plot(
    kind="bar",
    ax=axs[0,1]
)

axs[0,1].set_title(
    "Debt by Region"
)

axs[1,0].scatter(
    df["Debt"]/1e9,
    df["Forgiven"]/1e6
)

axs[1,0].set_title(
    "Debt vs Forgiveness"
)

axs[1,1].pie(
    [top5,others],
    labels=[
        "Top 5",
        "Others"
    ],
    autopct="%1.1f%%"
)

axs[1,1].set_title(
    "Concentration"
)

plt.tight_layout()

plt.savefig(
    "executive_dashboard.png"
)

plt.close()

# ======================================
# EXPORT REPORTS
# ======================================

df.to_csv(
    "country_debt_report.csv",
    index=False
)

region.to_csv(
    "regional_debt_report.csv"
)

print(
    "Global Debt Intelligence Dashboard Generated Successfully."
)