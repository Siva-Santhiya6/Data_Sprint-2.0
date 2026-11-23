import pandas as pd
import re

threads = pd.read_csv("the-procurement-desk/threads.csv")

# Let's inspect messages where currency is SGD, AED, JPY
unsupported_currs = []
for idx, row in threads.iterrows():
    msg = row['supplier_message']
    # Extract latest message if thread has multiple messages
    parts = re.split(r'\[Latest message\s*[^\]]*\]', msg, flags=re.IGNORECASE)
    latest_msg = parts[-1] if len(parts) > 1 else msg
    
    if re.search(r'\b(SGD|AED|JPY|AUD|CAD|CHF|CNY)\b', latest_msg, re.IGNORECASE):
        unsupported_currs.append((row['thread_id'], row['supplier'], row['category'], latest_msg))

print(f"Unsupported currency cases ({len(unsupported_currs)}):")
for tid, supp, cat, m in unsupported_currs[:5]:
    print(f"[{tid}] {supp} ({cat}):\n{m}\n")
