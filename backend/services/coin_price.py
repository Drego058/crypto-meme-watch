
import requests
import time

def get_coin_prices(coin_ids):
    prices = {}
    if not coin_ids:
        return prices

    try:
        ids_str = ",".join(coin_ids)
        url = f"https://api.coingecko.com/api/v3/simple/price?ids={ids_str}&vs_currencies=usd"
        response = requests.get(url)
        if response.status_code == 429:
            print("Rate limit bereikt. Even wachten...")
            time.sleep(3)
            response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        for coin_id in coin_ids:
            prices[coin_id] = data.get(coin_id, {}).get('usd')
    except Exception as e:
        print(f"Error fetching prices: {e}")
    return prices
