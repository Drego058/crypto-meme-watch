from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from sentiment import analyze_text
from reddit import get_reddit_memes
from twitter import search_tweets, get_popular_memes

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "Crypto Meme Watch API"}

@app.post("/sentiment")
async def sentiment_api(request: Request):
    body = await request.json()
    text = body.get("text", "")
    return analyze_text(text)

@app.get("/reddit-memes")
async def reddit_memes(subreddit: str = "memes", limit: int = 5):
    return get_reddit_memes(subreddit, limit)

@app.post("/tweets")
async def tweet_search(request: Request):
    body = await request.json()
    term = body.get("term", "")
    return search_tweets(term)

@app.get("/popular-memes")
async def popular_memes():
    return get_popular_memes()