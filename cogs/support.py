from typing import Optional

import discord_http as discord
from discord_http import commands

from bot import GiftifyHelper

DEVELOPER_ROLE_ID = 1089823072544108640
BOT_ADMIN_ROLE_ID = 1089823072544108638
MOD_ROLE_ID = 1120688394859720876

SUPPORT_CHANNEL_ID = 1131077649633120336
SUPPORT_ACCESS_ROLE_ID = 1122445173864026153

REPORT_CHANNEL_ID = 1131470656127647754


class HelpdeskDropdown(discord.view.Select):
    def __init__(self):
        super().__init__(
            custom_id="helpdesk",
            placeholder="Choose a help topic...",
            min_values=1,
            max_values=1,
        )

        self.add_item(
            label="How to use the bot",
            value="help",
            description="Learn how to setup and use the bot",
        )
        self.add_item(
            label="Technical Issues",
            value="status",
            description="If you are facing issues using the bot",
        )
        self.add_item(
            label="Report A Problem",
            value="report",
            description="If you want to report a problem or a bug",
        )
        self.add_item(
            label="Get human support",
            value="support",
            description="If none of the above answers your question",
        )


class HelpdeskDropdownView(discord.view.View):
    def __init__(self):
        super().__init__(HelpdeskDropdown())


class Support(commands.Cog):
    def __init__(self, bot: GiftifyHelper):
        self.bot = bot

    @commands.interaction("helpdesk")
    async def helpdesk_interaction(self, ctx: discord.Context):
        async def call_after(ctx: discord.Context):
            selected_option = ctx.select_values.strings[0]
            embed = self.get_embed(selected_option)

            if selected_option == "support":
                assert isinstance(ctx.user, discord.Member)
                await ctx.user.add_roles(SUPPORT_ACCESS_ROLE_ID)

            return ctx.response.send_message(embed=embed, ephemeral=True)

        return ctx.response.edit_message(call_after=call_after)

    @staticmethod
    def get_embed(selected_option: str) -> discord.Embed:
        embed = discord.Embed(color=0xCB3045)
        embed.set_thumbnail(
            url="https://media.discordapp.net/attachments/1120627940485509150/1183051663301427320/Logo_Circle.png"
        )
        embed.set_author(
            name="Giftify Discord Bot",
            url="https://giftifybot.vercel.app/",
            icon_url="https://media.discordapp.net/attachments/1120627940485509150/1183051663301427320/Logo_Circle.png",
        )

        if selected_option == "help":
            embed.title = "How to use the bot 🤖"
            embed.description = (
                "You can learn how to set up and use the Giftify Discord bot "
                "by following the [documentation](https://giftifybot.vercel.app/documentation)."
            )

        elif selected_option == "status":
            embed.title = "Technical Issues ❗"
            embed.description = (
                "If you are facing technical issues while using the bot, "
                "please check the [status page](https://giftifybot.vercel.app/status) for any ongoing problems."
            )

        elif selected_option == "report":
            embed.title = "Report A Problem 🐞"
            embed.description = (
                "If you encounter a problem or a bug with the bot, "
                "please report it by creating an issue on [the bot's github repository](https://giftifybot.vercel.app/github)."
            )

        elif selected_option == "support":
            embed.title = "Get human support 🆘"
            embed.description = (
                "You have been granted access to the support channel. "
                "Please avoid directly mentioning the moderators; instead, describe your issue and wait for up to 30 minutes before seeking assistance."
            )

        else:
            raise ValueError("Unknown option selected.")

        return embed

    @commands.command()
    @commands.guild_only()
    @commands.has_permissions("manage_guild")
    async def helpdesk(self, ctx: discord.Context):
        assert ctx.channel is not None

        embed = discord.Embed(
            title="Welcome to the Giftify Bot Helpdesk! 🎁",
            description=(
                "If you need assistance or have any questions, you can select a topic from the dropdown menu below. "
                "A support representative will be with you as soon as possible."
            ),
            color=0x32A852,
        )
        embed.set_author(
            name="Giftify Bot - Support",
            icon_url="https://media.discordapp.net/attachments/1120627940485509150/1183051663301427320/Logo_Circle.png",
        )

        view = HelpdeskDropdownView()
        await ctx.channel.send(embed=embed, view=view)

        return ctx.response.send_message("Successfully sent the embed!", ephemeral=True)


async def setup(bot: GiftifyHelper):
    await bot.add_cog(Support(bot))
