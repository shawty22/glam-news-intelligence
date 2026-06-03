"""
Lite pipeline using trafilatura (no browser needed).
Drop-in for pipeline.py when playwright isn't available.
Run: python pipeline_lite.py
"""
import hashlib
from datetime import datetime, timedelta

import feedparser
import trafilatura
import chromadb
from chromadb.utils.embedding_functions import SentenceTransformerEmbeddingFunction

from config import FEEDS, DB_PATH, MAX_PER_FEED, LOOKBACK_HOURS

_client    = chromadb.PersistentClient(path=DB_PATH)
_ef        = SentenceTransformerEmbeddingFunction(model_name="all-MiniLM-L6-v2")
collection = _client.get_or_create_collection("articles", embedding_function=_ef)


def _article_id(url: str) -> str:
    return hashlib.md5(url.encode()).hexdigest()


def _is_recent(entry) -> bool:
    if hasattr(entry, "published_parsed") and entry.published_parsed:
        published = datetime(*entry.published_parsed[:6])
        return published > datetime.utcnow() - timedelta(hours=LOOKBACK_HOURS)
    return True


def crawl_and_index():
    total = 0
    for feed_cfg in FEEDS:
        print(f"\n[{feed_cfg['name']}] fetching...")
        feed    = feedparser.parse(feed_cfg["url"])
        indexed = 0

        for entry in feed.entries:
            if indexed >= MAX_PER_FEED:
                break
            if not _is_recent(entry):
                continue

            url        = entry.get("link", "")
            article_id = _article_id(url)

            if collection.get(ids=[article_id])["ids"]:
                continue

            try:
                downloaded = trafilatura.fetch_url(url)
                if not downloaded:
                    continue
                text = trafilatura.extract(downloaded, include_comments=False, include_tables=False)
                if not text or len(text) < 100:
                    continue

                collection.add(
                    documents=[text[:3000]],
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
                print(f"  ! {url[:50]} — {exc}")

    print(f"\nDone. {total} new articles indexed.")


if __name__ == "__main__":
    crawl_and_index()
