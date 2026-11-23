import pandas as pd
from solve_engine_v3 import evaluate_thread

threads = pd.read_csv("the-procurement-desk/threads.csv")
sample_sub = pd.read_csv("the-procurement-desk/sample_submission.csv")

print(f"Test threads count: {len(threads)}")
print(f"Sample submission count: {len(sample_sub)}")

preds = []
for idx, row in threads.iterrows():
    pred = evaluate_thread(row)
    preds.append(pred)

sub = pd.DataFrame({
    'thread_id': threads['thread_id'],
    'label': preds
})

# Verification
assert len(sub) == len(sample_sub), f"Length mismatch: {len(sub)} vs {len(sample_sub)}"
assert list(sub.columns) == list(sample_sub.columns), f"Columns mismatch: {sub.columns} vs {sample_sub.columns}"
assert (sub['thread_id'] == sample_sub['thread_id']).all(), "Thread ID ordering mismatch!"
assert sub['label'].isnull().sum() == 0, "Null values found in predictions!"

# Check format of labels
# Must be ACTION:REASON: or ACTION:REASON:PRICE
import re
valid_format = sub['label'].apply(lambda x: bool(re.match(r'^(ACCEPT|REJECT|COUNTER|ESCALATE):[A-Z_]+:(\d+)?$', x)))
assert valid_format.all(), f"Invalid label formats found: {sub[~valid_format]['label'].tolist()}"

# Save submission.csv in root and in the-procurement-desk
sub.to_csv("submission.csv", index=False)
sub.to_csv("the-procurement-desk/submission.csv", index=False)

print("\nSuccessfully generated submission.csv!")
print("First 15 rows of submission.csv:")
print(sub.head(15))
print("\nAction breakdown:")
print(sub['label'].apply(lambda x: x.split(':')[0]).value_counts())
