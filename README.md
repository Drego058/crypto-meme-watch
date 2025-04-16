
# Meme Coin AI Project (Pushshift-free)

✅ 100% werkende versie zonder gebruik van Pushshift API.

## Features:
- Realtime scraping via `snscrape` (Reddit + X)
- CoinMarketCap + CoinGecko fallback voor prijsdata
- Responsive frontend met dark mode, sentimentfilter, auto-refresh

## Installatie

```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --reload
```

Open in browser: http://localhost:8000/

## Belangrijk
Zorg dat je een `.env` bestand hebt met:
COINMARKETCAP_API_KEY=your_key_here

## Render deploy
1. Zet je API key in "Environment"
2. Manual Deploy > Clear Cache > Deploy

Klaar!
