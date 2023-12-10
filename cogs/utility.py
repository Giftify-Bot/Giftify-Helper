from typing import Dict

import discord_http as discord
from discord_http import commands

from bot import GiftifyHelper

ROLES: Dict[str, int] = {
    "Giveaways": 1122414304096952401,
    "Guild News": 1122445113176637450,
    "Bot Updates": 1122414162002329620,
    "Bot Outages & Status": 1122413983861850132,
}


class RolesButton(discord.view.Button):
    def __init__(self, *, label: str, role_id: int):
        super().__init__(
            label=label,
            style=discord.ButtonStyles.primary,
            custom_id=f"roles:{role_id}",
        )


class RolesView(discord.view.View):
    def __init__(self, roles: Dict[str, int]):
        items = [
            RolesButton(label=label, role_id=role_id)
            for label, role_id in roles.items()
        ]

        super().__init__(*items)


class Utility(commands.Cog):
    def __init__(self, bot: GiftifyHelper):
        self.bot = bot

    @commands.interaction(r"roles:\d+", regex=True)
    async def roles_interaction(self, ctx: discord.Context):
        async def call_after(self, ctx: discord.Context):
            assert isinstance(ctx.user, discord.Member)
            assert ctx.custom_id is not None

            role_id = int(ctx.custom_id.split(":")[-1])

            embed: discord.Embed

            if ctx.user.get_role(role_id) is not None:
                await ctx.user.remove_roles(role_id)
                embed = discord.Embed(
                    colour=0xFF0000,
                    description=f"<:GiftifyMinus:1122076950421327872> Removed <@&{self.role_id}> from you!",
                )
            else:
                await ctx.user.add_roles(role_id)
                embed = discord.Embed(
                    colour=0x00FF00,
                    description=f"<:GiftifyPlus:1122076954556903494> Added <@&{self.role_id}> to you!",
                )

            return ctx.followup.send(embed=embed, ephemeral=True)

        return ctx.response.defer(thinking=True, ephemeral=True, call_after=call_after)

    @commands.command()
    @commands.guild_only()
    @commands.has_permissions("manage_guild")
    async def rules(self, ctx: discord.Context):
        image_url = "https://media.discordapp.net/attachments/1120627940485509150/1183051663301427320/Logo_Circle.png"
        tos_url = "https://giftifybot.vercel.app/terms"
        privacy_policy_url = "https://giftifybot.vercel.app/privacy"

        assert ctx.channel is not None

        embed = discord.Embed(
            description="Welcome to the Giftify Discord bot support server! We're here to assist you with any questions or issues you may have. To ensure a smooth and helpful experience for everyone, please follow these rules:",
            color=0xCB3045,
        )
        embed.set_author(name="Giftify Discord Bot - Rules", icon_url=image_url)
        embed.set_thumbnail(url=image_url)
        embed.add_field(
            name="1. Be respectful",
            value="Treat others with kindness and respect. Harassment, hate speech, or any form of discrimination will not be tolerated.",
            inline=False,
        )
        embed.add_field(
            name="2. Keep it appropriate",
            value="Please keep discussions and content appropriate for all audiences. No explicit, offensive, or NSFW content is allowed.",
            inline=False,
        )
        embed.add_field(
            name="3. No spamming or self-promotion",
            value="Avoid excessive posting, advertising, or promoting personal or external content without permission.",
            inline=False,
        )
        embed.add_field(
            name="4. Follow Discord's guidelines",
            value="Abide by Discord's Terms of Service (TOS) and Community Guidelines at all times.",
            inline=False,
        )
        embed.add_field(
            name="5. Use the appropriate channels",
            value="Keep conversations relevant to the designated channels. Off-topic discussions should be moved to the appropriate channels.",
            inline=False,
        )
        embed.add_field(
            name="6. No excessive tagging or mentions",
            value="Avoid spamming mentions or excessively tagging other users, especially without a valid reason.",
            inline=False,
        )
        embed.add_field(
            name="7. Respect bot usage",
            value="Use Giftify Discord Bot responsibly and within the limits set by the server administrators. Abuse or misuse may result in restrictions or removal.",
            inline=False,
        )
        embed.add_field(
            name="8. Listen to the moderators",
            value="Follow the instructions and decisions of the server moderators. If you have concerns, contact them privately.",
            inline=False,
        )
        embed.add_field(
            name="9. Keep personal information private",
            value="Do not share personal information about yourself or others without consent. Protect your privacy and the privacy of others.",
            inline=False,
        )
        embed.add_field(
            name="10. Have fun and enjoy your stay!",
            value="Remember to have a great time and make the most of your experience here!",
            inline=False,
        )
        embed.add_field(
            name="Privacy Policy",
            value=f"Please review our [Privacy Policy]({privacy_policy_url}) for information regarding data usage.",
            inline=False,
        )
        embed.add_field(
            name="Terms of Service",
            value=f"Please review our [Terms of Service]({tos_url}) for server guidelines and usage terms.",
            inline=False,
        )

        embed.set_footer(
            text="By joining this server, you agree to comply with these rules. Failure to adhere may result in appropriate action.",
            icon_url=image_url,
        )

        await ctx.channel.send(embed=embed)
        return ctx.response.send_message("Successfully sent the embed!", ephemeral=True)

    @commands.command()
    @commands.guild_only()
    @commands.has_permissions("manage_guild")
    async def roles(self, ctx: discord.Context):
        image_url = "https://media.discordapp.net/attachments/1120627940485509150/1183051663301427320/Logo_Circle.png"

        assert ctx.channel is not None

        embed = discord.Embed(
            title="Roles Selection",
            description=(
                "Please click the button below to get your corresponding roles.\n\n"
                "In case of interaction failure, try again after some time."
            ),
            color=0xCB3045,
        )
        embed.set_thumbnail(url=image_url)

        await ctx.channel.send(embed=embed, view=RolesView(ROLES))

        return ctx.response.send_message("Successfully sent the embed!", ephemeral=True)


async def setup(bot: GiftifyHelper):
    await bot.add_cog(Utility(bot))
