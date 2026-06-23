from gnews import GNews

import trafilatura

from database.db import DB
 
 
class GoogleNewsCollector:
 
    def __init__(self):

        self.db = DB()

        self.news = GNews(language='en', max_results=100)
 
        # 🔥 EXPANDED QUERIES (IMPORTANT FOR 100+ DOCS)

        self.queries = [

            "NVIDIA AI",

            "AI chips",

            "AI infrastructure",

            "AI investment",

            "AI market trends",

            "AI competition",

            "AI hardware",

            "AI breakthrough",

            "OpenAI NVIDIA",

            "Amazon AI chips",

            "TSMC NVIDIA",

            "AI industry news",

            "AI partnerships"

        ]
 
    def get_full_content(self, url):

        try:

            downloaded = trafilatura.fetch_url(url)

            content = trafilatura.extract(downloaded)
 
            # 🔥 fallback (VERY IMPORTANT)

            if not content:

                return ""
 
            return content

        except:

            return ""
 
    def collect(self):

        count = 0
 
        for q in self.queries:

            results = self.news.get_news(q)
 
            for r in results:
 
                try:

                    title = r.get("title")

                    url = r.get("url")

                    date = r.get("published date")
 
                    content = self.get_full_content(url)
 
                    # 🔥 RELAXED FILTER (IMPORTANT FOR 100 DOCS)

                    if not content:

                        content = title  # fallback so we don't lose data
 
                    self.db.insert(

                        title=title,

                        content=content,

                        source="GoogleNews",

                        category="AI-Market",

                        url=url,

                        date=date

                    )
 
                    print("Saved Google:", title)

                    count += 1
 
                except:

                    continue
 
        print("Total Google:", count)
 
import re
 
class Cleaner:
 
    def clean(self, text):
        if not text:
            return ""
 
        text = re.sub(r"\s+", " ", text)
        text = text.strip()
 
        return text
 