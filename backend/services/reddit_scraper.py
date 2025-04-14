import snscrape.modules.reddit as reddit

def fetch_reddit_posts(keyword, limit=10):
<<<<<<< HEAD
    posts = []
    for i, post in enumerate(reddit.RedditSearchScraper(f"{keyword} site:reddit.com").get_items()):
        if i >= limit:
            break
        posts.append(post.content)
    return posts
=======
    # Maak een scraper voor de zoekopdracht
    scraper = reddit.RedditSearchScraper(f'{keyword}')
    posts = []

    # Verkrijg berichten en voeg ze toe aan de lijst
    for i, post in enumerate(scraper.get_items()):
        if i >= limit:
            break
        posts.append(post.title + "\n" + post.selftext)
    
    return posts
>>>>>>> d1038717a95a3a92a7b5c73efc512f650577e409
