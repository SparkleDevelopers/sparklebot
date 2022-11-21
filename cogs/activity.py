from typing import Literal

import disnake
from disnake.ext import commands
from DiscordActivity import Activity


class Activities(commands.Cog):

    @commands.slash_command(name="activity", description="Всякие разные голосовые активности для канальчика")
    async def discord_activity(self, inter, voice_channel: disnake.VoiceChannel, activity_name: Literal['youtube', 'poker', 'betrayal', 'word-snack', 'doodle-crew']):
        data = await Activity(inter.bot).send_activity(voice=voice_channel, name=activity_name)
        await inter.send(f'[Кликни сюда, чтобы начать!](https://discord.gg/{data["code"]})')


def setup(bot):
    bot.add_cog(Activities(bot))
