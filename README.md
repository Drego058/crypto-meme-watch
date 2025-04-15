
# Meme Coin AI Dashboard

Deze applicatie zoekt automatisch naar meme coins op Reddit/X, analyseert sentiment, en toont trending coins.

## Functies

- 🔍 Herkenning van meme coins in posts
- 🤖 Sentimentanalyse per coin
- 💹 Live prijzen + 24h trends via CoinMarketCap API
- 🚀 Automatische herkenning van upcoming coins
- 📊 Dashboard met visuele weergave

## Installatie

1. Clone de repo:
```bash
git clone https://github.com/jouw-gebruiker/je-repo.git
cd je-repo/backend
```

2. Installeer requirements:
```bash
pip install -r requirements.txt
```

3. Voeg een `.env` toe:
```
COINMARKETCAP_API_KEY=your_api_key_here
REDDIT_CLIENT_ID=your_reddit_id
REDDIT_CLIENT_SECRET=your_reddit_secret
REDDIT_USER_AGENT=MemeCoinBot/0.1
```

4. Start de backend:
```bash
uvicorn main:app --reload
```

5. Ga naar `http://localhost:8000/` om het dashboard te bekijken.

## GitHub Push

```bash
git init
git add .
git commit -m "Initial commit"
git branch -M main
git remote add origin https://github.com/<username>/<repo>.git
git push -u origin main
```

## License

MIT
