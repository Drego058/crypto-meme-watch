from fastapi import FastAPI
from services.reddit_scraper import fetch_reddit_posts
from services.sentiment import analyze_sentiment
from models.predictor import predict_trend

app = FastAPI()

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
