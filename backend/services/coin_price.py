
import requests
import time

_price_cache = {}
_price_expiry = {}
_known_ids = set()
_known_ids_last_updated = 0
_change_cache = {}
_change_expiry = {}

def update_known_coin_ids():
    global _known_ids, _known_ids_last_updated
    now = time.time()
    if now - _known_ids_last_updated < 3600:
        return

    try:
        url = "https://api.coingecko.com/api/v3/coins/list"
        response = requests.get(url)
        response.raise_for_status()
        coins = response.json()
        _known_ids = set(coin["id"] for coin in coins)
        _known_ids_last_updated = now
    except Exception as e:
        print(f"Error updating known coin IDs: {e}")

def is_valid_coin_id(coin_id):
    update_known_coin_ids()
    return coin_id in _known_ids

def get_coin_prices_bulk(coin_ids):
    now = time.time()
    valid_ids = [cid for cid in coin_ids if is_valid_coin_id(cid)]
    uncached_ids = [cid for cid in valid_ids if cid not in _price_cache or now > _price_expiry[cid]]
    prices = {}

    if uncached_ids:
        ids_str = ",".join(uncached_ids)
        try:
            url = f"https://api.coingecko.com/api/v3/simple/price?ids={ids_str}&vs_currencies=usd"
            response = requests.get(url)
            if response.status_code == 429:
                print("429 Too Many Requests - waiting...")
                time.sleep(5)
                response = requests.get(url)
            response.raise_for_status()
            data = response.json()
            for cid in uncached_ids:
                price = data.get(cid, {}).get("usd", None)
                _price_cache[cid] = price
                _price_expiry[cid] = now + 60
        except Exception as e:
            print(f"Error in bulk fetch: {e}")

    for cid in coin_ids:
        prices[cid] = _price_cache.get(cid) if cid in _price_cache else None
    return prices

def get_coin_price_change_24h(coin_id, allow=True):
    now = time.time()
    if coin_id in _change_cache and now < _change_expiry.get(coin_id, 0):
        return _change_cache[coin_id]

    if not allow:
        return None

    try:
        url = f"https://api.coingecko.com/api/v3/coins/{coin_id}/market_chart?vs_currency=usd&days=1"
        response = requests.get(url)
        if response.status_code == 429:
            print("429 Too Many Requests (chart) - waiting...")
            time.sleep(5)
            response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        prices = data.get("prices", [])
        if len(prices) >= 2:
            start_price = prices[0][1]
            end_price = prices[-1][1]
            change = ((end_price - start_price) / start_price) * 100
            _change_cache[coin_id] = round(change, 2)
            _change_expiry[coin_id] = now + 3600
            return _change_cache[coin_id]
    except Exception as e:
        print(f"Error fetching 24h price change: {e}")
    return None
