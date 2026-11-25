import urllib.request
import re
import json

url = 'https://docs.google.com/forms/d/e/1FAIpQLSdvZMyjqJroBfbq8vkosecYye0-gwZrwfEjT9_RejS7c1vnhA/viewform'
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
try:
    with urllib.request.urlopen(req) as resp:
        html = resp.read().decode('utf-8')
    
    match = re.search(r'FB_PUBLIC_LOAD_DATA_\s*=\s*(.+?);\s*</script>', html, re.DOTALL)
    if match:
        data = json.loads(match.group(1))
        print("TITLE:", data[1][8] if len(data[1]) > 8 else "Unknown")
        print("SUBTITLE:", data[1][0])
        print("="*60)
        items = data[1][1]
        for idx, item in enumerate(items):
            title = item[1]
            desc = item[2]
            itype = item[3] # type
            details = item[4] if len(item) > 4 else None
            is_req = False
            options = []
            if details and len(details) > 0:
                for d in details:
                    if len(d) > 2 and d[2] == 1:
                        is_req = True
                    if len(d) > 1 and d[1]:
                        options = [opt[0] for opt in d[1] if opt]
            req_str = "REQUIRED" if is_req else "OPTIONAL"
            print(f"[{idx+1}] {title} ({req_str}) [type={itype}]")
            if desc:
                print(f"    Description: {desc}")
            if options:
                print(f"    Options: {options}")
    else:
        print("FB_PUBLIC_LOAD_DATA_ not found!")
except Exception as e:
    import traceback
    traceback.print_exc()
