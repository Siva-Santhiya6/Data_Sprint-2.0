import sys, os
sys.path.insert(0, os.path.abspath("."))
import pandas as pd
from solve_v2 import load_playbook, split_thread_messages

cats, supps, amds = load_playbook()
threads = pd.read_csv("the-procurement-desk/threads.csv")
row = threads[threads['thread_id'] == 'T10079'].iloc[0]

earlier, latest = split_thread_messages(row['supplier_message'])
print("Latest msg:\n", latest)

from experiments.test_solver_updates import extract_offer_price
p, status = extract_offer_price(row, earlier, latest, cats[row['category']], supps.get(row['supplier'], {}))
print("Extracted p:", p)
print("Round:", row['round'], "Category:", row['category'])
