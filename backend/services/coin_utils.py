
import re
import requests

def extract_coin_mentions(text):
    matches = re.findall(r'\$?[A-Z]{2,5}', text)
    return list(set([m.replace("$", "") for m in matches if len(m) <= 5]))

def fetch_coin_prices(symbols):
    prices = {}
    ids_map = {
        'PEPE': 'pepe',
        'DOGE': 'dogecoin',
        'WIF': 'dogwifhat',
        'SHIB': 'shiba-inu'
    }
    for symbol in symbols:
        coin_id = ids_map.get(symbol.upper())
        if coin_id:
            try:
                res = requests.get(f"https://api.coingecko.com/api/v3/simple/price?ids={coin_id}&vs_currencies=usd")
                data = res.json()
                prices[symbol.lower()] = data[coin_id]['usd']
            except:
                prices[symbol.lower()] = None
        else:
            prices[symbol.lower()] = None
    return prices
