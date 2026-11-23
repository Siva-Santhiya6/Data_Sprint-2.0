import pandas as pd
from solve_engine_v3 import evaluate_thread

threads = pd.read_csv("the-procurement-desk/threads.csv")
print(f"Evaluating {len(threads)} test threads...")

preds = []
for idx, row in threads.iterrows():
    pred = evaluate_thread(row)
    preds.append(pred)

threads['label'] = preds

print("\n--- TEST PREDICTIONS DISTRIBUTION (v3) ---")
actions = threads['label'].apply(lambda x: x.split(':')[0] + ":" + x.split(':')[1])
print(actions.value_counts())

missing_info = threads[threads['label'] == 'ESCALATE:MISSING_INFO:']
print(f"\nTotal MISSING_INFO threads: {len(missing_info)}")
for idx in range(min(15, len(missing_info))):
    row = missing_info.iloc[idx]
    print(f"\n--- MISSING_INFO [{row['thread_id']}] {row['supplier']} ({row['category']}) ---")
    print(repr(row['supplier_message']))
