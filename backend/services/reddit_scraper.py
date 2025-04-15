
import praw
import os
from dotenv import load_dotenv

load_dotenv()

reddit = praw.Reddit(
    client_id=os.getenv("REDDIT_CLIENT_ID"),
    client_secret=os.getenv("REDDIT_CLIENT_SECRET"),
    user_agent=os.getenv("REDDIT_USER_AGENT")
)

def fetch_reddit_posts(keyword, limit=10):
    posts = []
    for submission in reddit.subreddit("all").search(keyword, sort="new", limit=limit):
        posts.append(submission.title + " " + submission.selftext)
    return posts
