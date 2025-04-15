
import requests

def get_coin_price(coin_id):
    try:
        url = f"https://api.coingecko.com/api/v3/simple/price?ids={coin_id}&vs_currencies=usd"
        response = requests.get(url)
        response.raise_for_status()
        return response.json().get(coin_id, {}).get('usd', None)
    except Exception as e:
        print(f"Error fetching price: {e}")
        return None
