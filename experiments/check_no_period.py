import pandas as pd
import re

threads = pd.read_csv("the-procurement-desk/threads.csv")
sub_cats = {'cleaning', 'cloud-servers', 'crm-licenses', 'design-software', 'security-guards'}

truly_no_period = []
for idx, row in threads.iterrows():
    if row['category'] not in sub_cats:
        continue
    msg = row['supplier_message']
    # Check if month or year appears anywhere in the message
    if not re.search(r'\b(month|monthly|year|yearly|annum|annual|annually)\b', msg, re.IGNORECASE):
        truly_no_period.append((row['thread_id'], row['supplier'], row['category'], msg))

print(f"Subscription messages with NO period anywhere: {len(truly_no_period)}")
for tid, s, c, m in truly_no_period[:10]:
    print(f"[{tid}] {s} ({c}):\n{repr(m)}\n")
