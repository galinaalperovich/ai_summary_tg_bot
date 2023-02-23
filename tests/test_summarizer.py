import os
from datetime import datetime

import pytest

from summary_bot.summarizer import summarize_article


def get_test_data(fname="article_bart.txt"):
    test_data = os.path.join(os.path.dirname(__file__), fname)
    with open(test_data) as f:
        article = f.read()
    return article


@pytest.mark.asyncio
async def test_summarizer():
    article = get_test_data(fname="article_starbucks.txt")

    print("Summarizing article...")
    start = datetime.now()
    summary = await summarize_article(article)
    end = datetime.now()
    print(len(summary))
    print(summary)
    t2 = end - start
    print("Summarization takes", t2)
