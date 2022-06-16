import discord
import json
import os
from discord.ext import commands

class User(commands.Cog):
    
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print("[INFO] [COGS] Module bugs loaded")

    @commands.command(name="bug")
    async def bug(self, ctx , *, bug):
        embed=discord.Embed(title=f"{ctx.author.name} отправил баг!", description=bug, color=0x292B2F)
        embed.set_footer(text=f"Sparkle Bot 🧡 | Баг")
        channel = self.client.get_channel(986903843495354368)
        message = await channel.send(embed=embed)
        await message.add_reaction("<:galka:946355338339307561>")
        await message.add_reaction("<:X_:946355338364469258>")
        await ctx.send("Вы успешно отправили баг разработчику!")


def setup(client):
    client.add_cog(User(client))