import datetime
import logging
from typing import Optional

import discord
from aiohttp import web
from discord.ext import commands

from bot import GiftifyHelper

log = logging.getLogger("cogs.webserver")

INCIDENT_EMOJIS = {
    "Resolved": "✅",
    "Investigating": "🔍",
    "Identified": "✅",
    "Monitoring": "🔍",
}
STATUS_CHANNEL_ID = 1117845433507655742
STATUS_ROLE_MENTION = "<@&1122413983861850132>"


class WebServer(commands.Cog):
    def __init__(self, bot: GiftifyHelper):
        self.bot = bot
        self.app = web.Application()
        self.app.router.add_get("/", self.handle)
        self.app.router.add_post("/instatus-webhook", self.handle_instatus_webhook)

    async def cog_load(self):
        runner = web.AppRunner(self.app)
        await runner.setup()
        self.site = web.TCPSite(runner, "0.0.0.0", 8080)
        await self.site.start()
        log.info("Webserver started on port 8080.")

    async def cog_unload(self):
        await self.site.stop()

    async def handle(self, request: web.Request):
        return web.json_response({"success": 200})

    async def handle_instatus_webhook(self, request: web.Request):
        data = await request.json()

        if "incident" not in data or "incident_updates" not in data["incident"]:
            return web.json_response({"error": "Invalid webhook data"}, status=400)

        await self.send_webhook_message(data["incident"])

        return web.json_response({"success": True})

    async def send_webhook_message(self, incident: dict):
        incident_description = ""
        for incident_update in incident["incident_updates"]:
            created_at = incident_update["created_at"]
            created_at_timestamp = int(
                datetime.datetime.fromisoformat(
                    created_at.replace("Z", "+00:00")
                ).timestamp()
            )
            incident_description += (
                f"**{INCIDENT_EMOJIS.get(incident_update['status'], '✅')} {incident_update['status']} - <t:{created_at_timestamp}:f>**\n"
                f"{incident_update['markdown']}\n"
            )
        incident_embed = discord.Embed(
            title=incident["name"],
            description=incident_description,
            url=incident["url"],
            colour=discord.Colour.blurple(),
        )
        incident_embed.set_author(
            name="Giftify",
            url="https://giftifybot.vercel.app/status",
            icon_url="https://giftifybot.vercel.app/giftify_circle.png",
        )

        affected_components = incident["affected_components"]
        if len(affected_components) == 1:
            components_embed = discord.Embed(
                title=f"Affected Component: ✅ {affected_components[0]['name']} ({affected_components[0]['status']})",
                colour=discord.Colour.blurple(),
            )
        else:
            components_description = ""
            for component in affected_components:
                components_description += (
                    f"✅ {component['name']} ({component['status']})"
                )
            components_embed = discord.Embed(
                title="Affected Components",
                description=components_description,
                colour=discord.Colour.blurple(),
            )

        embeds = [incident_embed, components_embed]

        channel: Optional[discord.TextChannel] = self.bot.get_channel(STATUS_CHANNEL_ID)  # type: ignore
        if not channel:
            return

        message_sent: Optional[discord.Message] = None

        if len(incident["incident_updates"]) == 1:
            message_sent = await channel.send(
                STATUS_ROLE_MENTION,
                embeds=embeds,
                allowed_mentions=discord.AllowedMentions(roles=True),
            )
        else:
            message = await self.get_incident_message(channel, incident["name"])
            if message is not None:
                await message.edit(embeds=embeds)
                await message.reply(
                    f"{STATUS_ROLE_MENTION}, This incident has been updated!",
                    delete_after=10,
                    allowed_mentions=discord.AllowedMentions(roles=True),
                )
            else:
                message_sent = await channel.send(embeds=embeds)

        if message_sent is not None:
            try:
                await message_sent.publish()
            except discord.HTTPException:
                pass

    async def get_incident_message(
        self, channel: discord.TextChannel, incident_name: str
    ) -> Optional[discord.Message]:
        async for message in channel.history():
            if (
                message.embeds
                and message.author.id == self.bot.user.id
                and message.embeds[0].title
                and message.embeds[0].title == incident_name
            ):
                return message


async def setup(bot: GiftifyHelper) -> None:
    await bot.add_cog(WebServer(bot))
