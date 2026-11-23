import re

def test_t00036():
    text = "For the 60 monitors you requested, our revised offer is a 10% discount on our list price of INR 16,820 per monitor."
    m_list = re.search(r'(\d+)%\s*(?:discount\s+on\s+our\s+list\s+price\s+of|off\s+our\s+list\s+price\s+of)\s*(?:INR|USD|EUR|GBP|Rs\.?|₹)?\s*([\d,]+(?:\.\d+)?)', text, re.IGNORECASE)
    if m_list:
        disc = float(m_list.group(1)) / 100.0
        val = float(m_list.group(2).replace(",", ""))
        p = val * (1.0 - disc)
        print("T00036 price:", p)

test_t00036()
