import discord
import json
import os
from discord.ext import commands

class User(commands.Cog):
    
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print("[INFO] [COGS] Module guild_join loaded")

    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        name = guild.name
        id = guild.id
        owner = guild.owner_name
        members = guild.member_count
        bots = discord.Member.bot
        servers = len(self.client.guilds)
        embed=discord.Embed(title="Бот был добавлен на сервер!", description="", color=0x2ecc71)
        embed.add_field(name="Название сервера:", value=f"` {name} `", inline=False)
        embed.add_field(name="Владелец сервера:", value=f"` {owner} `", inline=False)
        embed.add_field(name="ID сервера:", value=f"` {id} `", inline=False)
        embed.add_field(name="Участников на сервере:", value=f"` {members} `", inline=False)
        embed.add_field(name="Ботов на сервере:", value=f"` {bots} `", inline=False)
        embed.add_field(name="Серверов у бота:", value=f"` {servers} `", inline=False)
        channel = self.client.get_channel(986593661259227196)
        await channel.send(embed=embed)

def setup(client):
    client.add_cog(User(client))