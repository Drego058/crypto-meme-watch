
# Voeg toe bovenin (extra import)
from services.coin_price import (
    get_coin_prices_bulk,
    get_coin_price_change_24h,
    get_sparkline,
    is_valid_coin_id,
    update_symbol_id_map
)

# Vervang binnen de verified append dit:
verified.append({
    "coin": symbol,
    "status": "verified",
    "mentions": mentions,
    "avg_sentiment": round(avg_sentiment, 3),
    "price": price,
    "change_24h": change,
    "sparkline": get_sparkline(symbol)
})

# Zorg dat de upcoming ook werkt zonder sparkline
upcoming.append({
    "coin": symbol,
    "status": "upcoming",
    "mentions": mentions,
    "avg_sentiment": round(avg_sentiment, 3),
    "price": None,
    "change_24h": None,
    "sparkline": []
})
