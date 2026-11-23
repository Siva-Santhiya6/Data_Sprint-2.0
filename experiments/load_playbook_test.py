import re
import os
import glob
import math
import pandas as pd

# Load playbook definitions
BASE_DIR = r"the-procurement-desk/playbook/playbook"

def load_playbook():
    categories = {}
    for path in glob.glob(os.path.join(BASE_DIR, "categories", "*.md")):
        cat_name = os.path.basename(path).replace(".md", "")
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
        supp_name = None
        with open(path, "r", encoding="utf-8") as f:
            text = f.read()
        m_title = re.search(r'# Supplier:\s*(.*)', text)
        if m_title:
            supp_name = m_title.group(1).strip()
        else:
            supp_name = os.path.basename(path).replace(".md", "")
            
        status = "Approved"
        if "PROBATION" in text:
            status = "PROBATION"
        elif "BLACKLISTED" in text:
            status = "BLACKLISTED"
            
        contract_rates = {}
        # e.g., invoices in GBP are converted at ₹104.5 per GBP
        for m in re.finditer(r'invoices in (\w+) are converted at [^\d]*([\d\.]+) per \w+', text):
            curr = m.group(1).upper()
            rate = float(m.group(2))
            contract_rates[curr] = rate
            
        contract_caps = {}
        # e.g., price cap for Catering of ₹400 per meal (replaces the walk-away price)
        for m in re.finditer(r'price cap for ([A-Za-z\s\-]+) of [^\d]*([\d,]+) per', text):
            cat_cap = m.group(1).strip().lower().replace(" ", "-")
            # map name to category key
            for k in categories:
                if k in cat_cap or cat_cap in k or cat_cap.replace(" ", "-") == k:
                    contract_caps[k] = float(m.group(2).replace(",", ""))
                    break
            else:
                # Direct check
                norm_cat = cat_cap.replace("services", "").replace("workshops", "").strip().replace(" ", "-")
                for k in categories:
                    if norm_cat in k or k in norm_cat:
                        contract_caps[k] = float(m.group(2).replace(",", ""))
                        
        suppliers[supp_name] = {
            "status": status,
            "contract_rates": contract_rates,
            "contract_caps": contract_caps
        }
        
    amendments = []
    for path in glob.glob(os.path.join(BASE_DIR, "amendments", "*.md")):
        with open(path, "r", encoding="utf-8") as f:
            text = f.read()
        # Header has category name
        m_hdr = re.search(r'# (AMD-\d+):\s*(.*)', text)
        amd_id = m_hdr.group(1)
        raw_cat = m_hdr.group(2).strip().lower()
        cat_key = None
        for k in categories:
            if k in raw_cat or raw_cat.replace("services", "").strip() in k:
                cat_key = k
                break
        eff_date = re.search(r'\*\*Effective from:\*\*\s*([\d\-]+)', text).group(1).strip()
        change_text = re.search(r'\*\*Change:\*\*\s*(.*)', text).group(1).strip()
        
        # parse change: target price, walk-away price, approval limit
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
print(f"Loaded {len(cats)} categories, {len(supps)} suppliers, {len(amds)} amendments.")
print("Suppliers loaded:", list(supps.keys())[:5])
print("Amendments loaded:", amds)
