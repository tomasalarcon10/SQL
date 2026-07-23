
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

np.random.seed(42)

# ======================================
# CUSTOMER ENERGY DATA
# ======================================

n = 500

cities = [
    "Bogota",
    "Medellin",
    "Cali",
    "Barranquilla",
    "Cartagena"
]

tariffs = [
    "Residential",
    "Commercial",
    "Industrial"
]

complaints = [
    "Billing Error",
    "Power Outage",
    "Voltage Issue",
    "Meter Problem"
]

df = pd.DataFrame({

    "CustomerID": range(1,n+1),

    "City": np.random.choice(cities,n),

    "Tariff": np.random.choice(tariffs,n),

    "Units": np.random.randint(50,1500,n),

    "Bill": np.random.randint(30000,900000,n),

    "Complaint": np.random.choice(complaints,n)

})

# ======================================
# ENERGY CONSUMPTION PYRAMID
# ======================================

usage_bins = pd.cut(
    df["Units"],
    bins=[0,200,500,1000,1500],
    labels=[
        "Low",
        "Medium",
        "High",
        "Extreme"
    ]
)

usage_bins.value_counts().plot(
    kind="bar"
)

plt.title(
    "Consumption Pyramid"
)

plt.tight_layout()

plt.savefig(
    "consumption_pyramid.png"
)

plt.close()

# ======================================
# CITY ENERGY MAP
# ======================================

city_usage = (
    df.groupby("City")["Units"]
    .sum()
)

city_usage.plot(
    kind="bar"
)

plt.title(
    "Energy Demand by City"
)

plt.tight_layout()

plt.savefig(
    "energy_demand_city.png"
)

plt.close()

# ======================================
# BILL DISTRIBUTION
# ======================================

plt.hist(
    df["Bill"],
    bins=25
)

plt.title(
    "Bill Distribution"
)

plt.tight_layout()

plt.savefig(
    "bill_distribution.png"
)

plt.close()

# ======================================
# COMPLAINT ANALYSIS
# ======================================

complaint_counts = (
    df["Complaint"]
    .value_counts()
)

complaint_counts.plot(
    kind="pie",
    autopct="%1.1f%%"
)

plt.ylabel("")

plt.title(
    "Customer Complaints"
)

plt.savefig(
    "complaints_breakdown.png"
)

plt.close()

# ======================================
# TARIFF PROFITABILITY
# ======================================

tariff_rev = (
    df.groupby("Tariff")["Bill"]
    .sum()
)

tariff_rev.plot(
    kind="bar"
)

plt.title(
    "Revenue by Tariff"
)

plt.tight_layout()

plt.savefig(
    "tariff_profitability.png"
)

plt.close()

# ======================================
# SMART GRID DASHBOARD
# ======================================

fig, axs = plt.subplots(
    2,
    2,
    figsize=(14,10)
)

city_usage.plot(
    kind="bar",
    ax=axs[0,0]
)

axs[0,0].set_title(
    "City Demand"
)

tariff_rev.plot(
    kind="bar",
    ax=axs[0,1]
)

axs[0,1].set_title(
    "Tariff Revenue"
)

complaint_counts.plot(
    kind="pie",
    ax=axs[1,0],
    autopct="%1.1f%%"
)

axs[1,0].set_title(
    "Complaints"
)

axs[1,1].hist(
    df["Bill"],
    bins=20
)

axs[1,1].set_title(
    "Bills"
)

plt.tight_layout()

plt.savefig(
    "smart_grid_dashboard.png"
)

plt.close()

print(
    "Smart Electricity Analytics Completed Successfully."
)