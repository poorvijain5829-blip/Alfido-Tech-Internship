"""
Task 3: Data Analysis with Pandas
-----------------------------------
Goal: Demonstrate data analysis skills using Pandas.

Requirements:
  - Load and inspect a CSV dataset
  - Clean missing or incorrect data
  - Apply filtering, grouping, and aggregation
  - Explain insights in simple words

Author: Lucky Jain
"""

import pandas as pd
import os

# ----------------------------------------------------------------------
# 1. CREATE A SAMPLE SALES DATASET (CSV)
#    In a real project you would load an existing CSV file.
#    Here we build one so the script is fully self-contained.
# ----------------------------------------------------------------------
data = {
    "OrderID":     [101, 102, 103, 104, 105, 106, 107, 108, 109, 110],
    "Product":     ["Laptop", "Phone", "Tablet", "Laptop", "Phone",
                    "Tablet", "Laptop", None,    "Phone", "Tablet"],
    "Category":    ["Electronics", "Electronics", "Electronics", "Electronics",
                    "Electronics", "Electronics", "Electronics", "Electronics",
                    "Electronics", "Electronics"],
    "Quantity":    [2, 5, 3, 1, 4, 2, 3, 2, None, 1],
    "UnitPrice":   [55000, 20000, 30000, 55000, 20000,
                    30000, 55000, 20000, 20000, -999],   # -999 is incorrect data
    "City":        ["Delhi", "Mumbai", "Delhi", "Bangalore", "Mumbai",
                    "Delhi", "Bangalore", "Mumbai", "Delhi", "Bangalore"],
    "CustomerAge": [25, 34, None, 28, 45, 31, 22, 38, 29, 41],
}

# Save to CSV so we can demonstrate loading from a file
CSV_PATH = "sales_data.csv"
pd.DataFrame(data).to_csv(CSV_PATH, index=False)
print(f"Sample CSV created: '{CSV_PATH}'\n")


# ----------------------------------------------------------------------
# 2. LOAD AND INSPECT THE DATASET
# ----------------------------------------------------------------------
print("=" * 55)
print("STEP 1: LOAD AND INSPECT")
print("=" * 55)

df = pd.read_csv(CSV_PATH)

print("\n--- First 5 rows ---")
print(df.head())

print("\n--- Dataset shape (rows, columns) ---")
print(df.shape)

print("\n--- Data types of each column ---")
print(df.dtypes)

print("\n--- Missing values per column ---")
print(df.isnull().sum())

print("\n--- Basic statistics ---")
print(df.describe())


# ----------------------------------------------------------------------
# 3. CLEAN MISSING OR INCORRECT DATA
# ----------------------------------------------------------------------
print("\n" + "=" * 55)
print("STEP 2: CLEAN DATA")
print("=" * 55)

# 3a. Drop rows where 'Product' is missing (can't analyse unknown product)
before = len(df)
df = df.dropna(subset=["Product"])
print(f"\nDropped {before - len(df)} row(s) with missing Product name.")

# 3b. Fill missing Quantity with the median quantity (safe estimate)
median_qty = df["Quantity"].median()
df["Quantity"] = df["Quantity"].fillna(median_qty)
print(f"Filled missing Quantity with median value: {median_qty}")

# 3c. Fill missing CustomerAge with the mean age (rounded)
mean_age = round(df["CustomerAge"].mean())
df["CustomerAge"] = df["CustomerAge"].fillna(mean_age)
print(f"Filled missing CustomerAge with mean value: {mean_age}")

# 3d. Remove rows with clearly incorrect UnitPrice (negative values)
before = len(df)
df = df[df["UnitPrice"] > 0]
print(f"Removed {before - len(df)} row(s) with invalid (negative) UnitPrice.")

# 3e. Add a calculated column: TotalRevenue = Quantity × UnitPrice
df["TotalRevenue"] = df["Quantity"] * df["UnitPrice"]

print("\n--- Cleaned dataset ---")
print(df)


# ----------------------------------------------------------------------
# 4. FILTERING, GROUPING, AND AGGREGATION
# ----------------------------------------------------------------------
print("\n" + "=" * 55)
print("STEP 3: FILTERING, GROUPING & AGGREGATION")
print("=" * 55)

# --- Filtering: orders with revenue above 1,00,000 ---
high_value = df[df["TotalRevenue"] > 100000]
print(f"\n[Filter] Orders with TotalRevenue > ₹1,00,000: {len(high_value)}")
print(high_value[["OrderID", "Product", "City", "TotalRevenue"]])

# --- Grouping by Product: total revenue and total quantity per product ---
product_group = df.groupby("Product").agg(
    Total_Revenue=("TotalRevenue", "sum"),
    Total_Quantity=("Quantity", "sum"),
    Avg_UnitPrice=("UnitPrice", "mean"),
    Order_Count=("OrderID", "count")
).reset_index()

print("\n[Group By Product] Sales Summary:")
print(product_group)

# --- Grouping by City: total revenue per city ---
city_group = df.groupby("City")["TotalRevenue"].sum().reset_index()
city_group.columns = ["City", "Total_Revenue"]
city_group = city_group.sort_values("Total_Revenue", ascending=False)

print("\n[Group By City] Revenue Summary:")
print(city_group)

# --- Aggregation: overall summary stats ---
print("\n[Aggregation] Overall Stats:")
print(f"  Total Orders   : {len(df)}")
print(f"  Total Revenue  : ₹{df['TotalRevenue'].sum():,.0f}")
print(f"  Avg Order Value: ₹{df['TotalRevenue'].mean():,.0f}")
print(f"  Top Product    : {product_group.loc[product_group['Total_Revenue'].idxmax(), 'Product']}")
print(f"  Top City       : {city_group.iloc[0]['City']}")


# ----------------------------------------------------------------------
# 5. INSIGHTS SUMMARY (in simple words)
# ----------------------------------------------------------------------
print("\n" + "=" * 55)
print("STEP 4: KEY INSIGHTS")
print("=" * 55)

top_product = product_group.loc[product_group["Total_Revenue"].idxmax(), "Product"]
top_city    = city_group.iloc[0]["City"]
total_rev   = df["TotalRevenue"].sum()

print(f"""
1. Best Selling Product: '{top_product}' generated the highest
   total revenue among all products.

2. Top City: '{top_city}' contributed the most revenue,
   making it the most valuable market.

3. High-Value Orders: {len(high_value)} orders had a total value
   above ₹1,00,000 — these are premium customers.

4. Data Quality: The dataset had missing values in Product,
   Quantity, and CustomerAge columns, plus one row with an
   incorrect (negative) price. All were cleaned before analysis.

5. Total Revenue: ₹{total_rev:,.0f} was generated across
   {len(df)} valid orders.
""")

print("Data analysis with Pandas completed successfully.")
