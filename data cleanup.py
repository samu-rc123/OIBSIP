import pandas as pd

# ==== Step 1: Load dataset ====
df = pd.read_csv("data.csv")
print("Data loaded successfully!")

# ==== Step 2: Standardize column names ====
df.columns = df.columns.str.strip().str.lower().str.replace(" ", "_")

# ==== Step 3: Clean string columns ====
for col in df.select_dtypes(include="object").columns:
    df[col] = df[col].str.strip()   # remove leading/trailing spaces

# ==== Step 4: Convert numeric columns safely ====
for col in ["age", "amount"]:
    if col in df.columns:
        df[col] = pd.to_numeric(df[col], errors="coerce")

# ==== Step 5: Handle missing values ====
# Drop rows with missing Name or Age (critical fields)
df = df.dropna(subset=["name", "age"])

# Fill Amount with mean if missing
if "amount" in df.columns:
    df["amount"] = df["amount"].fillna(df["amount"].mean())

# ==== Step 6: Convert date column if present ====
if "date_column" in df.columns:
    df["date_column"] = pd.to_datetime(df["date_column"], errors="coerce")

# ==== Step 7: Filter invalid ages ====
if "age" in df.columns:
    df = df[df["age"] >= 0]

# ==== Step 8: Remove duplicates (after cleaning) ====
df = df.drop_duplicates()

# ==== Step 9: Round numeric values for neatness ====
if "age" in df.columns:
    df["age"] = df["age"].round(0).astype(int)
if "amount" in df.columns:
    df["amount"] = df["amount"].round(2)

# ==== Step 10: Save cleaned data ====
df.to_csv("cleaned_data.csv", index=False)
print("Data cleanup complete! Cleaned file saved as cleaned_data.csv")
