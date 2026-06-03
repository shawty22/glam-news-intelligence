"""
Crawl RSS feeds → extract full article text → embed → store in ChromaDB.
Run directly:  python pipeline.py
"""
import asyncio
import hashlib
from datetime import datetime, timedelta

import feedparser
import chromadb
from chromadb.utils.embedding_functions import SentenceTransformerEmbeddingFunction
from crawl4ai import AsyncWebCrawler

from config import FEEDS, DB_PATH, MAX_PER_FEED, LOOKBACK_HOURS

_client = chromadb.PersistentClient(path=DB_PATH)
_ef     = SentenceTransformerEmbeddingFunction(model_name="all-MiniLM-L6-v2")
collection = _client.get_or_create_collection("articles", embedding_function=_ef)


def _article_id(url: str) -> str:
    return hashlib.md5(url.encode()).hexdigest()


def _is_recent(entry) -> bool:
    if hasattr(entry, "published_parsed") and entry.published_parsed:
        published = datetime(*entry.published_parsed[:6])
        return published > datetime.utcnow() - timedelta(hours=LOOKBACK_HOURS)
    return True  # include if no date available


async def crawl_and_index():
    total = 0
    async with AsyncWebCrawler(verbose=False) as crawler:
        for feed_cfg in FEEDS:
            print(f"\n[{feed_cfg['name']}] fetching feed...")
            feed    = feedparser.parse(feed_cfg["url"])
            indexed = 0

            for entry in feed.entries:
                if indexed >= MAX_PER_FEED:
                    break
                if not _is_recent(entry):
                    continue

                url        = entry.get("link", "")
                article_id = _article_id(url)

                # skip already-indexed articles
                if collection.get(ids=[article_id])["ids"]:
                    continue

                try:
                    result = await crawler.arun(url=url)
                    if not result.success or not result.markdown:
                        continue

                    text = result.markdown[:3000]

                    collection.add(
                        documents=[text],
                        metadatas=[{
                            "title":  entry.get("title", ""),
                            "source": feed_cfg["name"],
                            "url":    url,
                            "topics": ",".join(feed_cfg["topics"]),
                            "date":   str(datetime.utcnow().date()),
                        }],
                        ids=[article_id],
                    )
                    indexed += 1
                    total   += 1
                    print(f"  + {entry.get('title', url)[:70]}")

                except Exception as exc:
                    print(f"  ! failed {url[:60]} — {exc}")

    print(f"\nDone. {total} articles indexed.")


if __name__ == "__main__":
    asyncio.run(crawl_and_index())
