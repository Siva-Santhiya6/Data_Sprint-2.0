import sys
import os
sys.path.insert(0, os.path.abspath("."))
import pandas as pd
from solve_v2 import load_playbook, evaluate_thread, split_thread_messages, extract_offer_price

cats, supps, amds = load_playbook("the-procurement-desk/playbook/playbook")
threads = pd.read_csv("the-procurement-desk/threads.csv")

row = threads[threads['thread_id'] == 'T10225'].iloc[0]
print("Row:\n", row)
cat_info = dict(cats[row['category']])
supp_info = supps.get(row['supplier'], {})
print("\nInitial cat_info:", cat_info)
print("supp_info:", supp_info)

for amd in amds:
    if amd["date"] <= row['date'] and amd["category"] == row['category']:
        print("Applying amendment:", amd)
        cat_info[amd["field"]] = amd["value"]

if row['category'] in supp_info.get("contract_caps", {}):
    cat_info["walkaway"] = supp_info["contract_caps"][row['category']]
    print("Applied contract cap walkaway:", cat_info["walkaway"])

earlier, latest = split_thread_messages(row['supplier_message'])
p, status = extract_offer_price(row, earlier, latest, cat_info, supp_info)
print(f"Extracted p: {p}, status: {status}")
print(f"p * quantity: {p * float(row['quantity'])}")
print(f"Approval limit: {cat_info['approval']}")
print(f"Walkaway L(r): {cat_info['walkaway']}")

print("Result from evaluate_thread:", evaluate_thread(row, cats, supps, amds))
