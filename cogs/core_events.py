import asyncio
from threading import Thread

import disnake
from disnake.ext import commands


class CoreEvents(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message_edit(self, before, after):
        alt_ctx = await self.bot.get_context(after)

        if after.content.lower() == before.content.lower() or not alt_ctx.command or after.author.bot:
            return

        emoji = '↩️'
        await after.add_reaction(emoji)

        try:
            await self.bot.wait_for('raw_reaction_add', check=lambda user: user.user_id == after.author.id and user.message_id == after.id, timeout=5)
            await self.bot.process_commands(after)
            await after.clear_reactions()
        except asyncio.TimeoutError:
            await after.clear_reactions()

def setup(bot):
    bot.add_cog(CoreEvents(bot))
