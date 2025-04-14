from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from sentiment import analyze_text
import requests
import os
import praw

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

COINMARKETCAP_API_KEY = os.getenv("COINMARKETCAP_API_KEY")

class TextInput(BaseModel):
    text: str

class SearchInput(BaseModel):
    term: str

@app.get("/price")
def get_price(coin: str):
    url = f"https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest"
    headers = {"X-CMC_PRO_API_KEY": COINMARKETCAP_API_KEY}
    params = {"symbol": coin.upper()}
    response = requests.get(url, headers=headers, params=params)
    data = response.json()
    try:
        price = data["data"][coin.upper()]["quote"]["USD"]["price"]
        return {coin.lower(): {"usd": round(price, 2)}}
    except:
        return {"error": "Coin not found or API error."}

@app.get("/trending")
def trending():
    return ["bitcoin", "ethereum", "dogecoin"]

@app.post("/sentiment")
def sentiment(text: TextInput):
    result = analyze_text(text.text)
    return result

@app.get("/reddit-memes")
def reddit_memes(subreddit: str = "memes", limit: int = 5):
    reddit = praw.Reddit(
        client_id=os.getenv("REDDIT_CLIENT_ID"),
        client_secret=os.getenv("REDDIT_CLIENT_SECRET"),
        user_agent="meme-watcher"
    )
    memes = []
    for post in reddit.subreddit(subreddit).hot(limit=limit):
        if not post.stickied and (post.url.endswith(".jpg") or post.url.endswith(".png") or post.url.endswith(".jpeg")):
            memes.append({
                "title": post.title,
                "url": post.url,
                "permalink": f"https://reddit.com{post.permalink}",
                "score": post.score,
                "comments": post.num_comments
            })
    return memes