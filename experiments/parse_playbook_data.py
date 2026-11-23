import os
import glob
import re

base = r"the-procurement-desk/playbook/playbook"

print("--- SAMPLE CATEGORY (categories/laptops.md) ---")
with open(os.path.join(base, "categories", "laptops.md"), "r", encoding="utf-8") as f:
    print(f.read())

print("--- ALL CATEGORIES ---")
for c in sorted(glob.glob(os.path.join(base, "categories", "*.md"))):
    print(f"=== {os.path.basename(c)} ===")
    with open(c, "r", encoding="utf-8") as f:
        print(f.read())

print("--- ALL AMENDMENTS ---")
for a in sorted(glob.glob(os.path.join(base, "amendments", "*.md"))):
    print(f"=== {os.path.basename(a)} ===")
    with open(a, "r", encoding="utf-8") as f:
        print(f.read())

print("--- ALL SUPPLIERS (summarized) ---")
for s in sorted(glob.glob(os.path.join(base, "suppliers", "*.md"))):
    with open(s, "r", encoding="utf-8") as f:
        content = f.read().strip()
        print(f"{os.path.basename(s)}: {content}")
