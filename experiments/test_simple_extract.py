import re
from solve_engine import parse_number

examples = [
    "we are pleased to quote Rs. 12,662 per monitor.",
    "the best we can offer is between Rs. 1,506 and ₹1,638 per fixture depending on final specs.",
    "we can do INR 3,870 per headset, not ₹3,483.",
    "the best we can offer is two hundred sixty-six rupees per meal.",
    "we are pleased to quote $878.43 per laptop.",
    "we are pleased to quote €2.42 per shipment.",
    "our final price is £185.74 per guard per month.",
    "our final price is eighty-seven thousand five hundred rupees per server per year.",
    "our revised offer is a 10% discount on our list price of INR 16,820 per monitor.",
    "our revised offer is a further 5% off our previous quote.",
    "quote ₹44,07,800 in total for all 60 laptops."
]

def extract_price_simple(line):
    # Check range
    m_range = re.search(r'between\s+(?:INR|USD|EUR|GBP|Rs\.?|[₹\$€£])?\s*([\d,]+(?:\.\d+)?|[a-zA-Z\s]+?)\s+and\s+(?:INR|USD|EUR|GBP|Rs\.?|[₹\$€£])?\s*([\d,]+(?:\.\d+)?|[a-zA-Z\s]+?)\s+per', line, re.IGNORECASE)
    if m_range:
        p1 = parse_number(m_range.group(1))
        p2 = parse_number(m_range.group(2))
        return max(p1, p2)
        
    # Check list price discount
    m_list = re.search(r'(\d+)%\s*(?:discount\s+on\s+our\s+list\s+price\s+of|off\s+our\s+list\s+price\s+of)\s*(?:INR|USD|EUR|GBP|Rs\.?|[₹\$€£])?\s*([\d,]+(?:\.\d+)?)', line, re.IGNORECASE)
    if m_list:
        disc = float(m_list.group(1)) / 100.0
        val = float(m_list.group(2).replace(",", ""))
        return val * (1.0 - disc)
        
    # Check total
    m_tot = re.search(r'(?:INR|USD|EUR|GBP|Rs\.?|[₹\$€£])?\s*([\d,]+(?:\.\d+)?|[a-zA-Z\s]+)\s*in total for all\s*(\d+)', line, re.IGNORECASE)
    if m_tot:
        val = parse_number(m_tot.group(1))
        n = float(m_tot.group(2))
        return val / n
        
    # Check price before "per"
    # Find word "per"
    m_per = re.search(r'(?:quote|can do|offer is|final price is|best we can offer is|can offer|read)\s*(?:between\s+)?(?:INR|USD|EUR|GBP|Rs\.?|[₹\$€£])?\s*(.*?)\s+per\b', line, re.IGNORECASE)
    if m_per:
        val_str = m_per.group(1).strip()
        # strip any leading currency
        val_str = re.sub(r'^(?:INR|USD|EUR|GBP|Rs\.?|[₹\$€£])\s*', '', val_str, flags=re.IGNORECASE)
        return parse_number(val_str)
        
    return None

for ex in examples:
    print(f"Ex: {ex}\n -> Extracted: {extract_price_simple(ex)}\n")
