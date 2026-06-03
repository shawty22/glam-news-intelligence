"""
Nightly scheduler — crawls at 2am, generates briefings at 3am.
Run directly:  python scheduler.py
Keep this running in a terminal or as a background service.
"""
import asyncio

from apscheduler.schedulers.blocking import BlockingScheduler

from pipeline import crawl_and_index
from briefing import run_all_briefings

scheduler = BlockingScheduler(timezone="UTC")


@scheduler.scheduled_job("cron", hour=2, minute=0)
def nightly_crawl():
    print("=== Nightly crawl starting ===")
    asyncio.run(crawl_and_index())
    print("=== Nightly crawl complete ===")


@scheduler.scheduled_job("cron", hour=3, minute=0)
def morning_briefing():
    print("=== Generating briefings ===")
    run_all_briefings()
    print("=== Briefings complete ===")


if __name__ == "__main__":
    print("NewsBox scheduler running.")
    print("  Crawl:    02:00 UTC")
    print("  Briefing: 03:00 UTC")
    print("Press Ctrl+C to stop.\n")
    scheduler.start()
