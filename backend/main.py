
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, JSONResponse
import os

from services.reddit_scraper import fetch_reddit_posts
from services.sentiment import analyze_sentiment
from models.predictor import predict_trend
from services.coin_price import get_coin_price

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
        analyzed = [
            {
                "text": post,
                "sentiment": analyze_sentiment(post),
                "prediction": predict_trend(post),
                "price_btc": get_coin_price("bitcoin")
            }
            for post in posts
        ]
        return {"results": analyzed}
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})
