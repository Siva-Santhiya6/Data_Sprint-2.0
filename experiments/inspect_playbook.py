import os
import glob
import pandas as pd

base = r"the-procurement-desk/playbook/playbook"
categories = glob.glob(os.path.join(base, "categories", "*.md"))
suppliers = glob.glob(os.path.join(base, "suppliers", "*.md"))
amendments = glob.glob(os.path.join(base, "amendments", "*.md"))
precedents = glob.glob(os.path.join(base, "precedents", "*.md"))

print(f"Categories ({len(categories)}):", [os.path.basename(c) for c in categories])
print(f"Suppliers ({len(suppliers)}):", [os.path.basename(s) for s in suppliers])
print(f"Amendments ({len(amendments)}):", [os.path.basename(a) for a in amendments])
print(f"Precedents ({len(precedents)}):", [os.path.basename(p) for p in precedents])

sample_threads = pd.read_csv("the-procurement-desk/sample_threads.csv")
sample_answers = pd.read_csv("the-procurement-desk/sample_answers.csv")
print(f"Sample threads shape: {sample_threads.shape}")
print(f"Sample answers shape: {sample_answers.shape}")

threads = pd.read_csv("the-procurement-desk/threads.csv")
print(f"Test threads shape: {threads.shape}")
