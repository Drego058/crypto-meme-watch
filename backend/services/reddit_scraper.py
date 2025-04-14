import snscrape.modules.reddit as reddit

def fetch_reddit_posts(keyword, limit=10):
    scraper = reddit.RedditSearchScraper(f'{keyword}')
    posts = []
    for i, post in enumerate(scraper.get_items()):
        if i >= limit:
            break
        posts.append(post.title + "\n" + post.selftext)
    return posts
