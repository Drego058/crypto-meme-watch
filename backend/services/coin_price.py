
# Voeg aan het eind toe: extra functie om sparkline data op te halen via CoinGecko
def get_sparkline(symbol):
    try:
        cg_map = load_coingecko_symbol_map()
        cg_id = cg_map.get(symbol.upper())
        if not cg_id:
            return []
        res = requests.get(f"{CG_BASE_URL}/coins/{cg_id}/market_chart", params={"vs_currency": "usd", "days": 7})
        res.raise_for_status()
        data = res.json()
        prices = [round(p[1], 4) for p in data.get("prices", [])]
        return prices
    except Exception as e:
        print(f"⚠️ Error fetching sparkline for {symbol}: {e}")
        return []
