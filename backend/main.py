from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import os

from services.reddit_scraper import fetch_reddit_posts
from services.sentiment import analyze_sentiment
from models.predictor import predict_trend

app = FastAPI()

# Serve static frontend files
app.mount("/static", StaticFiles(directory="../frontend"), name="static")

@app.get("/")
def serve_index():
    index_path = os.path.join(os.path.dirname(__file__), "../frontend/index.html")
    return FileResponse(index_path)

@app.get("/analyze")
def analyze():
    posts = fetch_reddit_posts("meme coin")
    analyzed = [
        {
            "text": post,
            "sentiment": analyze_sentiment(post),
            "prediction": predict_trend(post)
        }
        for post in posts
    ]
    return {"results": analyzed}
