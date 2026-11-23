import pandas as pd
import re

threads = pd.read_csv("the-procurement-desk/threads.csv")

candidates = []
for idx, row in threads.iterrows():
    # Only latest message counts for banned terms according to decision-procedure.md:
    # "4. Banned contract terms anywhere in the latest message (see banned-terms.md) -> ESCALATE, BANNED_TERM."
    # Let's check both entire message and latest message
    msg = row['supplier_message']
    for line in msg.split('\n'):
        line_s = line.strip()
        if not line_s: continue
        if re.search(r'\b(renew|renewal|upfront|advance|liability|liable|exclusive|exclusivity|sole provider)\b', line_s, re.IGNORECASE):
            candidates.append(line_s)

unique_candidates = set(candidates)
print(f"Total unique lines matching banned terms regex: {len(unique_candidates)}")
for c in sorted(unique_candidates):
    print("  ->", repr(c))
