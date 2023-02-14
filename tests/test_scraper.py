from datetime import datetime

import pytest

from summary_bot.scraper import extract_article


@pytest.mark.asyncio
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
