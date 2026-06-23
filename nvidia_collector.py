import requests
from bs4 import BeautifulSoup
import trafilatura

from database.db import DB


class NvidiaCollector:

    def __init__(self):
        self.db = DB()
        self.base_url = "https://blogs.nvidia.com"

        self.headers = {
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/125.0 Safari/537.36"
            )
        }

    # =========================
    # EXTRACT FULL ARTICLE TEXT
    # =========================

    def get_full_content(self, url):
        try:
            downloaded = trafilatura.fetch_url(url)

            if not downloaded:
                return ""

            content = trafilatura.extract(downloaded)

            return content or ""

        except Exception as e:
            print(f"Content extraction error: {e}")
            return ""

    # =========================
    # EXTRACT PUBLISHED DATE
    # =========================

    def get_published_date(self, article_soup):

        try:

            # Method 1: OpenGraph / Article metadata
            meta_date = article_soup.find(
                "meta",
                {"property": "article:published_time"}
            )

            if meta_date:
                return meta_date.get("content", "").strip()

            # Method 2: Standard time tag
            time_tag = article_soup.find("time")

            if time_tag:

                if time_tag.get("datetime"):
                    return time_tag["datetime"].strip()

                return time_tag.get_text(strip=True)

            # Method 3: Generic meta tag
            meta_date = article_soup.find(
                "meta",
                {"name": "date"}
            )

            if meta_date:
                return meta_date.get("content", "").strip()

        except Exception as e:
            print("Date extraction error:", e)

        return ""

    # =========================
    # MAIN COLLECTION PIPELINE
    # =========================

    def collect(self):

        try:

            response = requests.get(
                self.base_url,
                headers=self.headers,
                timeout=15
            )

            response.raise_for_status()

        except Exception as e:

            print("Failed to access NVIDIA blog:", e)
            return

        soup = BeautifulSoup(
            response.text,
            "html.parser"
        )

        articles = soup.find_all("article")

        count = 0

        print(f"Found {len(articles)} articles")

        for article in articles[:20]:

            try:

                title_tag = article.find("h2")
                link_tag = article.find("a")

                if not title_tag or not link_tag:
                    continue

                title = title_tag.get_text(strip=True)

                link = link_tag.get("href", "")

                if not link:
                    continue

                # Convert relative URL → absolute URL
                if link.startswith("/"):
                    link = self.base_url + link

                # --------------------------------
                # LOAD ARTICLE PAGE
                # --------------------------------

                article_response = requests.get(
                    link,
                    headers=self.headers,
                    timeout=15
                )

                article_response.raise_for_status()

                article_soup = BeautifulSoup(
                    article_response.text,
                    "html.parser"
                )

                # --------------------------------
                # EXTRACT DATE
                # --------------------------------

                published_date = self.get_published_date(
                    article_soup
                )

                # --------------------------------
                # EXTRACT CONTENT
                # --------------------------------

                content = self.get_full_content(link)

                if not content:
                    continue

                if len(content.strip()) < 200:
                    continue

                # --------------------------------
                # SAVE TO DATABASE
                # --------------------------------

                self.db.insert(
                    title=title,
                    content=content,
                    source="NVIDIA",
                    category="Official-AI",
                    url=link,
                    date=published_date
                )

                print(
                    f"Saved NVIDIA: {title} | Date: {published_date}"
                )

                count += 1

            except Exception as e:

                print(
                    f"Error processing article: {e}"
                )

                continue

        print(f"\nTotal NVIDIA articles saved: {count}")


# =========================
# RUN
# =========================

if __name__ == "__main__":

    collector = NvidiaCollector()

    collector.collect()