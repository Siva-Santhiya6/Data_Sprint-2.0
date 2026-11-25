import pandas as pd

s_threads = pd.read_csv("the-procurement-desk/sample_threads.csv")
s_answers = pd.read_csv("the-procurement-desk/sample_answers.csv")
merged = pd.merge(s_threads, s_answers, on="thread_id")

for idx, row in merged.iterrows():
    if "APPROVAL_LIMIT" in row['label'] or "ACCEPT" in row['label']:
        print(f"{row['thread_id']} ({row['category']}, qty={row['quantity']}, round={row['round']}): {row['label']}")
        print(f"  Msg: {row['supplier_message'][-200:].replace(chr(10), ' ')}")
