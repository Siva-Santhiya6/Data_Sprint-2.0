import re

text_t6 = "the best we can offer is two hundred sixty-six rupees per meal"
text_t50 = "we are pleased to quote $878.43 per laptop"
text_t66 = "we are pleased to quote €2.42 per shipment"
text_t76 = "our final price is £185.74 per guard per month"

# Let's write a robust currency and price parser
def parse_price_clause(text):
    # Detect currency
    curr = "INR"
    if re.search(r'[\$]|USD\b', text, re.IGNORECASE):
        curr = "USD"
    elif re.search(r'[€]|EUR\b', text, re.IGNORECASE):
        curr = "EUR"
    elif re.search(r'[£]|GBP\b', text, re.IGNORECASE):
        curr = "GBP"
    elif re.search(r'\b(SGD|AED|JPY|AUD|CAD|CHF|CNY)\b', text, re.IGNORECASE):
        curr = re.search(r'\b(SGD|AED|JPY|AUD|CAD|CHF|CNY)\b', text, re.IGNORECASE).group(1).upper()
    elif re.search(r'Rs\.?|₹|INR|rupees', text, re.IGNORECASE):
        curr = "INR"
        
    # Match the quote value before 'per', 'in total', or punctuation
    # Remove leading phrase like "we are pleased to quote", "best we can offer is", "final price is", "can do"
    m = re.search(r'(?:quote|can do|offer is|final price is|best we can offer is|can offer|read)\s*(?:between\s+)?(?:INR|USD|EUR|GBP|SGD|AED|JPY|Rs\.?|[₹\$€£])?\s*([^,\n]+?)(?:\s+per|\s+in total|\s+inclusive|\s+including|\s+\(GST|\.|\n|$)', text, re.IGNORECASE)
    val_str = m.group(1).strip() if m else None
    return curr, val_str

for t in [text_t6, text_t50, text_t66, text_t76]:
    c, v = parse_price_clause(t)
    print(f"Text: {t}\n -> Curr: {c}, Val: {v}\n")
