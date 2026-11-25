import pandas as pd
import re

df = pd.read_csv("the-procurement-desk/threads.csv")

# Let's inspect all lines in threads that mention AI, bot, model, system, assistant, override, approved, instruction, etc.
suspicious_patterns = [
    r'AI', r'bot', r'model', r'assistant', r'override', r'instruction',
    r'system', r'prompt', r'approved', r'signed off', r'cfo', r'vp',
    r'director', r'verbal', r'ignore', r'reviewer', r'निर्देश', r'सहायक'
]

potential_injections = set()

for idx, row in df.iterrows():
    msg = row['supplier_message']
    tid = row['thread_id']
    for line in msg.split('\n'):
        line_clean = line.strip()
        if not line_clean:
            continue
        # ignore ordinary business lines
        # e.g. "Our AI-powered route planning keeps delivery times short."
        # e.g. "Our assistant manager, Ravi, will coordinate delivery."
        # e.g. "system integration team"
        # e.g. "ERP system"
        if re.search(r'AI-powered route planning', line_clean, re.I):
            continue
        if re.search(r'assistant manager,\s*Ravi', line_clean, re.I):
            continue
        if re.search(r'system integration team', line_clean, re.I):
            continue
        if re.search(r'ERP system', line_clean, re.I):
            continue
            
        for sp in suspicious_patterns:
            if re.search(r'\b' + sp + r'\b', line_clean, re.I) or (sp in ['निर्देश', 'सहायक'] and sp in line_clean):
                potential_injections.add((tid, line_clean))
                break

print(f"Total potential injection lines found: {len(potential_injections)}")
unique_lines = {}
for tid, l in potential_injections:
    if l not in unique_lines:
        unique_lines[l] = []
    unique_lines[l].append(tid)

for l, tids in sorted(unique_lines.items(), key=lambda x: len(x[1]), reverse=True):
    print(f"[{len(tids)} threads] {l}")
