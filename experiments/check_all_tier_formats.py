import pandas as pd
import re

df = pd.read_csv("the-procurement-desk/threads.csv")

patterns_seen = {
    "total_for_all": 0,
    "range": 0,
    "list_price_discount": 0,
    "discount_on_prev": 0,
    "correction": 0,
    "tiers_up_to": 0,
    "volume_further_off": 0,
    "free_per_every": 0,
    "pack_of": 0,
    "dozen": 0,
    "ream": 0,
    "standard_per": 0,
    "unmatched": 0
}

unmatched_threads = []

for idx, row in df.iterrows():
    msg = row['supplier_message']
    parts = re.split(r'\[Latest message\s*[^\]]*\]', msg, flags=re.I)
    latest = parts[-1] if len(parts) > 1 else msg
    
    matched = False
    if re.search(r'in total for all\s*\d+', latest, re.I):
        patterns_seen["total_for_all"] += 1
        matched = True
    if re.search(r'between.*and.*per', latest, re.I):
        patterns_seen["range"] += 1
        matched = True
    if re.search(r'\d+%\s*(?:discount on our list price|off our list price)', latest, re.I):
        patterns_seen["list_price_discount"] += 1
        matched = True
    if re.search(r'\d+%\s*off (?:our )?previous quote', latest, re.I):
        patterns_seen["discount_on_prev"] += 1
        matched = True
    if re.search(r'CORRECTION', latest, re.I):
        patterns_seen["correction"] += 1
        matched = True
    if re.search(r'orders of up to\s*\d+', latest, re.I):
        patterns_seen["tiers_up_to"] += 1
        matched = True
    if re.search(r'with a further\s*\d+%\s*off for orders of', latest, re.I):
        patterns_seen["volume_further_off"] += 1
        matched = True
    if re.search(r'plus\s*1\s*free', latest, re.I):
        patterns_seen["free_per_every"] += 1
        matched = True
    if re.search(r'per pack of', latest, re.I):
        patterns_seen["pack_of"] += 1
        matched = True
    if re.search(r'per dozen', latest, re.I):
        patterns_seen["dozen"] += 1
        matched = True
    if re.search(r'per ream', latest, re.I):
        patterns_seen["ream"] += 1
        matched = True
    if re.search(r'per\s+\w+', latest, re.I):
        patterns_seen["standard_per"] += 1
        matched = True
        
    if not matched:
        patterns_seen["unmatched"] += 1
        unmatched_threads.append((row['thread_id'], row['category'], latest))

print("Pattern counts:")
for k, v in patterns_seen.items():
    print(f"  {k}: {v}")

print(f"\nUnmatched count: {len(unmatched_threads)}")
for ut in unmatched_threads[:10]:
    print(f"{ut[0]} ({ut[1]}): {ut[2][:100]}")
