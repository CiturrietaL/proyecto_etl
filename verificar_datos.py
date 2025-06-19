import sqlite3
import pandas as pd

conn = sqlite3.connect('etl_proyecto.db')

print("✅ Dim_Customers")
print(pd.read_sql("SELECT * FROM Dim_Customers", conn))

print("\n✅ Dim_Accounts")
print(pd.read_sql("SELECT * FROM Dim_Accounts", conn))

print("\n✅ Dim_Products")
print(pd.read_sql("SELECT * FROM Dim_Products", conn))

print("\n✅ Fact_Transactions")
print(pd.read_sql("SELECT * FROM Fact_Transactions", conn))

conn.close()
