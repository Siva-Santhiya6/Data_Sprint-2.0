import pandas as pd

df = pd.read_csv("the-procurement-desk/threads.csv")
print("Total test threads:", len(df))
print("\nCategories distribution:")
print(df['category'].value_counts())
print("\nSuppliers count:", df['supplier'].nunique())
print("\nRounds distribution:")
print(df['round'].value_counts().sort_index())
print("\nDates min and max:", df['date'].min(), "to", df['date'].max())
print("\nSample test messages:")
for i in range(5):
    row = df.iloc[i]
    print(f"\n--- {row['thread_id']} ({row['supplier']}, {row['category']}, r={row['round']}, qty={row['quantity']}) ---")
    print(row['supplier_message'])
