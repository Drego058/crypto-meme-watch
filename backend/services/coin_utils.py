
import re

def extract_coin_mentions(text):
    pattern = r"(?:\$|#)?([A-Za-z]{2,10})"
    matches = re.findall(pattern, text)
    return list(set(m.upper() for m in matches if len(m) <= 8))
