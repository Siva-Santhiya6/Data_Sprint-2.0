import pandas as pd
from solve_engine import split_thread_messages, extract_offer_price, cats, supps, amds, check_prompt_injection, check_banned_terms

threads = pd.read_csv("the-procurement-desk/sample_threads.csv")
answers = pd.read_csv("the-procurement-desk/sample_answers.csv")
df = pd.merge(threads, answers, on="thread_id")

for target_id in ['T00002', 'T00007', 'T00017', 'T00028', 'T00036']:
    row = df[df['thread_id'] == target_id].iloc[0]
    earlier, latest = split_thread_messages(row['supplier_message'])
    cat_info = dict(cats[row['category']])
    supp_info = supps.get(row['supplier'], {})
    p, status = extract_offer_price(row, earlier, latest, cat_info, supp_info)
    print(f"\n=== {target_id} ({row['supplier']}, {row['category']}, r={row['round']}) ===")
    print("Earlier:\n", repr(earlier))
    print("Latest:\n", repr(latest))
    print(f"Extracted p: {p}, status: {status}")
