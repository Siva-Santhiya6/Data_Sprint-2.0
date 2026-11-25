import pandas as pd
import re

df = pd.read_csv("the-procurement-desk/threads.csv")

corr_threads = []
for idx, row in df.iterrows():
    msg = row['supplier_message']
    if "CORRECTION" in msg:
        parts = re.split(r'\[Latest message\s*[^\]]*\]', msg, flags=re.I)
        earlier = parts[0] if len(parts) > 1 else ""
        latest = parts[-1] if len(parts) > 1 else msg
        corr_threads.append((row['thread_id'], row['category'], earlier, latest))

print(f"Total correction threads: {len(corr_threads)}")
for tid, cat, earlier, latest in corr_threads[:10]:
    print(f"\n--- {tid} ({cat}) ---")
    print("EARLIER:", earlier[-150:].replace('\n', ' '))
    print("LATEST:", latest.replace('\n', ' '))
