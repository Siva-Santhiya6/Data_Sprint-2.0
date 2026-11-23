import pandas as pd
from solve_engine_v3 import evaluate_thread, split_thread_messages
import re

threads = pd.read_csv("the-procurement-desk/threads.csv")

missing_info = []
for idx, row in threads.iterrows():
    pred = evaluate_thread(row)
    if pred == 'ESCALATE:MISSING_INFO:':
        earlier, latest = split_thread_messages(row['supplier_message'])
        missing_info.append((row['thread_id'], row['supplier'], row['category'], latest))

print(f"Total MISSING_INFO cases: {len(missing_info)}")

# Categorize reasons
reasons = {'unsupported_currency': 0, 'no_price_call_or_revert': 0, 'subscription_no_period': 0, 'other': []}

for tid, supp, cat, msg in missing_info:
    if re.search(r'\b(AED|SGD|JPY|AUD|CAD|CHF|CNY)\b', msg, re.IGNORECASE):
        reasons['unsupported_currency'] += 1
    elif re.search(r'(let\'s get on a call|pricing will depend on the final specs|share them and we will revert)', msg, re.IGNORECASE):
        reasons['no_price_call_or_revert'] += 1
    elif cat in {'cleaning', 'cloud-servers', 'crm-licenses', 'design-software', 'security-guards'} and not re.search(r'\b(month|monthly|year|yearly|annum|annual)\b', msg, re.IGNORECASE):
        reasons['subscription_no_period'] += 1
    else:
        reasons['other'].append((tid, supp, cat, msg))

print(f"Unsupported currencies: {reasons['unsupported_currency']}")
print(f"No price (call / revert): {reasons['no_price_call_or_revert']}")
print(f"Subscription without period: {reasons['subscription_no_period']}")
print(f"Other cases: {len(reasons['other'])}")
for o in reasons['other']:
    print("OTHER:", o)
