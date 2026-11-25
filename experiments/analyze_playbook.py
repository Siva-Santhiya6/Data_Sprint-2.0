import os

base = "the-procurement-desk"
for root, dirs, files in os.walk(base):
    for f in files:
        if f.endswith(('.md', '.txt', '.json')):
            rel = os.path.relpath(os.path.join(root, f), base)
            print(f"File: {rel}")
