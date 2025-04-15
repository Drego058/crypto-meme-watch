
# 🧠 Meme Coin AI Dashboard

Een AI-powered dashboard dat meme coins in de gaten houdt op Reddit en X.  
Toont real-time sentiment, mentions, prijsdata en trending scores.

## 🔧 Functionaliteiten

- 🔍 Zoek naar trending meme coins
- 📈 Sentimentanalyse (VADER)
- 💬 Mentions op Reddit
- 💰 Prijs + 24u change via CoinMarketCap & CoinGecko fallback
- 🔥 Trending score + HOT-label
- 🖼️ Sparklines (tijdelijk uitgeschakeld)
- 🌐 Volledig werkende frontend (light UI)

## 🚀 Installatie

```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --reload
```

Bezoek dan: `http://localhost:8000`

## 📁 Projectstructuur

```
project_root/
├── backend/
│   ├── main.py
│   ├── services/
│   └── models/
├── frontend/
│   ├── index.html
│   └── static/
├── data/
├── .env.template
└── README.md
```

## 🧪 Demo-modus

Je kunt in de frontend handmatig demo-data tonen.

## 🌍 Deployment

Gebruik GitHub + Render (of Vercel) om te hosten.  
Voeg je API keys toe als environment variables.

