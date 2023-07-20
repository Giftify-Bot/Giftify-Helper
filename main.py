import asyncio
import logging
import logging.handlers
import os
import pathlib
from contextlib import contextmanager

import aiohttp
import dotenv
from discord.utils import _ColourFormatter, stream_supports_colour

from bot import GiftifyHelper

dotenv.load_dotenv()


@contextmanager
def setup_logging():
    log = logging.getLogger()
    logging.getLogger("discord").setLevel(logging.INFO)
    logging.getLogger("discord.http").setLevel(logging.INFO)

    log.setLevel(logging.INFO)
    logging_path = pathlib.Path("./logs/")
    logging_path.mkdir(exist_ok=True)
    handler = logging.handlers.RotatingFileHandler(
        filename=logging_path / "Giftify-Helper.log",
        encoding="utf-8",
        mode="w",
        maxBytes=32 * 1024 * 1024,
        backupCount=5,
    )
    dt_fmt = "%Y-%m-%d %H:%M:%S"
    fmt = logging.Formatter(
        "[{asctime}] [{levelname:<7}] {name}: {message}", dt_fmt, style="{"
    )
    handler.setFormatter(fmt)
    log.addHandler(handler)

    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(_ColourFormatter())

    log.addHandler(stream_handler)

    try:
        yield log
    finally:
        handlers = log.handlers[:]
        for hdlr in handlers:
            hdlr.close()
            log.removeHandler(hdlr)


async def main(logger: logging.Logger):
    async with aiohttp.ClientSession() as session, GiftifyHelper(
        logger, session
    ) as bot:
        await bot.start(os.environ["TOKEN"])


if __name__ == "__main__":
    with setup_logging() as logger:
        asyncio.run(main(logger))
