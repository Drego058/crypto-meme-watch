
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, JSONResponse
import os
from dotenv import load_dotenv
import time

from services.reddit_scraper import fetch_reddit_posts
from services.sentiment import analyze_sentiment
from models.predictor import predict_trend
from services.coin_price import (
    get_coin_prices_bulk,
    get_coin_price_change_24h,
    is_valid_coin_id,
    update_symbol_id_map
)
from services.coin_utils import extract_coin_mentions

load_dotenv()

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
        update_symbol_id_map(force=True)  # zorg dat map up-to-date is

        posts = fetch_reddit_posts("meme coin")
        coin_stats = {}

        for post in posts:
            sentiment = analyze_sentiment(post)
            mentions = extract_coin_mentions(post)
            for symbol in mentions:
                symbol = symbol.upper()
                if symbol not in coin_stats:
                    coin_stats[symbol] = {"mentions": 0, "sentiment_sum": 0}
                coin_stats[symbol]["mentions"] += 1
                coin_stats[symbol]["sentiment_sum"] += sentiment

        verified = []
        upcoming = []

        symbols = list(coin_stats.keys())
        valid_symbols = [s for s in symbols if is_valid_coin_id(s)]
        prices = get_coin_prices_bulk(valid_symbols)

        for symbol, data in coin_stats.items():
            if data["mentions"] <= 5:
                continue

            mentions = data["mentions"]
            avg_sentiment = data["sentiment_sum"] / mentions

            if symbol in valid_symbols:
                price = prices.get(symbol)
                change = get_coin_price_change_24h(symbol)
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
