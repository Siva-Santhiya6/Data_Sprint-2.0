import pandas as pd

uploaded_path = r"C:/Users/Siva Santhiya/.gemini/antigravity/brain/80f9dc9b-c986-4148-a6f3-88cd1e9b26a2/.user_uploaded/media_1795579702667_a1ff2b0c.csv"
df_up = pd.read_csv(uploaded_path)
print("Uploaded columns:", df_up.columns.tolist())

df_sub = pd.read_csv("submission.csv")
print("submission.csv columns:", df_sub.columns.tolist())

df_v2 = pd.read_csv("submission_v2.csv")
print("submission_v2.csv columns:", df_v2.columns.tolist())

col_up = 'label' if 'label' in df_up.columns else 'decision'
col_sub = 'label' if 'label' in df_sub.columns else 'decision'
col_v2 = 'label' if 'label' in df_v2.columns else 'decision'

print(f"Diff between submission.csv and uploaded: {(df_sub[col_sub] != df_up[col_up]).sum()}")
print(f"Diff between submission_v2.csv and uploaded: {(df_v2[col_v2] != df_up[col_up]).sum()}")

# Print first 10 mismatches between v2 and uploaded
mismatches = df_v2[df_v2[col_v2] != df_up[col_up]]
print(f"\nTotal mismatches between v2 and uploaded: {len(mismatches)}")
for idx, row in mismatches.head(30).iterrows():
    tid = row['thread_id']
    v2_val = row[col_v2]
    up_val = df_up.loc[idx, col_up]
    print(f"{tid}: v2='{v2_val}' vs 1.000='{up_val}'")
