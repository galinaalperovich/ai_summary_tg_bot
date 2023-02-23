from datetime import datetime

import pytest

from summary_bot.scraper import extract_article
from summary_bot.summarizer import summarize_article


@pytest.mark.asyncio
async def test_bot():
    url = "https://edition.cnn.com/2023/02/21/business/starbucks-oleato"
    print("Extracting article...")
    start = datetime.now()
    article = await extract_article(url)
    end = datetime.now()
    print(len(article))
    print(article)
    t1 = end - start
    print("Extraction takes", t1)
    summary = await summarize_article(article)
    end = datetime.now()
    print(len(summary))
    print(summary)
    t2 = end - start
    print("Summarization takes", t2)
