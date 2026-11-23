from solve_engine import split_thread_messages, cats, supps, amds, parse_number
import pandas as pd
import re

threads = pd.read_csv("the-procurement-desk/threads.csv")

def debug_extract(thread_row):
    msg = thread_row['supplier_message']
    earlier_msg, latest_msg = split_thread_messages(msg)
    category = thread_row['category']
    quantity = float(thread_row['quantity'])
    cat_info = dict(cats[category])
    supp_info = supps.get(thread_row['supplier'], {})
    
    print("--- DEBUGGING THREAD", thread_row['thread_id'], "---")
    
    # 1. Check for missing price or generic non-quotes
    if re.search(r'(let\'s get on a call|pricing will depend on the final specs;\s*please share them)', latest_msg, re.IGNORECASE):
        print("Failed at step 1")
        return None, "MISSING_INFO"
        
    curr = "INR"
    m_currs = re.findall(r'\b(USD|EUR|GBP|SGD|AED|JPY|AUD|CAD|CHF|CNY)\b', latest_msg, re.IGNORECASE)
    if m_currs:
        curr = m_currs[0].upper()
    elif re.search(r'Rs\.?|₹|INR|rupees', latest_msg, re.IGNORECASE):
        curr = "INR"
    else:
        if not re.search(r'\d', latest_msg) and parse_number(latest_msg) is None:
            print("Failed at step 2 (no curr, no num)")
            return None, "MISSING_INFO"
            
    print("Detected currency:", curr)
    supported_currs = {'INR', 'USD', 'EUR', 'GBP'}
    if curr not in supported_currs and curr not in supp_info.get("contract_rates", {}):
        print("Failed at supported currs")
        return None, "MISSING_INFO"
        
    m_prev_disc = re.search(r'(?:a\s+)?further\s*(\d+)%\s*off (?:our )?previous quote', latest_msg, re.IGNORECASE)
    if m_prev_disc:
        print("Matched prev disc")
        
    m_corr = re.search(r'CORRECTION\s*[\u2014\-]+\s*the price in my previous email should read\s*(?:INR|USD|EUR|GBP|Rs\.?|₹)?\s*([\d,]+(?:\.\d+)?|[a-zA-Z\s]+?)(?:\s*per|,\s*not|\.|\n|$)', latest_msg, re.IGNORECASE)
    if m_corr:
        print("Matched corr")
        target_text = latest_msg
        raw_price = parse_number(m_corr.group(1))
    else:
        target_text = latest_msg
        raw_price = None
        
    print("raw_price after corr:", raw_price)
    
    if raw_price is None:
        m_tot = re.search(r'([\d,]+(?:\.\d+)?|[a-zA-Z\s]+)\s*in total for all\s*(\d+)', target_text, re.IGNORECASE)
        m_range = re.search(r'between\s+(?:INR|USD|EUR|GBP|Rs\.?|₹)?\s*([\d,]+(?:\.\d+)?|[a-zA-Z\s]+?)\s+and\s+(?:INR|USD|EUR|GBP|Rs\.?|₹)?\s*([\d,]+(?:\.\d+)?|[a-zA-Z\s]+?)(?:\s+per|\s+depending|\.|\n|$)', target_text, re.IGNORECASE)
        m_list = re.search(r'(\d+)%\s*(?:discount\s+on\s+our\s+list\s+price\s+of|off\s+our\s+list\s+price\s+of)\s*(?:INR|USD|EUR|GBP|Rs\.?|₹)?\s*([\d,]+(?:\.\d+)?)', target_text, re.IGNORECASE)
        m_tier = re.search(r'(?:INR|USD|EUR|GBP|Rs\.?|₹)?\s*([\d,]+(?:\.\d+)?)\s*per\s*\w+\s*for orders of up to\s*(\d+)\s*[^,]+,\s*and\s*(?:INR|USD|EUR|GBP|Rs\.?|₹)?\s*([\d,]+(?:\.\d+)?)\s*per\s*\w+\s*for larger orders', target_text, re.IGNORECASE)
        
        if m_tot: print("Matched m_tot")
        elif m_range: print("Matched m_range")
        elif m_list: print("Matched m_list")
        elif m_tier: print("Matched m_tier")
        else:
            m_price = re.search(r'(?:quote|can do|offer is|final price is|best we can offer is|can offer|read)\s*(?:INR|USD|EUR|GBP|Rs\.?|₹)?\s*([A-Za-z\s\d,\.]+?)(?:\s*per|\s*inclusive|\s*including|\s*\(GST|\.|\n|$)', target_text, re.IGNORECASE)
            print("m_price match:", m_price.group(0) if m_price else None)
            if m_price:
                print("m_price group 1:", repr(m_price.group(1)))
                raw_price = parse_number(m_price.group(1))
                print("parse_number(group 1):", raw_price)

    print("Final raw_price:", raw_price)

row_t6 = threads[threads['thread_id'] == 'T10006'].iloc[0]
debug_extract(row_t6)

row_t50 = threads[threads['thread_id'] == 'T10050'].iloc[0]
debug_extract(row_t50)
