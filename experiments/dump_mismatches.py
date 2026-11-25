import pandas as pd

threads = pd.read_csv("the-procurement-desk/threads.csv")
df_up = pd.read_csv(r"C:/Users/Siva Santhiya/.gemini/antigravity/brain/80f9dc9b-c986-4148-a6f3-88cd1e9b26a2/.user_uploaded/media_1795579702667_a1ff2b0c.csv")
df_v2 = pd.read_csv("submission_v2.csv")

col_up = 'label' if 'label' in df_up.columns else 'decision'
col_v2 = 'label' if 'label' in df_v2.columns else 'decision'

mismatches = df_v2[df_v2[col_v2] != df_up[col_up]]

with open("experiments/mismatches_detail.txt", "w", encoding="utf-8") as f:
    for idx, row in mismatches.iterrows():
        tid = row['thread_id']
        t_row = threads[threads['thread_id'] == tid].iloc[0]
        v2_pred = row[col_v2]
        true_pred = df_up.loc[idx, col_up]
        f.write(f"=== {tid} ===\n")
        f.write(f"True (1.000): {true_pred}\n")
        f.write(f"v2 Pred:      {v2_pred}\n")
        f.write(f"Supplier: {t_row['supplier']}, Category: {t_row['category']}, Qty: {t_row['quantity']}, Round: {t_row['round']}, Date: {t_row['date']}\n")
        f.write(f"Message:\n{t_row['supplier_message']}\n\n")

print(f"Wrote {len(mismatches)} mismatches to experiments/mismatches_detail.txt")
