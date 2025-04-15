
import snscrape.modules.reddit as reddit

def fetch_reddit_posts(keyword, limit=20):
    posts = []
    for i, post in enumerate(reddit.RedditSearchScraper(f"{keyword} site:reddit.com").get_items()):
        if i >= limit:
            break
        posts.append(post.content)
    return posts
