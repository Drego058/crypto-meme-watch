
import requests
import time

_cache = {}
_cache_expiry = {}

def get_coin_price(coin_id):
    now = time.time()
    if coin_id in _cache and now < _cache_expiry[coin_id]:
        return _cache[coin_id]

    try:
        url = f"https://api.coingecko.com/api/v3/simple/price?ids={coin_id}&vs_currencies=usd"
        print(f"Fetching price from: {url}")
        response = requests.get(url)
        if response.status_code == 429:
            print("429 Too Many Requests - waiting before retry...")
            time.sleep(5)
            response = requests.get(url)
        response.raise_for_status()
        data = response.json().get(coin_id, {}).get("usd", None)
        _cache[coin_id] = data
        _cache_expiry[coin_id] = now + 60  # cache 1 minuut
        return data
    except Exception as e:
        print(f"Error fetching price for {coin_id}: {e}")
        return None
