import disnake
from disnake.ext import commands
import json
from utils import prefix as prefixes


class events(commands.Cog):

    def __init__(self, client):
        CONFIG = json.load(open("config.json"))
        self.client = client

    @commands.Cog.listener()
    async def on_message(self, message: disnake.Message):
        await self.client.process_commands(message)
        msg = message.content.lower()
        if message.content.startswith(['hello', 'ку', 'привет', 'здравствуйте', 'хай', 'hi','здарова']):
            hello = self.client.get_emoji("🖐")
            await message.add_reaction(hello)
    
    @commands.Cog.listener()
    async def on_message(self, message):
        if not message.author.bot:
            if message.content.startswith(f'<@{self.client.user.id}>') or message.content.startswith(f'<@!{self.client.user.id}>'):
                try:
                    prefix = prefixes.get(message.guild.id)
                except:
                    prefix = prefixes.get(message.guild.id)
                await message.channel.send(f'{message.author.mention}, мой префикс – `{prefix}`. Для просмотра списка команд введи `{prefix}help`.')

def setup(client):
    client.add_cog(events(client))