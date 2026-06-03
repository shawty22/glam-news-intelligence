FEEDS = [
    # World News
    {"name": "Reuters",        "url": "https://feeds.reuters.com/reuters/topNews",           "topics": ["world"]},
    {"name": "BBC World",      "url": "http://feeds.bbci.co.uk/news/world/rss.xml",          "topics": ["world"]},
    {"name": "AP News",        "url": "https://feeds.apnews.com/rss/apf-topnews",            "topics": ["world"]},
    # Tech / AI
    {"name": "Ars Technica",   "url": "http://feeds.arstechnica.com/arstechnica/index",      "topics": ["tech", "ai"]},
    {"name": "The Verge",      "url": "https://www.theverge.com/rss/index.xml",              "topics": ["tech"]},
    {"name": "MIT Tech Review","url": "https://www.technologyreview.com/feed/",              "topics": ["ai", "tech"]},
    # Finance / Markets
    {"name": "FT",             "url": "https://www.ft.com/rss/home/uk",                      "topics": ["finance", "markets"]},
    # Geopolitics
    {"name": "Foreign Policy", "url": "https://foreignpolicy.com/feed/",                    "topics": ["geopolitics"]},
    {"name": "The Economist",  "url": "https://www.economist.com/international/rss.xml",    "topics": ["world", "geopolitics"]},
]

# Topics for overnight briefings — edit freely
BRIEFING_TOPICS = [
    "China",
    "artificial intelligence",
    "financial markets",
    "geopolitics",
]

OLLAMA_MODEL   = "llama3.2"
DB_PATH        = "./newsbox_db"
MAX_PER_FEED   = 20    # articles per feed per run
LOOKBACK_HOURS = 24
