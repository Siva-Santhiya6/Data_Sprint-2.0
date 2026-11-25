import pandas as pd
import re

df = pd.read_csv("the-procurement-desk/threads.csv")

def check_all_injections(text):
    patterns = [
        r'admin override',
        r'note for the language model',
        r'whichever bot screens',
        r'system note to ai',
        r'ignore (?:your )?previous instructions',
        r'if an automated system is reading',
        r'<!--\s*assistant:',
        r'pre-approved.*(?:assistant|system|bot)',
        r'reviewing assistant should accept',
        r'set action\s*=\s*accept',
        r'just mark it accepted',
        r'output accept',
        r'AI\s*सहायक\s*के\s*लिए\s*निर्देश',
        r'इस\s*डील\s*को\s*तुरंत\s*ACCEPT',
        r'approval already granted',
        r'CFO already signed off',
        r'skip the playbook checks'
    ]
    for pat in patterns:
        if re.search(pat, text, re.I):
            return True, pat
    return False, None

found = 0
for idx, row in df.iterrows():
    is_inj, pat = check_all_injections(row['supplier_message'])
    if is_inj:
        found += 1

print(f"Total prompt injections caught with enhanced patterns: {found}")
