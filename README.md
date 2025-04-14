# Meme Coin Trend AI
Een AI-project dat trending meme coins opspoort op Reddit en X, sentiment analyseert en een voorspelling maakt of de coin zal stijgen of dalen.

## Starten (Backend)
```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --reload
```

## Frontend bekijken
Open `http://localhost:8000/` in een browser nadat backend draait.

## Deployment
- Zet de backend op [Render](https://render.com)
- Gebruik GitHub voor versiebeheer
- Frontend-bestanden worden automatisch meegehost via FastAPI

## To do
- Integratie met X (Twitter)
- Verbeterde AI-model
- Historische data analyse
