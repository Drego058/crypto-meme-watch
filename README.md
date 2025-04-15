
# Meme Coin AI Dashboard (Light Theme)

AI-dashboard dat meme coins opspoort op Reddit, analyseert en een voorspelling doet of ze stijgen of dalen.

## Installatie (Backend)

```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --reload
```

## Reddit API Keys instellen

Maak een app op [Reddit Apps](https://www.reddit.com/prefs/apps)  
Zet je `REDDIT_CLIENT_ID` en `REDDIT_CLIENT_SECRET` als omgevingvariabelen.

## Openen

Ga naar `http://localhost:8000/` in je browser.

## Deployment
- Render of andere hosting voor FastAPI backend
- Frontend wordt geserveerd via `/static`
