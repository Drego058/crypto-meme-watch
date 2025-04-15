
import praw
import os

reddit = praw.Reddit(
    client_id=os.getenv("REDDIT_CLIENT_ID"),
    client_secret=os.getenv("REDDIT_CLIENT_SECRET"),
    user_agent="meme-coin-ai"
)

def fetch_reddit_posts(keyword, limit=10):
    posts = []
    for submission in reddit.subreddit("all").search(keyword, limit=limit):
        posts.append(submission.title + "\n" + submission.selftext)
    return posts
