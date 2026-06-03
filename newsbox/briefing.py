"""
Generate opinionated overnight briefings from indexed articles using Ollama.
Run directly:  python briefing.py
"""
from datetime import date

import chromadb
import ollama
from chromadb.utils.embedding_functions import SentenceTransformerEmbeddingFunction

from config import DB_PATH, OLLAMA_MODEL, BRIEFING_TOPICS

_client = chromadb.PersistentClient(path=DB_PATH)
_ef     = SentenceTransformerEmbeddingFunction(model_name="all-MiniLM-L6-v2")
collection = _client.get_or_create_collection("articles", embedding_function=_ef)

_PROMPT = """\
You are a senior intelligence analyst writing a morning briefing for an expert audience.

Based ONLY on the articles below, write a sharp, opinionated analysis of: {topic}

Rules:
- Lead with the real story, not the surface headline
- Identify what is being missed or underreported
- Flag contradictions between sources if any exist
- End with "Watch for:" — one specific thing to monitor in the next 48 hours
- 250 words maximum. No filler.

Articles:
{articles}

Briefing:"""


def generate_briefing(topic: str, today: str | None = None) -> str:
    today = today or str(date.today())

    results = collection.query(
        query_texts=[topic],
        n_results=10,
        where={"date": today},
    )

    docs  = results["documents"][0]
    metas = results["metadatas"][0]

    if not docs:
        return f"No articles indexed for '{topic}' today ({today})."

    articles_block = "\n\n---\n\n".join(
        f"SOURCE: {m['source']}\nTITLE: {m['title']}\n{d[:600]}"
        for d, m in zip(docs, metas)
    )

    response = ollama.chat(
        model=OLLAMA_MODEL,
        messages=[{"role": "user", "content": _PROMPT.format(topic=topic, articles=articles_block)}],
    )
    return response["message"]["content"]


def run_all_briefings():
    today = str(date.today())
    print(f"\n{'='*60}")
    print(f"  INTELLIGENCE BRIEFING — {today}")
    print(f"{'='*60}")

    for topic in BRIEFING_TOPICS:
        print(f"\n## {topic.upper()}\n")
        print(generate_briefing(topic, today))

    print(f"\n{'='*60}\n")


if __name__ == "__main__":
    run_all_briefings()
