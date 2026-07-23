
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

np.random.seed(42)

# =====================================
# DRIVER DATA
# =====================================

n = 500

cities = [
    "New York",
    "Chicago",
    "Los Angeles",
    "Miami",
    "Dallas",
    "Houston"
]

incentives = [
    "Signup Bonus",
    "Referral Bonus",
    "Weekend Bonus",
    "Guaranteed Earnings"
]

df = pd.DataFrame({
    "DriverID": range(1,n+1),
    "City": np.random.choice(cities,n),
    "Verified": np.random.choice([0,1],n,p=[0.25,0.75]),
    "Activated": np.random.choice([0,1],n,p=[0.35,0.65]),
    "Trips": np.random.randint(0,120,n),
    "Earnings": np.random.randint(0,5000,n),
    "Incentive": np.random.choice(incentives,n)
})

# =====================================
# FUNNEL
# =====================================

signup = len(df)

verified = len(df[df["Verified"]==1])

activated = len(df[df["Activated"]==1])

active = len(df[df["Trips"]>0])

funnel = pd.Series(
    [signup,verified,activated,active],
    index=[
        "Signed Up",
        "Verified",
        "Activated",
        "Active Drivers"
    ]
)

plt.figure(figsize=(8,5))
funnel.plot(kind="bar")
plt.title("Driver Signup Funnel")
plt.tight_layout()
plt.savefig("signup_funnel.png")
plt.close()

# =====================================
# CITY ACTIVATION
# =====================================

city_activation = (
    df.groupby("City")["Activated"]
    .mean()*100
)

plt.figure(figsize=(8,5))
city_activation.plot(kind="bar")
plt.title("Activation Rate by City")
plt.ylabel("Activation %")
plt.tight_layout()
plt.savefig("activation_rate_by_city.png")
plt.close()

# =====================================
# INCENTIVES
# =====================================

incentive_perf = (
    df.groupby("Incentive")["Activated"]
    .mean()*100
)

plt.figure(figsize=(8,5))
incentive_perf.plot(kind="bar")
plt.title("Incentive Effectiveness")
plt.ylabel("Activation %")
plt.tight_layout()
plt.savefig("incentive_effectiveness.png")
plt.close()

# =====================================
# DRIVER LIFECYCLE
# =====================================

lifecycle = pd.Series(
    [
        signup,
        verified,
        activated,
        active
    ],
    index=[
        "Signup",
        "Verification",
        "Activation",
        "Retention"
    ]
)

plt.figure(figsize=(8,5))
plt.plot(lifecycle.index,lifecycle.values,marker="o")
plt.title("Driver Lifecycle")
plt.tight_layout()
plt.savefig("driver_lifecycle.png")
plt.close()

# =====================================
# MONTHLY SIGNUPS
# =====================================

months = np.random.randint(1,13,n)

monthly = (
    pd.Series(months)
    .value_counts()
    .sort_index()
)

plt.figure(figsize=(8,5))
monthly.plot()
plt.title("Signup Trends")
plt.tight_layout()
plt.savefig("signup_trends.png")
plt.close()

# =====================================
# HEATMAP
# =====================================

pivot = pd.crosstab(
    df["City"],
    np.random.randint(1,13,n)
)

plt.figure(figsize=(10,6))
plt.imshow(pivot, aspect="auto")
plt.colorbar()
plt.title("Activation Heatmap")
plt.yticks(range(len(pivot.index)), pivot.index)
plt.tight_layout()
plt.savefig("activation_heatmap.png")
plt.close()

# =====================================
# PREDICTIVE SCORE
# =====================================

score = (
    df["Verified"]*40
    + (df["Trips"]/120)*30
    + (df["Earnings"]/5000)*30
)

plt.figure(figsize=(8,5))
plt.hist(score,bins=20)
plt.title("Predictive Activation Score")
plt.tight_layout()
plt.savefig("predictive_score_distribution.png")
plt.close()

# =====================================
# DASHBOARD
# =====================================

fig, axs = plt.subplots(2,2,figsize=(12,8))

funnel.plot(kind="bar",ax=axs[0,0])
axs[0,0].set_title("Funnel")

city_activation.plot(kind="bar",ax=axs[0,1])
axs[0,1].set_title("Cities")

incentive_perf.plot(kind="bar",ax=axs[1,0])
axs[1,0].set_title("Incentives")

monthly.plot(ax=axs[1,1])
axs[1,1].set_title("Growth")

plt.tight_layout()
plt.savefig("driver_conversion_dashboard.png")
plt.close()

# =====================================
# REPORTS
# =====================================

funnel.to_csv("signup_funnel.csv")

city_activation.to_csv("city_performance.csv")

incentive_perf.to_csv("incentive_analysis.csv")

print("Ride-Hailing Driver Analysis Completed Successfully.")