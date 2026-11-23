import pandas as pd
import re

threads = pd.read_csv("the-procurement-desk/threads.csv")

quotes = []
for idx, row in threads.iterrows():
    msg = row['supplier_message']
    parts = re.split(r'\[Latest message\s*[^\]]*\]', msg, flags=re.IGNORECASE)
    latest_msg = parts[-1] if len(parts) > 1 else msg
    
    # Check lines that contain quotes
    for line in latest_msg.split('\n'):
        line_s = line.strip()
        if not line_s: continue
        if re.search(r'\b(quote|offer|price|do|cost|discount|CORRECTION)\b', line_s, re.IGNORECASE):
            quotes.append(line_s)

print(f"Total quote lines in test set: {len(quotes)}")
# Check for words in quotes
word_number_quotes = [q for q in quotes if re.search(r'\b(one|two|three|four|five|six|seven|eight|nine|ten|twenty|thirty|forty|fifty|sixty|seventy|eighty|ninety|thousand|lakh)\b', q, re.IGNORECASE) and not re.search(r'\d', q)]
print(f"Quotes with numbers in words only ({len(word_number_quotes)}):")
for wq in set(word_number_quotes):
    print("  ->", repr(wq))
