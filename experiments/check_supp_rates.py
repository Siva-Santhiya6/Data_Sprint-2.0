import glob, os, re

for path in sorted(glob.glob("the-procurement-desk/playbook/playbook/suppliers/*.md")):
    with open(path, "r", encoding="utf-8") as f:
        text = f.read()
    if "converted at" in text.lower() or "exchange rate" in text.lower() or "usd" in text.lower() or "eur" in text.lower() or "gbp" in text.lower():
        print(f"=== {os.path.basename(path)} ===")
        for line in text.split('\n'):
            if any(k in line.lower() for k in ["converted", "rate", "usd", "eur", "gbp"]):
                print(" ", line)
