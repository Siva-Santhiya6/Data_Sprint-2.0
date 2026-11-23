import re

text = "For the 50 monitors you requested, we are pleased to quote Rs. 12,662 per monitor."
m = re.search(r'(?:quote|can do|offer is|final price is|best we can offer is|can offer|read)\s*(?:between\s+)?(?:INR|USD|EUR|GBP|Rs\.?|[₹\$€£])?\s*([^,\n]+?)(?:\s+per|\s+in total|\s+inclusive|\s+including|\s+\(GST|[\r\n]|(?:\.\s+)|\.$|$)', text, re.IGNORECASE)
print("m:", m)
if m:
    print("group 0:", repr(m.group(0)))
    print("group 1:", repr(m.group(1)))
