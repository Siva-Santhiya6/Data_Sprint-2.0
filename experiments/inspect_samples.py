import pandas as pd

threads = pd.read_csv("the-procurement-desk/sample_threads.csv")
answers = pd.read_csv("the-procurement-desk/sample_answers.csv")
df = pd.merge(threads, answers, on="thread_id")

for idx, row in df.iterrows():
    print(f"==================================================")
    print(f"THREAD: {row['thread_id']} | DATE: {row['date']} | ROUND: {row['round']} | OUR_LAST: {row['our_last_counter']}")
    print(f"SUPPLIER: {row['supplier']} | CATEGORY: {row['category']} | QTY: {row['quantity']}")
    print(f"LABEL: {row['label']}")
    print(f"MESSAGE:\n{row['supplier_message']}")
