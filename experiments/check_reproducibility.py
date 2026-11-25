import pandas as pd
import subprocess
import os

print("Running solve_v2.py...")
cmd = ["python", "solve_v2.py", "--input", "the-procurement-desk/threads.csv", "--output", "test_reproduce.csv"]
subprocess.run(cmd, check=True)

df1 = pd.read_csv('submission_v2.csv')
df2 = pd.read_csv('test_reproduce.csv')

matches = (df1['label'] == df2['label']).sum()
total = len(df1)
print(f"Comparison: {matches} / {total} exact matches ({matches/total * 100:.2f}%)")

if os.path.exists("test_reproduce.csv"):
    os.remove("test_reproduce.csv")
    print("Cleaned up temporary test file.")
