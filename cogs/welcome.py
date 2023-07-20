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
    def get_welcome_message(mention: str):
        messages = [
            f"Welcome, welcome, welcome, {mention}! Have a great time!",
            f"Greetings, {mention}! Did you bring the snacks?",
            f"Hey there, {mention}! We hope you're ready to have a blast!",
            f"Look who just arrived! It's the one and only {mention}!",
            f"Hola, amigo {mention}! Ready to join the fun?",
            f"Ahoy there, {mention}! Prepare to be amazed!",
            f"Welcome, {mention}! We've been expecting you.",
            f"Hello, {mention}! Prepare for an adventure of a lifetime!",
            f"Hey, hey, hey! It's {mention} in the house!",
            f"Welcome, {mention}! Make yourself at home and enjoy!",
            f"Bonjour, {mention}! You've stepped into a world of wonders.",
            f"Hey, {mention}! We hope you brought your dancing shoes!",
            f"Greetings, {mention}! Let's paint the town red!",
            f"Welcome, welcome, welcome, {mention}! The party's just getting started!",
            f"Hey there, {mention}! Prepare to be entertained!",
            f"Ahoy, matey! It's the fabulous {mention}!",
            f"Hello, {mention}! We're glad you made it!",
            f"G'day, {mention}! Get ready for a ripper of a time!",
            f"Hey, {mention}! Let's rock and roll!",
            f"Welcome, welcome, welcome! Make way for the amazing {mention}!",
        ]

        return random.choice(messages)

    @commands.Cog.listener()
    async def on_member_join(self, member: discord.Member):
        if member.guild.id != GIFTIFY_SUPPORT_SERVER_ID:
            return

        channel: Optional[discord.TextChannel] = member.guild.get_channel(GIFTIFY_WELCOME_CHANNEL_ID)  # type: ignore
        if channel:
            await channel.send(self.get_welcome_message(member.mention))


async def setup(bot: GiftifyHelper) -> None:
    await bot.add_cog(Welcome(bot))
