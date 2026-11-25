import pandas as pd
import re
import glob
import os

df = pd.read_csv("the-procurement-desk/threads.csv")

# 1. Check all banned term matches
banned_phrases = [
    r'auto-renew', r'renews on its own', r'continues (?:from )?year to year unless',
    r'automatic renewal', r'unlimited liability', r'liability.*unlimited',
    r'exclusive supplier', r'exclusivity', r'upfront', r'advance'
]

print("=== BANNED TERMS AUDIT ===")
banned_threads = []
for idx, row in df.iterrows():
    msg = row['supplier_message']
    parts = re.split(r'\[Latest message\s*[^\]]*\]', msg, flags=re.I)
    latest = parts[-1] if len(parts) > 1 else msg
    for bp in banned_phrases:
        if re.search(bp, latest, re.I):
            # check exceptions
            if "not asking for exclusivity" in latest.lower():
                continue
            if "no automatic renewal" in latest.lower():
                continue
            # advance check: only > 30%
            m_pct = re.search(r'(\d+)%\s*(?:of the order value\s*)?(?:upfront|advance)', latest, re.I)
            if m_pct and float(m_pct.group(1)) <= 30.0 and not any(re.search(p, latest, re.I) for p in [r'auto-renew', r'unlimited liability', r'exclusive supplier']):
                continue
            banned_threads.append((row['thread_id'], bp, latest[-150:]))
            break
print(f"Banned threads found: {len(banned_threads)}")

# 2. Check all missing info
print("=== MISSING INFO AUDIT ===")
missing_threads = []
sub_cats = {'cleaning', 'cloud-servers', 'crm-licenses', 'design-software', 'security-guards'}
for idx, row in df.iterrows():
    msg = row['supplier_message']
    parts = re.split(r'\[Latest message\s*[^\]]*\]', msg, flags=re.I)
    latest = parts[-1] if len(parts) > 1 else msg
    
    # Non-quotes
    if re.search(r'(let\'s get on a call|pricing will depend on the final specs;\s*please share them)', latest, re.I):
        missing_threads.append((row['thread_id'], "Non-quote"))
        continue
    # Unsupported currency
    if re.search(r'\b(SGD|AED|JPY|AUD|CAD|CHF|CNY)\b', latest, re.I):
        # check if contract rates exist
        missing_threads.append((row['thread_id'], "Unsupported currency"))
        continue
    # Subscriptions missing period
    if row['category'] in sub_cats:
        if not re.search(r'\b(month|year|annual|monthly|annually)\b', latest, re.I):
            # check if previous quote discount had period
            missing_threads.append((row['thread_id'], "Subscription missing period"))

print(f"Missing info threads found: {len(missing_threads)}")
