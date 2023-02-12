# Summarize a URL with AI and Telegram bot

## Tools:

1. Telegram bot
2. Hugging Face BART model [sshleifer/distilbart-cnn-12-6](https://huggingface.co/sshleifer/distilbart-cnn-12-6)
3. Pypeteer to scrape the article from the website
4. Trafilatura to extract the article from the HTML

## Usage:

1. Send a link to the article to the bot
2. Wait for the summary

## How to run locally

1. Create a new bot using @BotFather
2. Create an env variable with the token `export BOT_TOKEN=<YOUR_TOKEN>`
3. Create python env and install dependencies

```shell
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
pip install -e .
```

4. Test main functions (at first, it will download the model, and it will take a few minutes)

```shell
python tests/test_bot.py
```

5. Run the bot

```shell
python summary_bot/bot.py
```

5. Send a link to the article to your bot and get the summary! 