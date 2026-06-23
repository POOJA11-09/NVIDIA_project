import feedparser
import trafilatura
from database.db import DB
 
 
class NewsRSSCollector:
 
    def __init__(self):
        self.db = DB()
 
        self.feeds = [
            "https://techcrunch.com/feed/",
            "https://www.theverge.com/rss/index.xml",
            "https://feeds.arstechnica.com/arstechnica/index",
        ]
 
    def get_full_content(self, url):
        try:
            downloaded = trafilatura.fetch_url(url)
            return trafilatura.extract(downloaded) or ""
        except:
            return ""
 
    def collect(self):
        count = 0
 
        for url in self.feeds:
            feed = feedparser.parse(url)
 
            for entry in feed.entries[:25]:
 
                try:
                    title = entry.get("title", "")
                    link = entry.get("link", "")
                    date = entry.get("published", "")
 
                    content = self.get_full_content(link)
 
                    # FIX 1 — block empty content
                    if not content or len(content.strip()) < 200:
                        continue
 
                    self.db.insert(
                        title=title,
                        content=content,
                        source="RSS",
                        category="Tech-News",
                        url=link,
                        date=date
                    )
 
                    print("Saved RSS:", title)
                    count += 1
 
                except Exception as e:
                    print("RSS Error:", e)
 
        print("Total RSS:", count)