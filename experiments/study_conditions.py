import pandas as pd
import re

threads = pd.read_csv("the-procurement-desk/threads.csv")

candidates = set()
for idx, row in threads.iterrows():
    msg = row['supplier_message']
    for line in msg.split('\n'):
        line_s = line.strip()
        if not line_s: continue
        # Look for clauses that might be contract conditions
        if re.search(r'\b(unless|continues|cancel|terms|agreement|contract|condition|guarantee|warranty|delivery|payment|liability|liable|exclusive|renew|upfront|advance|down payment|deposit)\b', line_s, re.IGNORECASE):
            candidates.add(line_s)

print(f"Total unique condition lines: {len(candidates)}")
for c in sorted(candidates):
    print("  ->", repr(c))
