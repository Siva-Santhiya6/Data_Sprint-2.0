import pandas as pd
import re

df = pd.read_csv("the-procurement-desk/threads.csv")

for idx, row in df.iterrows():
    msg = row['supplier_message']
    # search for "off" or "discount"
    for m in re.finditer(r'(\d+)%\s*(?:off|discount)', msg, re.I):
        # print surrounding text
        start = max(0, m.start() - 40)
        end = min(len(msg), m.end() + 60)
        snippet = msg[start:end].replace('\n', ' ')
        # filter out standard patterns
        if "off our previous quote" in snippet:
            continue
        if "off our list price" in snippet:
            continue
        if "off for orders of" in snippet:
            continue
        print(f"{row['thread_id']}: {snippet}")
