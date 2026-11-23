import pandas as pd
import re

threads = pd.read_csv("the-procurement-desk/threads.csv")

print("Checking currencies in test set...")
currencies = set()
for msg in threads['supplier_message']:
    found = re.findall(r'\b(INR|USD|EUR|GBP|JPY|AUD|CAD|CHF|CNY|SGD|HKD|NZD|SEK|KRW|AED|SAR|Rs\.?|₹)\b', msg, re.IGNORECASE)
    for c in found:
        currencies.add(c.upper())
print("Found currencies/symbols:", currencies)

print("\nChecking for words like bot, model, system, instruct, prompt, override, etc.")
bot_patterns = [
    r'bot', r'model', r'prompt', r'override', r'instruction', r'reviewer', r'ignore',
    r'assistant', r'system', r'cfo', r'signed off', r'approved', r'bypass'
]
suspicious_lines = []
for idx, row in threads.iterrows():
    msg = row['supplier_message']
    for pat in [r'bot\b', r'model\b', r'override\b', r'prompt\b', r'signed off\b', r'reviewer\b', r'ignore previous\b', r'bypass\b', r'disregard\b', r'system instructions\b', r'agent\b', r'language model\b', r'screening bot\b']:
        if re.search(pat, msg, re.IGNORECASE):
            suspicious_lines.append((row['thread_id'], pat, msg))
            break

print(f"Total threads with prompt-injection keywords: {len(suspicious_lines)}")
for tid, pat, m in suspicious_lines[:10]:
    print(f"[{tid}] (matched {pat}):\n{m}\n")
