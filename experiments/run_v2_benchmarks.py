import pandas as pd
import subprocess
import zipfile
import os

# 1. Evaluate on sample_threads.csv
cmd1 = ["python", "solve_v2.py", "--input", "the-procurement-desk/sample_threads.csv", "--output", "sample_v2_preds.csv"]
subprocess.run(cmd1, check=True)

p = pd.read_csv('sample_v2_preds.csv')
a = pd.read_csv('the-procurement-desk/sample_answers.csv')
matches = (p['label'] == a['label']).sum()
total = len(a)
acc = matches / total
print(f"SAMPLE SET ACCURACY: {acc * 100:.2f}% ({matches} / {total})")

# 2. Evaluate on full test set threads.csv
cmd2 = ["python", "solve_v2.py", "--input", "the-procurement-desk/threads.csv", "--output", "submission_v2.csv"]
subprocess.run(cmd2, check=True)

df_v1 = pd.read_csv("submission.csv")
df_v2 = pd.read_csv("submission_v2.csv")

diffs = df_v1['label'] != df_v2['label']
num_diffs = diffs.sum()
print(f"\nTOTAL PREDICTION DIFFERENCES BETWEEN V1 and V2: {num_diffs} out of {len(df_v2)} ({num_diffs / len(df_v2) * 100:.2f}%)")

print("\nSample of differences:")
diff_df = pd.DataFrame({
    'thread_id': df_v1.loc[diffs, 'thread_id'],
    'v1_label': df_v1.loc[diffs, 'label'],
    'v2_label': df_v2.loc[diffs, 'label']
})
print(diff_df.head(20))

with zipfile.ZipFile('submission_v2.zip', 'w', zipfile.ZIP_DEFLATED) as z:
    z.write('submission_v2.csv')
print(f"\nsubmission_v2.zip created successfully! Size: {os.path.getsize('submission_v2.zip')} bytes")
