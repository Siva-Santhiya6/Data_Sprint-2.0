import glob, os, re

for path in sorted(glob.glob("the-procurement-desk/playbook/playbook/amendments/*.md")):
    with open(path, "r", encoding="utf-8") as f:
        print(f"=== {os.path.basename(path)} ===")
        print(f.read())
