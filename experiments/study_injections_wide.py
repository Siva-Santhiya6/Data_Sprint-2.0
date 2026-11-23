import pandas as pd
import re

threads = pd.read_csv("the-procurement-desk/threads.csv")

candidates = []
for idx, row in threads.iterrows():
    msg = row['supplier_message']
    for line in msg.split('\n'):
        line_s = line.strip()
        if not line_s: continue
        if re.search(r'\b(ignore|disregard|bypass|jailbreak|prompt|system|assistant|reviewer|instruction|override|pre-approved|signed off)\b', line_s, re.IGNORECASE):
            candidates.append(line_s)

unique_candidates = set(candidates)
print(f"Total unique lines matching wider security regex: {len(unique_candidates)}")
for c in sorted(unique_candidates):
    print("  ->", repr(c))
