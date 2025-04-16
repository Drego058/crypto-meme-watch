
import requests
import os

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

    symbols_str = ",".join(valid_symbols)
    try:
        url = f"{CMC_BASE}/cryptocurrency/quotes/latest?symbol={symbols_str}&convert=USD"
        res = requests.get(url, headers=CMC_HEADERS)
        data = res.json()["data"]
        for sym in valid_symbols:
            prices[sym] = data[sym]["quote"]["USD"]["price"]
        return prices
    except Exception as e:
        print("⚠️ CMC API failed, falling back to CoinGecko:", e)
        return fetch_prices_from_coingecko(valid_symbols)

def fetch_prices_from_coingecko(symbols):
    prices = {}
    try:
        for symbol in symbols:
            url = f"https://api.coingecko.com/api/v3/simple/price?ids={symbol.lower()}&vs_currencies=usd"
            res = requests.get(url)
            if res.status_code == 200:
                data = res.json()
                if symbol.lower() in data:
                    prices[symbol] = data[symbol.lower()]["usd"]
    except Exception as e:
        print("⚠️ CoinGecko fallback failed:", e)
    return prices

def get_coin_price_change_24h(symbol):
    try:
        url = f"{CMC_BASE}/cryptocurrency/quotes/latest?symbol={symbol}&convert=USD"
        res = requests.get(url, headers=CMC_HEADERS)
        data = res.json()
        return data["data"][symbol]["quote"]["USD"]["percent_change_24h"]
    except Exception as e:
        print(f"⚠️ CMC 24h change failed for {symbol}, trying CoinGecko:", e)
        return get_24h_change_from_coingecko(symbol)

def get_24h_change_from_coingecko(symbol):
    try:
        url = f"https://api.coingecko.com/api/v3/coins/{symbol.lower()}/market_chart?vs_currency=usd&days=1"
        res = requests.get(url)
        data = res.json()
        prices = data.get("prices", [])
        if len(prices) >= 2:
            start = prices[0][1]
            end = prices[-1][1]
            change = ((end - start) / start) * 100
            return round(change, 2)
    except Exception as e:
        print("⚠️ CoinGecko 24h fallback failed:", e)
    return None
