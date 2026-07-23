
import pandas as pd
import matplotlib.pyplot as plt

# ==========================================
# LOAD DATA
# ==========================================

CSV_PATH = r"Olist_Customer_Geographic_Analytics\olist_customers_dataset.csv"

df = pd.read_csv(CSV_PATH)

print("Dataset Loaded Successfully")
print(df.head())

# ==========================================
# SUMMARY METRICS
# ==========================================

total_records = len(df)

unique_customers = (
    df["customer_unique_id"]
    .nunique()
)

total_states = (
    df["customer_state"]
    .nunique()
)

total_cities = (
    df["customer_city"]
    .nunique()
)

summary = pd.DataFrame({

    "Metric":[
        "Total Records",
        "Unique Customers",
        "States",
        "Cities"
    ],

    "Value":[
        total_records,
        unique_customers,
        total_states,
        total_cities
    ]
})

summary.to_csv(
    "customer_summary.csv",
    index=False
)

# ==========================================
# CUSTOMERS BY STATE
# ==========================================

state_counts = (
    df["customer_state"]
    .value_counts()
)

plt.figure(figsize=(10,6))

state_counts.head(15).plot(
    kind="bar"
)

plt.title(
    "Top States by Customer Count"
)

plt.ylabel(
    "Customers"
)

plt.tight_layout()

plt.savefig(
    "customers_by_state.png"
)

plt.close()

# ==========================================
# TOP CITIES
# ==========================================

city_counts = (
    df["customer_city"]
    .value_counts()
)

plt.figure(figsize=(10,6))

city_counts.head(20).plot(
    kind="barh"
)

plt.title(
    "Top Cities"
)

plt.tight_layout()

plt.savefig(
    "top_cities.png"
)

plt.close()

# ==========================================
# STATE DISTRIBUTION
# ==========================================

plt.figure(figsize=(8,8))

state_counts.head(10).plot(
    kind="pie",
    autopct="%1.1f%%"
)

plt.ylabel("")

plt.title(
    "Customer Distribution by State"
)

plt.tight_layout()

plt.savefig(
    "state_distribution.png"
)

plt.close()

# ==========================================
# ZIP PREFIX DISTRIBUTION
# ==========================================

zip_counts = (
    df["customer_zip_code_prefix"]
    .value_counts()
)

plt.figure(figsize=(10,6))

zip_counts.head(20).plot(
    kind="bar"
)

plt.title(
    "Top Zip Code Prefixes"
)

plt.tight_layout()

plt.savefig(
    "zip_prefix_distribution.png"
)

plt.close()

# ==========================================
# CUSTOMER SUMMARY
# ==========================================

plt.figure(figsize=(8,5))

plt.bar(
    summary["Metric"],
    summary["Value"]
)

plt.title(
    "Customer Summary"
)

plt.tight_layout()

plt.savefig(
    "customer_summary.png"
)

plt.close()

# ==========================================
# EXECUTIVE DASHBOARD
# ==========================================

fig, axs = plt.subplots(
    2,
    2,
    figsize=(14,10)
)

state_counts.head(10).plot(
    kind="bar",
    ax=axs[0,0]
)

axs[0,0].set_title(
    "Customers by State"
)

city_counts.head(10).plot(
    kind="bar",
    ax=axs[0,1]
)

axs[0,1].set_title(
    "Top Cities"
)

zip_counts.head(10).plot(
    kind="bar",
    ax=axs[1,0]
)

axs[1,0].set_title(
    "Zip Prefixes"
)

axs[1,1].bar(
    summary["Metric"],
    summary["Value"]
)

axs[1,1].set_title(
    "Customer Summary"
)

plt.tight_layout()

plt.savefig(
    "executive_dashboard.png"
)

plt.close()

print()
print("="*50)
print("OLIST CUSTOMER GEOGRAPHIC ANALYSIS COMPLETE")
print("="*50)
print(f"Records: {total_records}")
print(f"Unique Customers: {unique_customers}")
print(f"States: {total_states}")
print(f"Cities: {total_cities}")