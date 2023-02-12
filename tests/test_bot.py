import asyncio
import os
from datetime import datetime

from summary_bot.summarizer import summarize_article
from summary_bot.scraper import extract_article


async def test_scraper():
    url = "https://www.projectpro.io/article/transformers-bart-model-explained/553"
    print("Extracting article...")
    start = datetime.now()
    article = await extract_article(url)
    end = datetime.now()
    print(len(article))
    print(article)
    t1 = end - start
    print("Extraction takes", t1)
    print("Test passed")


async def test_summarizer():
    test_data = os.path.join(os.path.dirname(__file__), "test.txt")
    with open(test_data) as f:
        article = f.read()

    print("Summarizing article...")
    start = datetime.now()
    summary = await summarize_article(article)
    end = datetime.now()
    print(len(summary))
    print(summary)
    t2 = end - start
    print("Summarization takes", t2)
    print("Test passed")


loop = asyncio.get_event_loop()
_ = loop.run_until_complete(test_scraper())
_ = loop.run_until_complete(test_summarizer())
