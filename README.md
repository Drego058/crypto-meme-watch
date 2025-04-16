
# Meme Coin AI Dashboard

Volledig werkende meme coin AI-tracker met sentiment, scraping, trending analyse en fallback.

## Inhoud

- ✅ FastAPI backend met snscrape (géén Pushshift)
- ✅ CoinMarketCap + CoinGecko fallback voor prijsdata
- ✅ Frontend met filters, dark mode, mobielvriendelijk

## Installatie

```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --reload
```

Open in browser: http://localhost:8000/

## Render-deploy
1. Zet COINMARKETCAP_API_KEY in Environment
2. Upload deze bestanden naar GitHub en link je repo
3. Klik op "Manual Deploy" > Clear Cache > Deploy

Enjoy!
