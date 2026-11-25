import pandas as pd
import re

df = pd.read_csv("the-procurement-desk/threads.csv")

vol_threads = []
for idx, row in df.iterrows():
    msg = row['supplier_message']
    m = re.search(r'with a further\s*(\d+)%\s*off for orders of\s*(\d+)\s*(?:\w+\s*)?or more', msg, re.I)
    if m:
        disc = float(m.group(1))
        thresh = float(m.group(2))
        q = float(row['quantity'])
        vol_threads.append((row['thread_id'], row['category'], q, thresh, disc, q >= thresh, msg[-200:]))

print(f"Total volume discount threads: {len(vol_threads)}")
for vt in vol_threads[:15]:
    print(vt[:6])
