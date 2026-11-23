import pandas as pd
import re

threads = pd.read_csv("the-procurement-desk/threads.csv")

# Let's inspect all lines in all messages that contain any keywords related to:
# bot, model, system, agent, override, admin, prompt, cfo, sign, approve, language, instruct, ignore
injection_lines = []
for idx, row in threads.iterrows():
    msg = row['supplier_message']
    lines = msg.split('\n')
    for line in lines:
        line_clean = line.strip()
        if not line_clean:
            continue
        # Check if line matches injection-like patterns
        if re.search(r'\b(bot|prompt|override|language model|admin|cfo|pre-approved|signed off|whichever bot|system note)\b', line_clean, re.IGNORECASE):
            # Exclude legitimate business: "ERP system", "route planning", "assistant manager", etc.
            injection_lines.append((row['thread_id'], line_clean))

print(f"Total matching lines: {len(injection_lines)}")
unique_patterns = set(l[1] for l in injection_lines)
print(f"Unique matching lines ({len(unique_patterns)}):")
for u in sorted(unique_patterns):
    print("  ->", repr(u))
