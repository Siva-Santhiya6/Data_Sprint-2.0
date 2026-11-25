import sys
import os
sys.path.insert(0, os.path.abspath("experiments"))
sys.path.insert(0, os.path.abspath("."))
import pandas as pd
from test_solver_updates import evaluate_thread, load_playbook, df_true, col_true

cats, supps, amds = load_playbook()
threads = pd.read_csv("the-procurement-desk/threads.csv")

diffs = []
for idx, row in threads.iterrows():
    pred = evaluate_thread(row, cats, supps, amds)
    true_val = df_true.loc[idx, col_true]
    if pred != true_val:
        diffs.append((row['thread_id'], pred, true_val, row))

print(f"Remaining diffs: {len(diffs)}")
for tid, pred, true_val, row in diffs:
    print(f"\n=== {tid} ===")
    print(f"Pred: {pred} | True: {true_val}")
    print(f"Category: {row['category']}, Supplier: {row['supplier']}, Qty: {row['quantity']}, Round: {row['round']}, Date: {row['date']}")
    print(f"Message:\n{row['supplier_message']}")
