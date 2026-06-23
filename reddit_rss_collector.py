import feedparser
from database.db import DB
 
 
class RedditRSSCollector:
 
    def __init__(self):
        self.db = DB()
 
        self.feeds = [
            "https://www.reddit.com/r/MachineLearning/.rss",
            "https://www.reddit.com/r/artificial/.rss",
            "https://www.reddit.com/r/nvidia/.rss",
            "https://www.reddit.com/r/technology/.rss",
        ]
 
    def collect(self):
        count = 0
 
        for url in self.feeds:
            feed = feedparser.parse(url)
 
            for entry in feed.entries[:20]:
                try:
                    title = entry.get("title", "")
                    content = entry.get("summary", "")
                    link = entry.get("link", "")
                    date = entry.get("published", "")
 
                    self.db.insert(
                        title=title,
                        content=content,
                        source="Reddit",
                        category="Sentiment-Tech",
                        url=link,
                        date=date
                    )
 
                    print("Saved Reddit:", title)
                    count += 1
 
                except Exception as e:
                    print("Reddit Error:", e)
 
        print("Total Reddit:", count)