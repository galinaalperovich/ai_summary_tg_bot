import logging
import os

from aiogram import Bot, Dispatcher, executor, types
from summary_bot.scraper import extract_article

logging.basicConfig(level=logging.INFO)

BOT_TOKEN = os.getenv("BOT_TOKEN")
if not BOT_TOKEN:
    logging.error("BOT_TOKEN env var is not found, cannot start the bot without it, create with @BotFather Telegram bot")
    raise ValueError("BOT_TOKEN env variable is not found")
else:
    logging.info("BOT_TOKEN found, starting the bot")

from summary_bot.summarizer import summarize_article

bot = Bot(token=BOT_TOKEN, parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot)


@dp.message_handler(commands=["start"])
async def welcome(message: types.Message):
    await message.answer("Hi! Please send me a URL to summarize.")


@dp.message_handler()
async def get_summary(message: types.Message):
    try:
        user_input = message.text.strip()
        if not user_input.startswith("http"):
            await message.reply(
                "Please enter a valid URL to summarize, should start with `http`"
            )
            return

        await message.reply("Summarizing an article...")
        logging.info("Extracting article...")
        article = await extract_article(user_input)

        logging.info("Summarizing article...")
        summary = await summarize_article(article, message)
        await message.reply(summary)

    except Exception as err:
        await message.reply(f"Something went wrong :/ \n\nError: {err}")


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
