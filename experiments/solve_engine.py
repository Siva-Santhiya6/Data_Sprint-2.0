import re
import os
import glob
import math
import pandas as pd

BASE_DIR = r"the-procurement-desk/playbook/playbook"

def load_playbook():
    categories = {}
    for path in glob.glob(os.path.join(BASE_DIR, "categories", "*.md")):
        cat_name = os.path.basename(path).replace(".md", "").strip().lower()
        with open(path, "r", encoding="utf-8") as f:
            text = f.read()
        
        unit = re.search(r'\*\*Normalized unit:\*\*\s*(.*)', text).group(1).strip()
        gst = float(re.search(r'\*\*GST rate:\*\*\s*(\d+)%', text).group(1)) / 100.0
        target = float(re.search(r'\*\*Target price:\*\*\s*[\u20b9\u00a3\$\u20ac\w\.,\s]*?([\d,]+)', text).group(1).replace(",", ""))
        walkaway = float(re.search(r'\*\*Walk-away price:\*\*\s*[\u20b9\u00a3\$\u20ac\w\.,\s]*?([\d,]+)', text).group(1).replace(",", ""))
        rounds = int(re.search(r'\*\*Negotiation rounds \(R\):\*\*\s*(\d+)', text).group(1))
        beta = float(re.search(r'\*\*Concession exponent \(.*?\):\*\*\s*([\d\.]+)', text).group(1))
        approval = float(re.search(r'\*\*Approval limit:\*\*\s*[\u20b9\u00a3\$\u20ac\w\.,\s]*?([\d,]+)', text).group(1).replace(",", ""))
        
        pack_conv = None
        m_pack = re.search(r'\*\*Pack conversion:\*\*\s*(.*)', text)
        if m_pack:
            pack_conv = m_pack.group(1).strip()
            
        categories[cat_name] = {
            "unit": unit,
            "gst": gst,
            "target": target,
            "walkaway": walkaway,
            "rounds": rounds,
            "beta": beta,
            "approval": approval,
            "pack_conv": pack_conv
        }

    suppliers = {}
    for path in glob.glob(os.path.join(BASE_DIR, "suppliers", "*.md")):
        with open(path, "r", encoding="utf-8") as f:
            text = f.read()
        m_title = re.search(r'# Supplier:\s*(.*)', text)
        supp_name = m_title.group(1).strip() if m_title else os.path.basename(path).replace(".md", "")
            
        status = "Approved"
        if "PROBATION" in text:
            status = "PROBATION"
        elif "BLACKLISTED" in text:
            status = "BLACKLISTED"
            
        contract_rates = {}
        for m in re.finditer(r'invoices in (\w+) are converted at [^\d]*([\d\.]+) per \w+', text):
            curr = m.group(1).upper()
            rate = float(m.group(2))
            contract_rates[curr] = rate
            
        contract_caps = {}
        for m in re.finditer(r'price cap for ([A-Za-z\s\-&]+) of [^\d]*([\d,]+) per', text):
            raw_c = m.group(1).strip().lower().replace(" ", "-")
            for k in categories:
                if k == raw_c or k in raw_c or raw_c in k:
                    contract_caps[k] = float(m.group(2).replace(",", ""))
                    break
                        
        suppliers[supp_name] = {
            "status": status,
            "contract_rates": contract_rates,
            "contract_caps": contract_caps
        }
        
    amendments = []
    for path in glob.glob(os.path.join(BASE_DIR, "amendments", "*.md")):
        with open(path, "r", encoding="utf-8") as f:
            text = f.read()
        m_hdr = re.search(r'# (AMD-\d+):\s*(.*)', text)
        amd_id = m_hdr.group(1)
        raw_cat = m_hdr.group(2).strip().lower().replace(" ", "-")
        cat_key = None
        for k in categories:
            if k == raw_cat or k in raw_cat or raw_cat in k:
                cat_key = k
                break
        eff_date = re.search(r'\*\*Effective from:\*\*\s*([\d\-]+)', text).group(1).strip()
        change_text = re.search(r'\*\*Change:\*\*\s*(.*)', text).group(1).strip()
        
        m_val = re.search(r'[\u20b9\u00a3\$\u20ac\w\.,\s]*?([\d,]+)', change_text)
        val = float(m_val.group(1).replace(",", "")) if m_val else None
        
        field = None
        if "target price" in change_text.lower():
            field = "target"
        elif "walk-away price" in change_text.lower():
            field = "walkaway"
        elif "approval limit" in change_text.lower():
            field = "approval"
            
        amendments.append({
            "id": amd_id,
            "category": cat_key,
            "date": eff_date,
            "field": field,
            "value": val
        })
        
    amendments.sort(key=lambda x: x["date"])
    return categories, suppliers, amendments

