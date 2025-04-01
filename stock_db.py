import sqlite3
import pandas as pd

# # Load the CSV file
# csv_file = "data/sale.csv"
# df = pd.read_csv(csv_file, encoding="ISO-8859-1")

# # Convert ORDERDATE to datetime format
# df["ORDERDATE"] = pd.to_datetime(df["ORDERDATE"], errors="coerce")

# # Fill missing values
# df["ADDRESSLINE2"].fillna("Unknown", inplace=True)
# df["STATE"].fillna("Unknown", inplace=True)
# df["TERRITORY"].fillna("Unknown", inplace=True)
# df["POSTALCODE"] = df["POSTALCODE"].astype(str).replace("nan", "Unknown")

# # Ensure correct datatypes
# df["ORDERNUMBER"] = df["ORDERNUMBER"].astype(int)
# df["QUANTITYORDERED"] = df["QUANTITYORDERED"].astype(int)
# df["MSRP"] = df["MSRP"].astype(int)

# # Save the cleaned file
# cleaned_file_path = "sale_cleaned.csv"
# df.to_csv(cleaned_file_path, index=False, encoding="ISO-8859-1")

# print("Data cleaning complete. Cleaned file saved as sale_cleaned.csv")

csv_file = "sale_cleaned.csv"
df = pd.read_csv(csv_file, encoding="ISO-8859-1")
db_file="sale.db"
conn=sqlite3.connect(db_file)

cursor = conn.cursor()


# Convert CSV to SQL Table
table_name = "sale"  # Choose a table name
df.to_sql(table_name, conn, if_exists="replace", index=False)

# Close the database connection
conn.close()