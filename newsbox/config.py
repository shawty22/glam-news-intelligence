FEEDS = [
    # Amazon / Illegal Mining / Deforestation
    {"name": "Mongabay",          "url": "https://news.mongabay.com/feed/",                          "topics": ["amazon", "mining", "deforestation"]},
    {"name": "InfoAmazonia",      "url": "https://infoamazonia.org/en/feed/",                        "topics": ["amazon", "mining"]},
    {"name": "Amazon Watch",      "url": "https://amazonwatch.org/news/feed",                        "topics": ["amazon", "indigenous", "mining"]},
    {"name": "Global Witness",    "url": "https://www.globalwitness.org/en/blog/feed/",              "topics": ["mining", "corruption", "indigenous"]},
    {"name": "Reporter Brasil",   "url": "https://reporterbrasil.org.br/feed/",                     "topics": ["amazon", "mining", "labour"]},
    {"name": "FERN",              "url": "https://www.fern.org/news-resources/news/feed/",           "topics": ["deforestation", "forests", "policy"]},
    {"name": "Climate Home News", "url": "https://www.climatechangenews.com/feed/",                  "topics": ["climate", "policy", "amazon"]},
    {"name": "The Guardian Env",  "url": "https://www.theguardian.com/environment/rss",              "topics": ["environment", "amazon", "climate"]},
    {"name": "Reuters Environment","url": "https://feeds.reuters.com/reuters/environment",           "topics": ["environment", "mining"]},
    # Indigenous Rights
    {"name": "Survival Intl",     "url": "https://www.survivalinternational.org/news/feed",          "topics": ["indigenous", "amazon"]},
    # Supply Chain / Corporate
    {"name": "Global Trade Review","url": "https://www.gtreview.com/feed/",                         "topics": ["supply-chain", "mining", "trade"]},
    # Brazilian News (English)
    {"name": "Brazil Reports",    "url": "https://brazilreports.com/feed/",                         "topics": ["brazil", "amazon", "politics"]},
    {"name": "The Brazilian Report","url": "https://brazilian.report/feed/",                        "topics": ["brazil", "amazon", "politics"]},
]

# Topics for overnight briefings
BRIEFING_TOPICS = [
    "illegal gold mining Amazon",
    "garimpo deforestation",
    "indigenous land rights Brazil",
    "mercury contamination Amazon",
    "supply chain gold laundering",
]

OLLAMA_MODEL   = "llama3.2"
DB_PATH        = "./newsbox_db"
MAX_PER_FEED   = 20    # articles per feed per run
LOOKBACK_HOURS = 24
