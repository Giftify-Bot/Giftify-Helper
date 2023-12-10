import logging
from typing import Tuple

import discord_http as discord

try:
    from typing import Self
except ImportError:
    from typing_extensions import Self

log = logging.getLogger(__name__)

EXTENSIONS: Tuple[str, ...] = (
    "cogs.utility",
    "cogs.support",
    "cogs.webserver",
)


class GiftifyHelper(discord.Client):
    user: discord.User

    async def on_ready(self, user: discord.User):
        log.info(f"Logged in as {user}")

    async def setup_hook(self: Self):
        for extension in EXTENSIONS:
            log.info(f"Loaded {extension}")
            await self.load_extension(extension)
