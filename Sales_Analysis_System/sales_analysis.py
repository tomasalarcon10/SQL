
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

np.random.seed(42)

# ======================================
# SAMPLE DATA
# ======================================

categories = [
    "Beverages",
    "Dairy",
    "Snacks",
    "Fruits",
    "Vegetables"
]

stores = [
    "Bogota",
    "Medellin",
    "Cali",
    "Barranquilla"
]

payments = [
    "Cash",
    "Credit Card",
    "Debit Card",
    "Mobile Payment"
]

products = [
    "Milk",
    "Bread",
    "Juice",
    "Apple",
    "Chips",
    "Coffee",
    "Cheese",
    "Banana"
]

n = 500

df = pd.DataFrame({
    "Category": np.random.choice(categories,n),
    "Store": np.random.choice(stores,n),
    "PaymentMethod": np.random.choice(payments,n),
    "Product": np.random.choice(products,n),
    "Quantity": np.random.randint(1,10,n),
    "Revenue": np.random.randint(5,150,n)
})

# ======================================
# Category Sales
# ======================================

category_sales = (
    df.groupby("Category")["Revenue"]
    .sum()
)

plt.figure(figsize=(8,5))
category_sales.plot(kind="bar")
plt.title("Sales by Category")
plt.tight_layout()
plt.savefig("category_sales.png")
plt.close()

# ======================================
# Location Sales
# ======================================

location_sales = (
    df.groupby("Store")["Revenue"]
    .sum()
)

plt.figure(figsize=(8,5))
location_sales.plot(kind="bar")
plt.title("Sales by Location")
plt.tight_layout()
plt.savefig("location_sales.png")
plt.close()

# ======================================
# Payment Methods
# ======================================

payment = (
    df.groupby("PaymentMethod")
    .size()
)

plt.figure(figsize=(8,5))
payment.plot(kind="pie", autopct="%1.1f%%")
plt.ylabel("")
plt.title("Payment Methods")
plt.tight_layout()
plt.savefig("payment_methods.png")
plt.close()

# ======================================
# Monthly Sales
# ======================================

months = pd.Series(
    np.random.randint(1,13,n)
)

monthly = (
    months.value_counts()
    .sort_index()
)

plt.figure(figsize=(8,5))
monthly.plot()
plt.title("Monthly Sales")
plt.tight_layout()
plt.savefig("monthly_sales.png")
plt.close()

# ======================================
# Top Products
# ======================================

top_products = (
    df.groupby("Product")["Quantity"]
    .sum()
    .sort_values(ascending=False)
)

plt.figure(figsize=(8,5))
top_products.head(10).plot(kind="bar")
plt.title("Top Products")
plt.tight_layout()
plt.savefig("top_products.png")
plt.close()

# ======================================
# REPORTS
# ======================================

category_sales.reset_index().to_csv(
    "sales_by_category.csv",
    index=False
)

location_sales.reset_index().to_csv(
    "sales_by_location.csv",
    index=False
)

payment.reset_index().to_csv(
    "payment_methods.csv",
    index=False
)

print("Sales Analysis Completed Successfully.")