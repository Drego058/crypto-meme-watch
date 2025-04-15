
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, JSONResponse
import os

from services.reddit_scraper import fetch_reddit_posts
from services.sentiment import analyze_sentiment
from services.coin_utils import extract_coin_mentions, fetch_coin_prices

app = FastAPI()

app.mount("/static", StaticFiles(directory="../frontend"), name="static")

@app.get("/")
def serve_index():
    index_path = os.path.join(os.path.dirname(__file__), "../frontend/index.html")
    return FileResponse(index_path)

@app.get("/analyze")
def analyze():
    posts = fetch_reddit_posts("meme coin")
    coin_data = {}

    for post in posts:
        coins = extract_coin_mentions(post)
        sentiment = analyze_sentiment(post)
        for coin in coins:
            if coin not in coin_data:
                coin_data[coin] = {"mentions": 0, "sentiment_total": 0}
            coin_data[coin]["mentions"] += 1
            coin_data[coin]["sentiment_total"] += sentiment

    # Voeg prijsdata toe
    prices = fetch_coin_prices(list(coin_data.keys()))

    result = []
    for coin, data in coin_data.items():
        avg_sentiment = data["sentiment_total"] / data["mentions"]
        price = prices.get(coin.lower(), None)
        result.append({
            "coin": coin,
            "mentions": data["mentions"],
            "avg_sentiment": avg_sentiment,
            "price": price
        })

    return JSONResponse({"results": result})
