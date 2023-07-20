import random
from typing import Optional

import discord
from discord.ext import commands

from bot import GiftifyHelper

GIFTIFY_SUPPORT_SERVER_ID = 1089823072544108635
GIFTIFY_WELCOME_CHANNEL_ID = 1089823073294897196


class Welcome(commands.Cog):
    def __init__(self, bot: GiftifyHelper) -> None:
        self.bot = bot

    @staticmethod
    def get_welcome_message(username: str):
        messages = [
            f"Welcome, welcome, welcome, {username}! Have a great time!",
            f"Greetings, {username}! Did you bring the snacks?",
            f"Hey there, {username}! We hope you're ready to have a blast!",
            f"Look who just arrived! It's the one and only {username}!",
            f"Hola, amigo {username}! Ready to join the fun?",
            f"Ahoy there, {username}! Prepare to be amazed!",
            f"Welcome, {username}! We've been expecting you.",
            f"Hello, {username}! Prepare for an adventure of a lifetime!",
            f"Hey, hey, hey! It's {username} in the house!",
            f"Welcome, {username}! Make yourself at home and enjoy!",
            f"Bonjour, {username}! You've stepped into a world of wonders.",
            f"Hey, {username}! We hope you brought your dancing shoes!",
            f"Greetings, {username}! Let's paint the town red!",
            f"Welcome, welcome, welcome, {username}! The party's just getting started!",
            f"Hey there, {username}! Prepare to be entertained!",
            f"Ahoy, matey! It's the fabulous {username}!",
            f"Hello, {username}! We're glad you made it!",
            f"G'day, {username}! Get ready for a ripper of a time!",
            f"Hey, {username}! Let's rock and roll!",
            f"Welcome, welcome, welcome! Make way for the amazing {username}!",
        ]

        return random.choice(messages)

    @commands.Cog.listener()
    async def on_member_join(self, member: discord.Member):
        if member.guild.id != GIFTIFY_SUPPORT_SERVER_ID:
            return

        channel: Optional[discord.TextChannel] = member.guild.get_channel(GIFTIFY_WELCOME_CHANNEL_ID)  # type: ignore
        if channel:
            await channel.send(self.get_welcome_message(member.display_name))


async def setup(bot: GiftifyHelper) -> None:
    await bot.add_cog(Welcome(bot))