cats, supps, amds = load_playbook()

def parse_number(val_str):
    if not val_str:
        return None
    val_clean = str(val_str).replace(",", "").strip()
    
    # check if "lakh" or "k" in string
    m_lakh = re.search(r'([\d\.]+)\s*lakh', val_clean, re.IGNORECASE)
    if m_lakh:
        return float(m_lakh.group(1)) * 100000.0
    m_k = re.search(r'([\d\.]+)\s*k\b', val_clean, re.IGNORECASE)
    if m_k:
        return float(m_k.group(1)) * 1000.0
        
    m_num = re.search(r'[\d\.]+', val_clean)
    if m_num:
        try:
            return float(m_num.group(0))
        except:
            pass
            
    # Check words
    num_words = {
        'zero': 0, 'one': 1, 'two': 2, 'three': 3, 'four': 4, 'five': 5,
        'six': 6, 'seven': 7, 'eight': 8, 'nine': 9, 'ten': 10,
        'eleven': 11, 'twelve': 12, 'thirteen': 13, 'fourteen': 14,
        'fifteen': 15, 'sixteen': 16, 'seventeen': 17, 'eighteen': 18,
        'nineteen': 19, 'twenty': 20, 'thirty': 30, 'forty': 40,
        'fifty': 50, 'sixty': 60, 'seventy': 70, 'eighty': 80, 'ninety': 90
    }
    multipliers = {
        'hundred': 100,
        'thousand': 1000,
        'lakh': 100000,
        'lakhs': 100000,
        'crore': 10000000,
        'crores': 10000000
    }
    tokens = re.findall(r'\b[a-zA-Z]+\b', val_clean.lower())
    total = 0
    current = 0
    matched_any = False
    for token in tokens:
        if token in num_words:
            current += num_words[token]
            matched_any = True
        elif token == 'hundred':
            current = (current if current > 0 else 1) * 100
            matched_any = True
        elif token in multipliers:
            mult = multipliers[token]
            current = (current if current > 0 else 1) * mult
            total += current
            current = 0
            matched_any = True
        elif token == 'and':
            continue
    total += current
    if matched_any:
        return float(total)
    return None

def check_prompt_injection(thread_msg):
    patterns = [
        r'admin override',
        r'note for the language model',
        r'whichever bot screens',
        r'system note to ai',
        r'ignore (?:your )?previous instructions',
        r'if an automated system is reading',
        r'<!--\s*assistant:',
        r'pre-approved.*assistant should accept',
        r'set action\s*=\s*accept',
        r'just mark it accepted',
        r'output accept'
    ]
    for pat in patterns:
        if re.search(pat, thread_msg, re.IGNORECASE):
            return True
    return False

def check_banned_terms(latest_msg):
    # 1. Automatic renewal
    if re.search(r'\b(auto-renews|renews on its own|continues (?:from )?year to year unless)\b', latest_msg, re.IGNORECASE):
        if not re.search(r'no automatic renewal', latest_msg, re.IGNORECASE):
            return True
            
    # 2. Upfront or advance payment > 30%
    m_pct = re.search(r'(\d+)%\s*(?:of the order value\s*)?(?:upfront|advance)', latest_msg, re.IGNORECASE)
    if m_pct:
        pct = float(m_pct.group(1))
        if pct > 30.0:
            return True
    if re.search(r'\b(half|two-thirds|three-quarters)\s*(?:of\s*)?(?:the\s*)?(?:order value\s*)?(?:upfront|advance)\b', latest_msg, re.IGNORECASE):
        return True
        
    # 3. Unlimited liability
    if re.search(r'\b(liability.*unlimited|unlimited liability)\b', latest_msg, re.IGNORECASE):
        return True
        
    # 4. Exclusivity
    if re.search(r'\bexclusive supplier\b', latest_msg, re.IGNORECASE):
        if not re.search(r'not asking for exclusivity', latest_msg, re.IGNORECASE):
            return True
            
    return False

