import asyncio
import logging
import logging.handlers
import os

import dotenv

from bot import GiftifyHelper

dotenv.load_dotenv()


async def main():
    logger = logging.getLogger("discord")
    logger.setLevel(logging.INFO)

    handler = logging.handlers.RotatingFileHandler(
        filename="discord.log",
        encoding="utf-8",
        maxBytes=32 * 1024 * 1024,
        backupCount=5,
    )
    dt_fmt = "%Y-%m-%d %H:%M:%S"
    formatter = logging.Formatter(
        "[{asctime}] [{levelname:<8}] {name}: {message}", dt_fmt, style="{"
    )
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    async with GiftifyHelper() as bot:
        await bot.start(os.environ["TOKEN"])


if __name__ == "__main__":
    asyncio.run(main())
