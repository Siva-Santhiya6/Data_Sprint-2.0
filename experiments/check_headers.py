import pandas as pd
import re

threads = pd.read_csv("the-procurement-desk/threads.csv")

headers = set()
for msg in threads['supplier_message']:
    found = re.findall(r'\[([^\]]+)\]', msg)
    for f in found:
        # ignore admin override
        if 'admin override' in f.lower(): continue
        headers.add(f.split('—')[0].strip())

print("Headers found in threads:", headers)
