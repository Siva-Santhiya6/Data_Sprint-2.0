import pandas as pd
import re

threads = pd.read_csv("the-procurement-desk/threads.csv")

price_clauses = []
for idx, row in threads.iterrows():
    msg = row['supplier_message']
    parts = re.split(r'\[Latest message\s*[^\]]*\]', msg, flags=re.IGNORECASE)
    latest_msg = parts[-1] if len(parts) > 1 else msg
    
    # Let's find matches for:
    # "quote ...", "offer is ...", "can do ...", "final price is ...", "best we can offer is ..."
    m = re.search(r'(quote|best we can offer is|can do|revised offer is|final price is|can offer)\s+(.*)', latest_msg, re.IGNORECASE)
    if m:
        clause = m.group(2).split('.')[0].split('\n')[0].strip()
        price_clauses.append((row['thread_id'], clause))

print(f"Total price clauses extracted: {len(price_clauses)}")
# Let's inspect some of them
for tid, c in price_clauses[:20]:
    print(f"[{tid}] -> {repr(c)}")