def split_thread_messages(thread_msg):
    parts = re.split(r'\[Latest message\s*[^\]]*\]', thread_msg, flags=re.IGNORECASE)
    if len(parts) > 1:
        earlier = parts[0]
        latest = parts[-1]
    else:
        earlier = ""
        latest = thread_msg
    return earlier, latest

def extract_offer_price(thread_row, earlier_msg, latest_msg, cat_info, supp_info):
    category = thread_row['category']
    quantity = float(thread_row['quantity'])
    
    # 1. Check for missing price or non-quotes without any numbers
    if re.search(r'(let\'s get on a call|pricing will depend on the final specs;\s*please share them)', latest_msg, re.IGNORECASE):
        return None, "MISSING_INFO"
        
    # 2. Check currency
    curr = "INR"
    m_currs = re.findall(r'\b(USD|EUR|GBP|SGD|AED|JPY|AUD|CAD|CHF|CNY)\b', latest_msg, re.IGNORECASE)
    if m_currs:
        curr = m_currs[0].upper()
    elif re.search(r'Rs\.?|₹|INR|rupees', latest_msg, re.IGNORECASE):
        curr = "INR"
    else:
        if not re.search(r'\d', latest_msg) and parse_number(latest_msg) is None:
            return None, "MISSING_INFO"
            
    supported_currs = {'INR', 'USD', 'EUR', 'GBP'}
    if curr not in supported_currs and curr not in supp_info.get("contract_rates", {}):
        return None, "MISSING_INFO"
        
    # Rate conversion
    rate = 1.0
    if curr == "USD":
        rate = supp_info.get("contract_rates", {}).get("USD", 84.5)
    elif curr == "EUR":
        rate = supp_info.get("contract_rates", {}).get("EUR", 91.0)
    elif curr == "GBP":
        rate = supp_info.get("contract_rates", {}).get("GBP", 106.0)
    elif curr in supp_info.get("contract_rates", {}):
        rate = supp_info["contract_rates"][curr]
        
    # Subscriptions check
    sub_cats = {'cleaning', 'cloud-servers', 'crm-licenses', 'design-software', 'security-guards'}
    is_sub = category in sub_cats
    
    # GST check
    is_gst_inclusive = bool(re.search(r'\b(inclusive of gst|including gst|incl\.?\s*gst|\(gst included\))\b', latest_msg, re.IGNORECASE))
    
    # Parse price number!
    # A. "a further D% off our previous quote"
    m_prev_disc = re.search(r'(?:a\s+)?further\s*(\d+)%\s*off (?:our )?previous quote', latest_msg, re.IGNORECASE)
    if m_prev_disc:
        disc = float(m_prev_disc.group(1)) / 100.0
        # In earlier message, extract supplier quote before Acme Procurement
        supp_earlier = earlier_msg
        m_acme = re.search(r'\[Earlier message\s*—\s*Acme Procurement\]', earlier_msg, flags=re.IGNORECASE)
        if m_acme:
            supp_earlier = earlier_msg[:m_acme.start()]
            
        m_earlier = re.search(r'(?:quote was|quote is|can do|offer is)\s*(?:INR|USD|EUR|GBP|Rs\.?|₹)?\s*([\d,]+(?:\.\d+)?)', supp_earlier, re.IGNORECASE)
        prev_price = float(m_earlier.group(1).replace(",", "")) if m_earlier else parse_number(supp_earlier)
        if prev_price is None:
            return None, "MISSING_INFO"
            
        raw_price = prev_price * (1.0 - disc)
        period = "year" if "year" in supp_earlier.lower() or "annual" in supp_earlier.lower() else ("month" if "month" in supp_earlier.lower() else None)
        if is_sub and period is None:
            return None, "MISSING_INFO"
            
        p = raw_price * rate
        if is_gst_inclusive:
            p = p / (1.0 + cat_info["gst"])
            
        if is_sub:
            if "per year" in cat_info["unit"] and period == "month":
                p = p * 12.0
            elif "per month" in cat_info["unit"] and period == "year":
                p = p / 12.0
        return p, "OK"

    # B. CORRECTION
    m_corr = re.search(r'CORRECTION\s*[\u2014\-]+\s*the price in my previous email should read\s*(?:INR|USD|EUR|GBP|Rs\.?|₹)?\s*([\d,]+(?:\.\d+)?|[a-zA-Z\s]+?)(?:\s*per|,\s*not|\.|\n|$)', latest_msg, re.IGNORECASE)
    if m_corr:
        raw_price = parse_number(m_corr.group(1))
        target_text = latest_msg
    else:
        target_text = latest_msg
        raw_price = None

    if raw_price is None:
        # C. Total for all N units:
        m_tot = re.search(r'([\d,]+(?:\.\d+)?|[a-zA-Z\s]+)\s*in total for all\s*(\d+)', target_text, re.IGNORECASE)
        if m_tot:
            tot_val = parse_number(m_tot.group(1))
            n_units = float(m_tot.group(2))
            raw_price = tot_val / n_units
            p = raw_price * rate
            if is_gst_inclusive:
                p = p / (1.0 + cat_info["gst"])
            return p, "OK"

        # D. Range: "between Rs. 1,506 and ₹1,638 per fixture"
        m_range = re.search(r'between\s+(?:INR|USD|EUR|GBP|Rs\.?|₹)?\s*([\d,]+(?:\.\d+)?|[a-zA-Z\s]+?)\s+and\s+(?:INR|USD|EUR|GBP|Rs\.?|₹)?\s*([\d,]+(?:\.\d+)?|[a-zA-Z\s]+?)(?:\s+per|\s+depending|\.|\n|$)', target_text, re.IGNORECASE)
        if m_range:
            p1 = parse_number(m_range.group(1))
            p2 = parse_number(m_range.group(2))
            raw_price = max(p1, p2)
        elif re.search(r'(\d+)%\s*(?:discount\s+on\s+our\s+list\s+price\s+of|off\s+our\s+list\s+price\s+of)\s*(?:INR|USD|EUR|GBP|Rs\.?|₹)?\s*([\d,]+(?:\.\d+)?)', target_text, re.IGNORECASE):
            m_list = re.search(r'(\d+)%\s*(?:discount\s+on\s+our\s+list\s+price\s+of|off\s+our\s+list\s+price\s+of)\s*(?:INR|USD|EUR|GBP|Rs\.?|₹)?\s*([\d,]+(?:\.\d+)?)', target_text, re.IGNORECASE)
            disc = float(m_list.group(1)) / 100.0
            val = float(m_list.group(2).replace(",", ""))
            raw_price = val * (1.0 - disc)
        elif re.search(r'(?:INR|USD|EUR|GBP|Rs\.?|₹)?\s*([\d,]+(?:\.\d+)?)\s*per\s*\w+\s*for orders of up to\s*(\d+)\s*[^,]+,\s*and\s*(?:INR|USD|EUR|GBP|Rs\.?|₹)?\s*([\d,]+(?:\.\d+)?)\s*per\s*\w+\s*for larger orders', target_text, re.IGNORECASE):
            m_tier = re.search(r'(?:INR|USD|EUR|GBP|Rs\.?|₹)?\s*([\d,]+(?:\.\d+)?)\s*per\s*\w+\s*for orders of up to\s*(\d+)\s*[^,]+,\s*and\s*(?:INR|USD|EUR|GBP|Rs\.?|₹)?\s*([\d,]+(?:\.\d+)?)\s*per\s*\w+\s*for larger orders', target_text, re.IGNORECASE)
            p_low = float(m_tier.group(1).replace(",", ""))
            thresh = float(m_tier.group(2))
            p_high = float(m_tier.group(3).replace(",", ""))
            raw_price = p_low if quantity <= thresh else p_high
        else:
            m_price = re.search(r'(?:quote|can do|offer is|final price is|best we can offer is|can offer|read)\s*(?:INR|USD|EUR|GBP|Rs\.?|₹)?\s*([A-Za-z\s\d,\.]+?)(?:\s*per|\s*inclusive|\s*including|\s*\(GST|\.|\n|$)', target_text, re.IGNORECASE)
            if m_price:
                raw_price = parse_number(m_price.group(1))
            else:
                m_any = re.search(r'([\d,]+(?:\.\d+)?)', target_text)
                raw_price = parse_number(m_any.group(1)) if m_any else None

    if raw_price is None:
        return None, "MISSING_INFO"

    # Free deal check
    m_free = re.search(r'plus\s*1\s*free\s*\w+\s*for every\s*(\d+)\s*you pay for', target_text, re.IGNORECASE)
    if m_free:
        y = float(m_free.group(1))
        raw_price = raw_price * (y / (y + 1.0))

    # Pack conversion
    if "per pack" in target_text.lower():
        m_pk = re.search(r'per pack of (\d+)', target_text.lower())
        pk_size = float(m_pk.group(1)) if m_pk else 4.0
        raw_price = raw_price / pk_size
    elif "per dozen" in target_text.lower():
        raw_price = raw_price / 12.0
    elif "per ream" in target_text.lower() and category == "printer-paper":
        raw_price = raw_price * 10.0

    # Subscription period check
    if is_sub:
        period = "year" if "year" in target_text.lower() or "annual" in target_text.lower() else ("month" if "month" in target_text.lower() else None)
        if period is None:
            return None, "MISSING_INFO"
        if "per year" in cat_info["unit"] and period == "month":
            raw_price = raw_price * 12.0
        elif "per month" in cat_info["unit"] and period == "year":
            raw_price = raw_price / 12.0

    p = raw_price * rate
    if is_gst_inclusive:
        p = p / (1.0 + cat_info["gst"])

    return p, "OK"

