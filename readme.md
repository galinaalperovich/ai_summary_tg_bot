# Summarize a URL with AI and Telegram bot
Sometimes you don't want to read the whole article, but you want to know what it's about. 

This Telegram bot will extract the content of an article from a given URL and summarize it for you with the help of AI summarization model.

## Tools:

1. Telegram bot
2. Hugging Face BART model [sshleifer/distilbart-cnn-12-6](https://huggingface.co/sshleifer/distilbart-cnn-12-6)
3. Pypeteer to scrape the article from the website
4. Trafilatura to extract the article from the HTML

## Usage:

1. Send a URL that contains an article to the bot
2. Wait for the summary

## Run locally

1. Create a new bot using @BotFather
2. Create python env and install dependencies

```shell
export BOT_TOKEN=<YOUR_TOKEN>
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
pip install -e .
```

3. Test main functions (at first, it will download the model, and it will take a few minutes)

```shell
python tests/test_bot.py
```

4. Run the bot

```shell
python summary_bot/bot.py
```

6. Send a link to the article to your bot in Telegram and get the summary!

## Run with Docker
Warning: It won't work on arm86 (Apple Silicon), I wasn't able to make Pypeteer work in Docker. 

But it works on Debian 10, x86-64.    

```shell
docker build -t ai_summary_bot:latest .
docker run --rm --init -it --name ai_summary_bot --env BOT_TOKEN="<YOUR_TOKEN>" --env FROM_DOCKER=1 ai_summary_bot:latest

# in case it is not killed by Ctrl+C
docker kill ai_summary_bot
```
