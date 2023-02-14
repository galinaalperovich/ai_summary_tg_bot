from aiogram import Bot, Dispatcher, executor, types

from summary_bot.scraper import extract_article
from summary_bot.settings import BOT_TOKEN, MODEL_NAME, logger
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

        await message.reply("Summarizing the article...")
        logger.info("Extracting article...")
        article = await extract_article(user_input)

        logger.info("Summarizing article...")
        summary = await summarize_article(article, message, model_name=MODEL_NAME)
        logger.info("Done summarizing article")

        await message.reply(summary)

    except Exception as err:
        logger.error("Error while summarizing article", exc_info=err)
        await message.reply(f"Error while summarizing article:\n\n{err}")


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
