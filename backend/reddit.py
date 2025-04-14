import requests
import os

CLIENT_ID = os.getenv("REDDIT_CLIENT_ID")
SECRET = os.getenv("REDDIT_SECRET")
USERNAME = os.getenv("REDDIT_USERNAME")
PASSWORD = os.getenv("REDDIT_PASSWORD")
USER_AGENT = "CryptoMemeWatchBot/0.1"

def get_token():
    auth = requests.auth.HTTPBasicAuth(CLIENT_ID, SECRET)
    data = {'grant_type': 'password', 'username': USERNAME, 'password': PASSWORD}
    headers = {'User-Agent': USER_AGENT}
    res = requests.post("https://www.reddit.com/api/v1/access_token", auth=auth, data=data, headers=headers)
    return res.json()["access_token"]

def get_reddit_memes(subreddit="memes", limit=5):
    token = get_token()
    headers = {"Authorization": f"bearer {token}", "User-Agent": USER_AGENT}
    url = f"https://oauth.reddit.com/r/{subreddit}/hot?limit={limit}"
    res = requests.get(url, headers=headers)
    data = res.json()
    memes = []
    for post in data["data"]["children"]:
        p = post["data"]
        if p.get("post_hint") == "image":
            memes.append({
                "title": p["title"],
                "url": p["url"],
                "score": p["score"],
                "comments": p["num_comments"],
                "permalink": f"https://reddit.com{p['permalink']}"
            })
    return memes