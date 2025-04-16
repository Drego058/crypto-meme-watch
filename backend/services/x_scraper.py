
import snscrape.modules.twitter as twitter

def fetch_x_posts(keyword, limit=10):
    posts = []
    for i, tweet in enumerate(twitter.TwitterSearchScraper(f"{keyword}").get_items()):
        if i >= limit:
            break
        posts.append(tweet.content)
    return posts
