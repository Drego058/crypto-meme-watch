
# Meme Coin AI Dashboard Pro

AI-dashboard dat trending meme coins herkent op Reddit & X, sentiment analyseert en voorspelt welke coins kunnen stijgen of dalen.

## Features

- ✅ Realtime scraping van Reddit en X
- ✅ Sentimentanalyse met VADER
- ✅ Slimme coinherkenning ($PEPE, WAGMI, etc.)
- ✅ Trending score + hot coins
- ✅ Sparklines (laatste 7 dagen)
- ✅ Auto-refresh & demo fallback
- ✅ Responsive design met dark mode

## Installatie

```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --reload
```

Frontend: open `http://localhost:8000/`

## API Key

Plaats je CoinMarketCap key in `.env`:

```
COINMARKETCAP_API_KEY=your_key_here
```

## Deployment

Gebruik GitHub + Render. Frontend wordt meegeleverd via FastAPI.
