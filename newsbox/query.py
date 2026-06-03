"""
Query the news knowledge base instantly — no inference, pure semantic search.
Run directly:  python query.py
"""
import sys

import chromadb
from chromadb.utils.embedding_functions import SentenceTransformerEmbeddingFunction

from config import DB_PATH

_client = chromadb.PersistentClient(path=DB_PATH)
_ef     = SentenceTransformerEmbeddingFunction(model_name="all-MiniLM-L6-v2")
collection = _client.get_or_create_collection("articles", embedding_function=_ef)


def search(question: str, n: int = 5, date_filter: str | None = None):
    kwargs = {"query_texts": [question], "n_results": n}
    if date_filter:
        kwargs["where"] = {"date": date_filter}

    results = collection.query(**kwargs)
    docs    = results["documents"][0]
    metas   = results["metadatas"][0]

    if not docs:
        print("Nothing found.")
        return

    for i, (doc, meta) in enumerate(zip(docs, metas), 1):
        print(f"\n{'─'*60}")
        print(f"[{i}] {meta['title']}")
        print(f"    {meta['source']}  •  {meta['date']}")
        print(f"    {meta['url']}")
        print(f"\n{doc[:500]}...")


def interactive():
    print("NewsBox  —  semantic search across your indexed news")
    print("Commands: 'quit' to exit | 'date YYYY-MM-DD' to filter by date\n")

    date_filter = None
    while True:
        try:
            raw = input("Ask: ").strip()
        except (EOFError, KeyboardInterrupt):
            break

        if not raw:
            continue
        if raw.lower() in ("quit", "exit", "q"):
            break
        if raw.lower().startswith("date "):
            date_filter = raw.split()[1]
            print(f"Filtering to: {date_filter}")
            continue

        search(raw, date_filter=date_filter)


if __name__ == "__main__":
    if len(sys.argv) > 1:
        search(" ".join(sys.argv[1:]))
    else:
        interactive()
