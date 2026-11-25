import pandas as pd
import re

df = pd.read_csv("the-procurement-desk/threads.csv")

# Let's inspect all non-ascii characters or multilingual patterns
non_ascii_threads = []
for idx, row in df.iterrows():
    msg = row['supplier_message']
    # Check for Devanagari, Tamil, Telugu, Arabic, Chinese, etc.
    # Exclude rupee symbol ₹ (\u20b9), euro €, pound £, mdash —, ndash –
    cleaned = re.sub(r'[\u20b9\u20ac\u00a3\u2014\u2013\u2018\u2019\u201c\u201d]', '', msg)
    non_ascii = [c for c in cleaned if ord(c) > 127]
    if non_ascii:
        non_ascii_threads.append((row['thread_id'], "".join(non_ascii[:20]), msg))

print(f"Total threads with non-ascii characters: {len(non_ascii_threads)}")
for t_id, chars, msg in non_ascii_threads[:20]:
    # find where non-ascii appears
    lines = [l for l in msg.split('\n') if any(ord(c) > 127 for c in re.sub(r'[\u20b9\u20ac\u00a3\u2014\u2013\u2018\u2019\u201c\u201d]', '', l))]
    print(f"{t_id}: {lines}")
