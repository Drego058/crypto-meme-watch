
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

# Simpele CoinTicker -> CoinGecko ID mapping (uitbreidbaar)
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

        # Filter alleen geldige coins
        valid_symbols = [s for s in coin_stats if SYMBOL_TO_ID.get(s.upper()) and is_valid_coin_id(SYMBOL_TO_ID[s.upper()])]
        ids = [SYMBOL_TO_ID[s.upper()] for s in valid_symbols]

        prices = get_coin_prices_bulk(ids)

        result = []
        for symbol in valid_symbols:
            coin_id = SYMBOL_TO_ID[symbol.upper()]
            mentions = coin_stats[symbol]["mentions"]
            avg_sentiment = coin_stats[symbol]["sentiment_sum"] / mentions
            price = prices.get(coin_id)
            change = get_coin_price_change_24h(coin_id)
            result.append({
                "coin": symbol,
                "mentions": mentions,
                "avg_sentiment": round(avg_sentiment, 3),
                "price": price,
                "change_24h": change
            })

        return {"results": result}
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})
