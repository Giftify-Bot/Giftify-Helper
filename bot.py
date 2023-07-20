import logging
from typing import Tuple, TypeAlias

import aiohttp
import discord
from discord.ext import commands
from discord.ext.commands import errors

try:
    from typing import Self
except ImportError:
    from typing_extensions import Self

log = logging.getLogger("bot")

EXTENSIONS: Tuple[str, ...] = (
    "cogs.utility",
    "cogs.support",
    "cogs.welcome",
    "cogs.webserver",
)


class GiftifyHelper(commands.Bot):
    user: discord.ClientUser

    def __init__(
        self: Self,
        logger: logging.Logger,
        session: aiohttp.ClientSession,
        *args,
        **kwargs,
    ):
        self.logger = logger
        self.session = session
        super().__init__(
            *args,
            **kwargs,
            command_prefix=commands.when_mentioned_or("."),
            intents=discord.Intents.all(),
            allowed_mentions=discord.AllowedMentions(everyone=False, roles=False),
            case_insensitive=True,
            help_command=None,
            activity=discord.Game(name="with Giftify"),
        )

    async def on_ready(self: Self):
        log.info(f"Logged in as {self.user.display_name} ({self.user.id}).")

    async def setup_hook(self: Self):
        await self.load_extension("jishaku")
        for extension in EXTENSIONS:
            await self.load_extension(extension)

    async def on_command_error(
        self, ctx: commands.Context[Self], error: errors.CommandError
    ):
        if not isinstance(error, commands.CommandInvokeError):
            await ctx.send(str(error))


# Type Aliases
Context: TypeAlias = commands.Context[GiftifyHelper]
Interaction: TypeAlias = discord.Interaction[GiftifyHelper]
