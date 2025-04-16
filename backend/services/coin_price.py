
import requests
import os
import time

CMC_API_KEY = os.getenv("COINMARKETCAP_API_KEY")
CMC_HEADERS = {"X-CMC_PRO_API_KEY": CMC_API_KEY}
CMC_BASE = "https://pro-api.coinmarketcap.com/v1"

symbol_to_id = {}

def update_symbol_id_map():
    global symbol_to_id
    try:
        url = f"{CMC_BASE}/cryptocurrency/map"
        response = requests.get(url, headers=CMC_HEADERS)
        data = response.json()
        symbol_to_id = {entry["symbol"]: entry["id"] for entry in data["data"]}
    except Exception as e:
        print("⚠️ Error updating CoinMarketCap symbol map:", e)

def is_valid_coin_id(symbol):
    return symbol in symbol_to_id

def get_coin_prices_bulk(symbols):
    prices = {}
    valid_symbols = [s for s in symbols if s in symbol_to_id]
    if not valid_symbols:
        return prices
    chunks = [valid_symbols[i:i + 10] for i in range(0, len(valid_symbols), 10)]
    for chunk in chunks:
        symbols_str = ",".join(chunk)
        url = f"{CMC_BASE}/cryptocurrency/quotes/latest?symbol={symbols_str}&convert=USD"
        try:
            res = requests.get(url, headers=CMC_HEADERS)
            data = res.json()["data"]
            for sym in chunk:
                prices[sym] = data[sym]["quote"]["USD"]["price"]
        except Exception as e:
            print(f"Error fetching price chunk: {e}")
    return prices

def get_coin_price_change_24h(symbol):
    try:
        url = f"{CMC_BASE}/cryptocurrency/quotes/latest?symbol={symbol}&convert=USD"
        res = requests.get(url, headers=CMC_HEADERS)
        data = res.json()
        return data["data"][symbol]["quote"]["USD"]["percent_change_24h"]
    except Exception as e:
        print(f"Error fetching 24h change for {symbol}:", e)
        return None
