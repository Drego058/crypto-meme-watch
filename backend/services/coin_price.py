
import os
import requests
import time
import json
from dotenv import load_dotenv

load_dotenv()

CMC_API_KEY = os.getenv("COINMARKETCAP_API_KEY")
CMC_BASE_URL = "https://pro-api.coinmarketcap.com/v1"
CMC_HEADERS = {"X-CMC_PRO_API_KEY": CMC_API_KEY}

_price_cache = {}
_price_expiry = {}

CACHE_FILE = os.path.join(os.path.dirname(__file__), "../cache/coin_symbol_map.json")
_id_map = {}
_id_map_updated = 0

def update_symbol_id_map(force=False):
    global _id_map, _id_map_updated
    now = time.time()

    if not force and (now - _id_map_updated < 86400):
        return

    try:
        print("🔁 Updating CoinMarketCap symbol map...")
        res = requests.get(f"{CMC_BASE_URL}/cryptocurrency/map", headers=CMC_HEADERS)
        res.raise_for_status()
        coins = res.json()["data"]
        _id_map = {coin["symbol"].upper(): coin["id"] for coin in coins}
        _id_map_updated = now

        with open(CACHE_FILE, "w") as f:
            json.dump({"updated": now, "map": _id_map}, f)
    except Exception as e:
        print(f"⚠️ Error updating CoinMarketCap symbol map: {e}")
        # fallback op cache
        if os.path.exists(CACHE_FILE):
            with open(CACHE_FILE) as f:
                cached = json.load(f)
                _id_map = cached.get("map", {})
                _id_map_updated = cached.get("updated", now)

def is_valid_coin_id(symbol):
    update_symbol_id_map()
    return symbol.upper() in _id_map

def get_coin_prices_bulk(symbols):
    update_symbol_id_map()
    now = time.time()
    valid_symbols = [s for s in symbols if s.upper() in _id_map]
    uncached = [s for s in valid_symbols if s not in _price_cache or now > _price_expiry.get(s, 0)]
    prices = {}

    if uncached:
        symbol_str = ",".join(uncached)
        try:
            response = requests.get(
                f"{CMC_BASE_URL}/cryptocurrency/quotes/latest",
                headers=CMC_HEADERS,
                params={"symbol": symbol_str, "convert": "USD"}
            )
            response.raise_for_status()
            data = response.json()["data"]
            for s in uncached:
                price = data.get(s, {}).get("quote", {}).get("USD", {}).get("price")
                _price_cache[s] = price
                _price_expiry[s] = now + 60
        except Exception as e:
            print(f"Error fetching CoinMarketCap prices: {e}")

    for s in symbols:
        prices[s] = _price_cache.get(s)
    return prices

def get_coin_price_change_24h(symbol):
    try:
        response = requests.get(
            f"{CMC_BASE_URL}/cryptocurrency/quotes/latest",
            headers=CMC_HEADERS,
            params={"symbol": symbol, "convert": "USD"}
        )
        response.raise_for_status()
        data = response.json()["data"]
        change = data[symbol]["quote"]["USD"].get("percent_change_24h")
        return round(change, 2)
    except Exception as e:
        print(f"Error fetching 24h change (CMC): {e}")
    return None
