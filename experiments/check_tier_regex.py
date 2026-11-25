import pandas as pd
import re

df = pd.read_csv("the-procurement-desk/threads.csv")

tier_threads = []
for idx, row in df.iterrows():
    msg = row['supplier_message']
    if "orders of up to" in msg.lower():
        tier_threads.append((row['thread_id'], row['quantity'], msg[-250:]))

print(f"Total tier threads: {len(tier_threads)}")
failed_matches = []
for tid, q, snippet in tier_threads:
    m_tier = re.search(r'(?:INR|USD|EUR|GBP|Rs\.?|[₹\$€£])?\s*([\d,]+(?:\.\d+)?)\s*per\s*\w+\s*for orders of up to\s*(\d+)\s*[^,]+,\s*and\s*(?:INR|USD|EUR|GBP|Rs\.?|[₹\$€£])?\s*([\d,]+(?:\.\d+)?)\s*per\s*\w+\s*for larger orders', snippet, re.IGNORECASE)
    if not m_tier:
        failed_matches.append((tid, snippet))

print(f"Failed tier matches: {len(failed_matches)}")
for fm in failed_matches[:5]:
    print(fm)