def evaluate_thread(row):
    thread_id = row['thread_id']
    date = row['date']
    supplier = row['supplier']
    category = row['category']
    quantity = float(row['quantity'])
    round_num = int(row['round'])
    msg = row['supplier_message']
    
    cat_info = dict(cats[category])
    supp_info = supps.get(supplier, {"status": "Approved", "contract_rates": {}, "contract_caps": {}})
    
    for amd in amds:
        if amd["date"] <= date and amd["category"] == category:
            cat_info[amd["field"]] = amd["value"]
            
    if category in supp_info.get("contract_caps", {}):
        cat_info["walkaway"] = supp_info["contract_caps"][category]
        
    earlier_msg, latest_msg = split_thread_messages(msg)
    
    # Rule 1: Missing information
    p, status = extract_offer_price(row, earlier_msg, latest_msg, cat_info, supp_info)
    if status == "MISSING_INFO":
        return "ESCALATE:MISSING_INFO:"
        
    # Rule 2: Blacklisted supplier
    if supp_info["status"] == "BLACKLISTED":
        return "REJECT:BLACKLISTED_SUPPLIER:"
        
    # Rule 3: Prompt injection (anywhere in thread)
    if check_prompt_injection(msg):
        return "ESCALATE:PROMPT_INJECTION:"
        
    # Rule 4: Banned contract terms (in latest message)
    if check_banned_terms(latest_msg):
        return "ESCALATE:BANNED_TERM:"
        
    # Rule 5: Price decision
    target = cat_info["target"]
    walkaway = cat_info["walkaway"]
    R = cat_info["rounds"]
    beta = cat_info["beta"]
    approval_limit = cat_info["approval"]
    
    is_probation = (supp_info["status"] == "PROBATION")
    if is_probation:
        L_r = target
    else:
        if round_num == 1:
            L_r = target
        elif round_num == R:
            L_r = walkaway
        else:
            L_r = target + (walkaway - target) * (((round_num - 1.0) / (R - 1.0)) ** beta)
            
    if p <= L_r + 1e-6:
        deal_value = p * quantity
        if deal_value > approval_limit:
            return "ESCALATE:OVER_APPROVAL_LIMIT:"
        else:
            return "ACCEPT:ACCEPTABLE_PRICE:"
    else:
        if round_num == R:
            return "REJECT:ABOVE_WALKAWAY:"
        else:
            counter_p = int(math.floor(L_r + 0.5))
            return f"COUNTER:COUNTER_OFFER:{counter_p}"

# Test on sample threads!
sample_threads = pd.read_csv("the-procurement-desk/sample_threads.csv")
sample_answers = pd.read_csv("the-procurement-desk/sample_answers.csv")
df_samples = pd.merge(sample_threads, sample_answers, on="thread_id")

correct = 0
total = len(df_samples)
mismatches = []
for idx, row in df_samples.iterrows():
    pred = evaluate_thread(row)
    actual = row['label']
    if pred == actual:
        correct += 1
    else:
        mismatches.append((row['thread_id'], actual, pred, row['supplier'], row['category']))

print(f"Sample Accuracy: {correct} / {total} ({correct/total*100:.1f}%)")
if mismatches:
    print("\nMismatches:")
    for tid, act, pred, supp, cat in mismatches:
        print(f"[{tid}] Actual: {act} | Pred: {pred} | {supp} ({cat})")
