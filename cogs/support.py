from typing import Optional

import discord
from discord.ext import commands

from bot import Context, GiftifyHelper, Interaction

DEVELOPER_ROLE_ID = 1089823072544108640
BOT_ADMIN_ROLE_ID = 1089823072544108638
MOD_ROLE_ID = 1120688394859720876

SUPPORT_ACCESS_ROLE_ID = 1122445173864026153

REPORT_CHANNEL_ID = 1131470656127647754


class HelpdeskDropdown(discord.ui.Select):
    def __init__(self):
        options = [
            discord.SelectOption(
                label="How to use the bot",
                value="help",
                description="Learn how to setup and use the bot",
            ),
            discord.SelectOption(
                label="Technical Issues",
                value="status",
                description="If you are facing issues using the bot",
            ),
            discord.SelectOption(
                label="Report A Problem",
                value="report",
                description="If you want to report a problem or a bug",
            ),
            discord.SelectOption(
                label="Get human support",
                value="support",
                description="If none of the above answers your question",
            ),
        ]

        super().__init__(
            custom_id="helpdesk",
            placeholder="Choose a help topic...",
            min_values=1,
            max_values=1,
            options=options,
        )

    async def callback(self, interaction: Interaction):
        selected_option = self.values[0]
        embed = self.get_embed(selected_option)
        await interaction.response.send_message(embed=embed, ephemeral=True)
        if selected_option == "support":
            assert isinstance(interaction.user, discord.Member)
            await interaction.user.add_roles(discord.Object(SUPPORT_ACCESS_ROLE_ID))

    @staticmethod
    def get_embed(selected_option: str) -> discord.Embed:
        embed = discord.Embed(color=0xCB3045)
        embed.set_thumbnail(url="https://giftifybot.vercel.app/giftify_circle.png")
        embed.set_author(
            name="Giftify Discord Bot",
            url="https://giftifybot.vercel.app/",
            icon_url="https://giftifybot.vercel.app/giftify_circle.png",
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
                "please report it using the `.report <bug_info>` command in <#1089823073294897198> channel."
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


class HelpdeskDropdownView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        self.add_item(HelpdeskDropdown())


class Support(commands.Cog):
    def __init__(self, bot: GiftifyHelper):
        self.bot = bot

    def cog_load(self):
        self.bot.add_view(HelpdeskDropdownView())

    @commands.command()
    @commands.guild_only()
    @commands.has_permissions(manage_guild=True)
    async def helpdesk(self, ctx: Context):
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
            icon_url="https://giftifybot.vercel.app/giftify_circle.png",
        )

        view = HelpdeskDropdownView()
        await ctx.send(embed=embed, view=view)

    @commands.command(name="clearsupport", aliases=["cs", "clear_support"])
    @commands.guild_only()
    @commands.has_any_role(DEVELOPER_ROLE_ID, BOT_ADMIN_ROLE_ID, MOD_ROLE_ID)
    async def clear_support(self, ctx: Context):
        assert ctx.guild is not None

        role = ctx.guild.get_role(SUPPORT_ACCESS_ROLE_ID)
        if role:
            async with ctx.typing():
                i = 0
                for member in role.members:
                    await member.remove_roles(role)
                    i += 1
                await ctx.send(f"Removed the role from {i} members!")
        else:
            await ctx.send("The support access role was not found.")

    @commands.command()
    @commands.cooldown(1, 600, commands.BucketType.user)
    @commands.guild_only()
    async def report(self, ctx: Context, *, bug: str):
        channel: Optional[discord.TextChannel] = self.bot.get_channel(REPORT_CHANNEL_ID)  # type: ignore
        if channel:
            embed = discord.Embed(
                title="New bug reported!",
                description=bug[:2048],
                color=discord.Colour.red(),
            )
            embed.set_author(name=ctx.author.name, icon_url=ctx.author.display_avatar)

            await channel.send(embed=embed)
        else:
            await ctx.send("The support channel was not found.")


async def setup(bot: GiftifyHelper):
    await bot.add_cog(Support(bot))
