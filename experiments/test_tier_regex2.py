import pandas as pd
import re

df = pd.read_csv("the-procurement-desk/threads.csv")

tier_threads = []
for idx, row in df.iterrows():
    msg = row['supplier_message']
    if "orders of up to" in msg.lower():
        tier_threads.append((row['thread_id'], row['quantity'], msg))

matched = 0
for tid, q, snippet in tier_threads:
    m = re.search(r'(?:INR|USD|EUR|GBP|Rs\.?|[₹\$€£])?\s*([\d,]+(?:\.\d+)?)\s*per\s+[a-zA-Z\s]+?for orders of up to\s*(\d+)\s*[^,]+,\s*and\s*(?:INR|USD|EUR|GBP|Rs\.?|[₹\$€£])?\s*([\d,]+(?:\.\d+)?)\s*per\s+[a-zA-Z\s]+?for larger orders', snippet, re.IGNORECASE)
    if m:
        matched += 1
    else:
        print("Still failed:", tid)

print(f"Tier regex matches: {matched} / {len(tier_threads)}")
