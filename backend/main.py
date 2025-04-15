
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, JSONResponse
import os
from dotenv import load_dotenv

from services.reddit_scraper import fetch_reddit_posts
from services.sentiment import analyze_sentiment
from models.predictor import predict_trend
from services.coin_price import get_coin_prices_bulk, get_coin_price_change_24h, is_valid_coin_id
from services.coin_utils import extract_coin_mentions

load_dotenv()

# Simpele CoinTicker -> CoinGecko ID mapping
SYMBOL_TO_ID = {
    "DOGE": "dogecoin",
    "PEPE": "pepe",
    "SHIB": "shiba-inu",
    "WIF": "dogwifhat",
    "BTC": "bitcoin"
}

app = FastAPI()
app.mount("/static", StaticFiles(directory="../frontend"), name="static")

@app.get("/")
def serve_index():
    try:
        index_path = os.path.join(os.path.dirname(__file__), "../frontend/index.html")
        return FileResponse(index_path)
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})

@app.get("/analyze")
def analyze():
    try:
        posts = fetch_reddit_posts("meme coin")
        coin_stats = {}

        for post in posts:
            sentiment = analyze_sentiment(post)
            mentions = extract_coin_mentions(post)
            for symbol in mentions:
                if symbol not in coin_stats:
                    coin_stats[symbol] = {"mentions": 0, "sentiment_sum": 0}
                coin_stats[symbol]["mentions"] += 1
                coin_stats[symbol]["sentiment_sum"] += sentiment

        result = []

        verified = []
        upcoming = []

        for symbol, data in coin_stats.items():
            mentions = data["mentions"]
            avg_sentiment = data["sentiment_sum"] / mentions
            coin_id = SYMBOL_TO_ID.get(symbol.upper())

            if coin_id and is_valid_coin_id(coin_id):
                price = get_coin_prices_bulk([coin_id]).get(coin_id)
                change = get_coin_price_change_24h(coin_id)
                verified.append({
                    "coin": symbol,
                    "status": "verified",
                    "mentions": mentions,
                    "avg_sentiment": round(avg_sentiment, 3),
                    "price": price,
                    "change_24h": change
                })
            else:
                upcoming.append({
                    "coin": symbol,
                    "status": "upcoming",
                    "mentions": mentions,
                    "avg_sentiment": round(avg_sentiment, 3),
                    "price": None,
                    "change_24h": None
                })

        return {"verified": verified, "upcoming": upcoming}
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})
