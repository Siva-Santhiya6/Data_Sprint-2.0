from solve_engine import split_thread_messages, extract_offer_price, cats, supps, amds, parse_number
import pandas as pd
import re

threads = pd.read_csv("the-procurement-desk/threads.csv")

for tid in ['T10006', 'T10050', 'T10066', 'T10076']:
    row = threads[threads['thread_id'] == tid].iloc[0]
    earlier, latest = split_thread_messages(row['supplier_message'])
    cat_info = dict(cats[row['category']])
    supp_info = supps.get(row['supplier'], {})
    p, status = extract_offer_price(row, earlier, latest, cat_info, supp_info)
    print(f"\n[{tid}] Status: {status}, Price: {p}")
    print("Latest msg:", repr(latest))
