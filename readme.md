# Telegram bot with AI article Summarizer
There is a blog post about this mini-project: https://medium.com/@galperovich/build-a-telegram-chatbot-with-any-ai-model-under-the-hood-62f9a8675d81

> **tl;dr:** we are building a text summarization bot for long articles, but I keep the code as general as possible, so consider it as a Python template for wrapping any model into a bot.

Sometimes you don't want to read the whole article, but you want to know what it's about.

This Telegram bot will extract the content of an article from a given URL and summarize it for you with the help of AI
summarization model.

## Usage

1. Create a Telegram bot with [BotFather](https://t.me/botfather)
2. Run the bot locally or deploy with Docker
3. Send a URL with an article you want to summarize to the bot
4. Receive summarized article!

## Tools under the hood

1. Telegram bot and `aiogram` library
2. Hugging Face BART model for summarization
3. `pyppeteer` headless browser to scrape an article from a given URL
4. `trafilatura` to extract the article from the HTML (removes all the ads and other stuff)

## How to run

### Environment variables

1. `BOT_TOKEN` - Telegram bot token. Get it by creating in [@BotFather](https://t.me/BotFather)
2. `MODEL_NAME` - Summarization model name (options: "sshleifer/distilbart-cnn-12-6", "facebook/bart-large-cnn", "
   facebook/bart-large-xsum"). By default "sshleifer/distilbart-cnn-12-6"
3. `LOG_LEVEL` - Logging level (options: "DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"). By default "INFO"
4. `FROM_DOCKER` - If the app is running in Docker (options: 1, 0). By default 0

### Run locally

```shell
export BOT_TOKEN=<YOUR_TOKEN>
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
pip install -e .
```

Run tests (at first, it will download the model, and it will take a few minutes)

```shell
pytest
```

Run the bot

```shell
python summary_bot/bot.py
```

Send to your Telegram bot a link to the article and get the summary!

### Run with Docker

Warning: It won't work on arm86 (Apple Silicon), I wasn't able to make Pypeteer work in Docker.

But it works on Linux/Debian 10, x86-64.

```shell
docker build -t ai_summary_bot:latest .
docker run --rm --init -it --name ai_summary_bot \
  --env BOT_TOKEN="<YOUR_TOKEN>" \
  --env FROM_DOCKER=1 \
  ai_summary_bot:latest

# in case it is not killed by Ctrl+C
docker kill ai_summary_bot
```

