import glob, os, re

for path in sorted(glob.glob("the-procurement-desk/playbook/playbook/suppliers/*.md")):
    with open(path, "r", encoding="utf-8") as f:
        text = f.read()
    if "price cap" in text.lower():
        print(f"=== {os.path.basename(path)} ===")
        print(text)
