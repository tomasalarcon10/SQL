
import pandas as pd
import matplotlib.pyplot as plt

# =====================================
# LOAD DATA
# =====================================

CSV_PATH = r"Retail_Revenue_Intelligence_Hub\sales_data_sample.csv"

df = pd.read_csv(
    CSV_PATH,
    encoding="latin1"
)

# =====================================
# CLEANING
# =====================================

df["ORDERDATE"] = pd.to_datetime(
    df["ORDERDATE"]
)

# =====================================
# MONTHLY REVENUE
# =====================================

monthly = (
    df.groupby(
        ["YEAR_ID","MONTH_ID"]
    )["SALES"]
    .sum()
)

plt.figure(figsize=(10,6))

monthly.plot()

plt.title(
    "Monthly Revenue Trend"
)

plt.tight_layout()

plt.savefig(
    "monthly_revenue.png"
)

plt.close()

# =====================================
# COUNTRY SALES
# =====================================

country_sales = (
    df.groupby("COUNTRY")
    ["SALES"]
    .sum()
    .sort_values(
        ascending=False
    )
)

plt.figure(figsize=(12,6))

country_sales.head(15).plot(
    kind="bar"
)

plt.title(
    "Top Countries by Revenue"
)

plt.tight_layout()

plt.savefig(
    "country_sales.png"
)

plt.close()

# =====================================
# PRODUCT LINE
# =====================================

productline = (
    df.groupby("PRODUCTLINE")
    ["SALES"]
    .sum()
    .sort_values(
        ascending=False
    )
)

plt.figure(figsize=(10,6))

productline.plot(
    kind="bar"
)

plt.title(
    "Product Line Performance"
)

plt.tight_layout()

plt.savefig(
    "productline_performance.png"
)

plt.close()

# =====================================
# TOP CUSTOMERS
# =====================================

customers = (
    df.groupby("CUSTOMERNAME")
    ["SALES"]
    .sum()
    .sort_values(
        ascending=False
    )
)

plt.figure(figsize=(10,6))

customers.head(15).plot(
    kind="barh"
)

plt.title(
    "Top Customers"
)

plt.tight_layout()

plt.savefig(
    "top_customers.png"
)

plt.close()

# =====================================
# DEAL SIZE
# =====================================

deal = (
    df["DEALSIZE"]
    .value_counts()
)

plt.figure(figsize=(8,5))

deal.plot(
    kind="pie",
    autopct="%1.1f%%"
)

plt.ylabel("")

plt.title(
    "Deal Size Distribution"
)

plt.savefig(
    "dealsize_distribution.png"
)

plt.close()

# =====================================
# REVENUE HEATMAP
# =====================================

pivot = pd.pivot_table(
    df,
    values="SALES",
    index="YEAR_ID",
    columns="MONTH_ID",
    aggfunc="sum"
)

plt.figure(figsize=(10,5))

plt.imshow(
    pivot,
    aspect="auto"
)

plt.colorbar()

plt.title(
    "Revenue Heatmap"
)

plt.tight_layout()

plt.savefig(
    "revenue_heatmap.png"
)

plt.close()

# =====================================
# EXECUTIVE DASHBOARD
# =====================================

fig, axs = plt.subplots(
    2,
    2,
    figsize=(14,10)
)

country_sales.head(10).plot(
    kind="bar",
    ax=axs[0,0]
)

axs[0,0].set_title(
    "Countries"
)

productline.plot(
    kind="bar",
    ax=axs[0,1]
)

axs[0,1].set_title(
    "Products"
)

customers.head(10).plot(
    kind="bar",
    ax=axs[1,0]
)

axs[1,0].set_title(
    "Customers"
)

deal.plot(
    kind="pie",
    ax=axs[1,1],
    autopct="%1.1f%%"
)

axs[1,1].set_title(
    "Deal Size"
)

plt.tight_layout()

plt.savefig(
    "executive_dashboard.png"
)

plt.close()

# =====================================
# REPORTS
# =====================================

country_sales.to_csv(
    "country_sales_report.csv"
)

customers.to_csv(
    "customer_sales_report.csv"
)

productline.to_csv(
    "productline_report.csv"
)

print(
    "Retail Revenue Intelligence Hub Completed Successfully."
)