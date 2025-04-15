
import re

def extract_coin_mentions(text):
    matches = re.findall(r'\$?[A-Z]{2,5}', text)
    return list(set([m.replace("$", "") for m in matches if len(m) <= 5]))
