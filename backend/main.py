
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, JSONResponse
import os
from dotenv import load_dotenv

from services.reddit_scraper import fetch_reddit_posts
from services.sentiment import analyze_sentiment
from models.predictor import predict_trend
from services.coin_price import get_coin_price, get_coin_price_change_24h
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
        posts = fetch_reddit_posts("meme coin")
        coin_stats = {}

        for post in posts:
            sentiment = analyze_sentiment(post)
            mentions = extract_coin_mentions(post)
            for coin in mentions:
                if coin not in coin_stats:
                    coin_stats[coin] = {"mentions": 0, "sentiment_sum": 0}
                coin_stats[coin]["mentions"] += 1
                coin_stats[coin]["sentiment_sum"] += sentiment

        result = []
        for coin, data in coin_stats.items():
            avg_sentiment = data["sentiment_sum"] / data["mentions"]
            coin_id = coin.lower()
            price = get_coin_price(coin_id)
            change = get_coin_price_change_24h(coin_id)
            result.append({
                "coin": coin,
                "mentions": data["mentions"],
                "avg_sentiment": round(avg_sentiment, 3),
                "price": price,
                "change_24h": change
            })

        return {"results": result}
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})
