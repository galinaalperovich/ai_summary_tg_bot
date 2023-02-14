import logging
import os

# Log configuration
logger = logging.getLogger("ai_summary_bot")
logger.setLevel(os.getenv("LOG_LEVEL", "INFO"))

# Telegram bot configuration
BOT_TOKEN = os.getenv("BOT_TOKEN")
if not BOT_TOKEN:
    logging.error(
        "BOT_TOKEN env var is not found, cannot start the bot without it, create it with @BotFather Telegram bot! "
    )
else:
    logging.info("BOT_TOKEN found, starting the bot")

# Model configuration
DEFAULT_MODEL_NAME = "sshleifer/distilbart-cnn-12-6"
MODEL_NAME = os.getenv("MODEL_NAME")
if not MODEL_NAME:
    MODEL_NAME = DEFAULT_MODEL_NAME
    logging.info(f"MODEL_NAME env var is not found, using default model {MODEL_NAME}")
else:
    logging.info(f"MODEL_NAME is {MODEL_NAME}")

# Pyppeteer configuration
FROM_DOCKER = os.getenv("FROM_DOCKER")
if not FROM_DOCKER:
    logging.info("Running web scraping locally")
    FROM_DOCKER = False
else:
    logging.info("Running web scraping from inside Docker")
    FROM_DOCKER = True

NUM_SCRAPE_ATTEMPTS = 1

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) "
                  "AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/83.0.4103.97 Safari/537.36",
}
EXTRA_HTTP_HEADERS = {"Accept-Language": "en-US;q=0.8,en;q=0.7"}

WAIT_COND = ["domcontentloaded", "networkidle0"]
