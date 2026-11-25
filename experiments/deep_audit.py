import pandas as pd
import re
import os
import glob

# 1. Check category pack conversions
print("=== CATEGORY PACK CONVERSIONS ===")
for p in glob.glob("the-procurement-desk/playbook/playbook/categories/*.md"):
    with open(p, "r", encoding="utf-8") as f:
        t = f.read()
    cat = os.path.basename(p).replace(".md", "")
    unit = re.search(r'\*\*Normalized unit:\*\*\s*(.*)', t)
    pack = re.search(r'\*\*Pack conversion:\*\*\s*(.*)', t)
    gst = re.search(r'\*\*GST rate:\*\*\s*(\d+)%', t)
    print(f"{cat}: unit={unit.group(1) if unit else None}, pack={pack.group(1) if pack else None}, gst={gst.group(1) if gst else None}%")

df = pd.read_csv("the-procurement-desk/threads.csv")
print(f"\nTotal test threads: {len(df)}")

# Check potential prompt injection phrases
print("\n=== POTENTIAL MISSED PROMPT INJECTIONS ===")
injection_keywords = [
    r'\boverride\b', r'\bapproval\b', r'\bapproved\b', r'\bsigned off\b',
    r'\binstruct\b', r'\bprompt\b', r'\bignore\b', r'\bforget\b',
    r'\bassistant\b', r'\bllm\b', r'\bmodel\b', r'\bbot\b', r'\bai\b',
    r'\bsecret\b', r'\bjailbreak\b', r'\brule\b', r'\bdirective\b'
]
matched_injections = []
for idx, row in df.iterrows():
    msg = row['supplier_message']
    for kw in injection_keywords:
        m = re.search(kw, msg, re.IGNORECASE)
        if m:
            matched_injections.append((row['thread_id'], kw, m.group(0), msg[:150]))
            break
print(f"Threads matching injection keywords: {len(matched_injections)}")
for t_id, kw, val, snippet in matched_injections[:15]:
    print(f"  {t_id} [{kw}]: {snippet.replace(chr(10), ' ')}")

# Check potential volume discounts
print("\n=== POTENTIAL VOLUME DISCOUNTS ===")
vol_patterns = [
    r'volume discount',
    r'discount (?:of|for|on) orders',
    r'for orders (?:of|over|above)',
    r'if you order (?:more than|at least)',
    r'order(?:ing)?\s+\d+\s+or more',
    r'buy\s+\d+'
]
matched_vol = []
for idx, row in df.iterrows():
    msg = row['supplier_message']
    for pat in vol_patterns:
        m = re.search(pat, msg, re.IGNORECASE)
        if m:
            matched_vol.append((row['thread_id'], pat, m.group(0), row['quantity'], msg[-200:]))
            break
print(f"Threads matching volume patterns: {len(matched_vol)}")
for t_id, pat, val, q, snippet in matched_vol[:10]:
    print(f"  {t_id} (qty={q}) [{pat}]: {snippet.replace(chr(10), ' ')}")
