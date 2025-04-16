
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, JSONResponse
import os
from dotenv import load_dotenv
from services.reddit_scraper import fetch_reddit_posts
from services.x_scraper import fetch_x_posts
from services.sentiment import analyze_sentiment
from services.coin_utils import extract_coin_mentions
from services.coin_price import (
    get_coin_prices_bulk,
    get_coin_price_change_24h,
    is_valid_coin_id,
    update_symbol_id_map
)

load_dotenv()

app = FastAPI()
app.mount("/static", StaticFiles(directory="../frontend/static"), name="static")

@app.get("/")
def serve_index():
    index_path = os.path.join(os.path.dirname(__file__), "../frontend/index.html")
    return FileResponse(index_path)

@app.get("/analyze")
def analyze():
    try:
        update_symbol_id_map()  # geforceerd verversen symbol-to-ID map
        raw_posts = fetch_reddit_posts("meme coin") + fetch_x_posts("meme coin")

        stats = {}
        for post in raw_posts:
            sentiment = analyze_sentiment(post)
            mentions = extract_coin_mentions(post)
            for symbol in mentions:
                if symbol not in stats:
                    stats[symbol] = {"mentions": 0, "sentiment": 0}
                stats[symbol]["mentions"] += 1
                stats[symbol]["sentiment"] += sentiment

        verified, upcoming = [], []
        symbols = list(stats.keys())
        valid = [s for s in symbols if is_valid_coin_id(s)]

        prices = get_coin_prices_bulk(valid)

        for symbol in symbols:
            data = stats[symbol]
            if data["mentions"] < 2:
                continue
            avg_sentiment = round(data["sentiment"] / data["mentions"], 3)
            if symbol in valid:
                change = get_coin_price_change_24h(symbol)
                verified.append({
                    "coin": symbol,
                    "mentions": data["mentions"],
                    "avg_sentiment": avg_sentiment,
                    "price": prices.get(symbol),
                    "change_24h": change,
                    "status": "verified"
                })
            else:
                upcoming.append({
                    "coin": symbol,
                    "mentions": data["mentions"],
                    "avg_sentiment": avg_sentiment,
                    "price": None,
                    "change_24h": None,
                    "status": "upcoming"
                })

        return {"verified": verified, "upcoming": upcoming}
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})
