import pandas as pd
threads = pd.read_csv("the-procurement-desk/threads.csv")
row = threads[threads['thread_id'] == 'T10092'].iloc[0]
print(row['supplier_message'])
