import pandas as pd
from solve_engine import evaluate_thread, cats, supps, amds

threads = pd.read_csv("the-procurement-desk/threads.csv")
print(f"Loaded {len(threads)} test threads.")

preds = []
for idx, row in threads.iterrows():
    pred = evaluate_thread(row)
    preds.append(pred)

threads['label'] = preds

print("\n--- TEST PREDICTIONS DISTRIBUTION ---")
actions = threads['label'].apply(lambda x: x.split(':')[0] + ":" + x.split(':')[1])
print(actions.value_counts())

print("\n--- SAMPLE 20 TEST PREDICTIONS ---")
for idx in range(20):
    row = threads.iloc[idx]
    print(f"{row['thread_id']}: {row['label']} | {row['supplier']} ({row['category']}, r={row['round']})")

# Let's inspect threads predicted as MISSING_INFO to ensure every one is genuinely missing info
missing_info_threads = threads[threads['label'] == 'ESCALATE:MISSING_INFO:']
print(f"\nTotal MISSING_INFO threads: {len(missing_info_threads)}")
for idx in range(min(15, len(missing_info_threads))):
    row = missing_info_threads.iloc[idx]
    print(f"\n--- MISSING_INFO [{row['thread_id']}] {row['supplier']} ({row['category']}) ---")
    print(repr(row['supplier_message']))
