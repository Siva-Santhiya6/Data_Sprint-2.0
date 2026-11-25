import glob, os

files = glob.glob("the-procurement-desk/playbook/playbook/policies/*.md") + glob.glob("the-procurement-desk/playbook/playbook/precedents/*.md")
for fpath in files:
    print(f"\n{'='*20} {fpath} {'='*20}")
    with open(fpath, "r", encoding="utf-8") as f:
        print(f.read())
