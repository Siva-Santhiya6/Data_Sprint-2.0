import pandas as pd
import re

threads = pd.read_csv("the-procurement-desk/threads.csv")

subscription_categories = {'cleaning', 'cloud-servers', 'crm-licenses', 'design-software', 'security-guards'}

no_period_cases = []
no_number_cases = []

for idx, row in threads.iterrows():
    msg = row['supplier_message']
    parts = re.split(r'\[Latest message\s*[^\]]*\]', msg, flags=re.IGNORECASE)
    latest_msg = parts[-1] if len(parts) > 1 else msg
    
    # Check if there is any number or number word
    has_number = bool(re.search(r'\d', latest_msg) or re.search(r'\b(one|two|three|four|five|six|seven|eight|nine|ten|eleven|twelve|thirteen|fourteen|fifteen|sixteen|seventeen|eighteen|nineteen|twenty|thirty|forty|fifty|sixty|seventy|eighty|ninety|hundred|thousand|lakh|crore)\b', latest_msg, re.IGNORECASE))
    if not has_number:
        no_number_cases.append((row['thread_id'], row['supplier'], row['category'], latest_msg))
        
    if row['category'] in subscription_categories:
        # Check if month or year or billing period is mentioned
        has_period = bool(re.search(r'\b(month|monthly|year|yearly|annum|annual|annually)\b', latest_msg, re.IGNORECASE))
        if not has_period:
            no_period_cases.append((row['thread_id'], row['supplier'], row['category'], latest_msg))

print(f"No number cases ({len(no_number_cases)}):")
for tid, s, c, m in no_number_cases[:5]:
    print(f"[{tid}] {s} ({c}):\n{m}\n")

print(f"Subscription without period cases ({len(no_period_cases)}):")
for tid, s, c, m in no_period_cases[:5]:
    print(f"[{tid}] {s} ({c}):\n{m}\n")
