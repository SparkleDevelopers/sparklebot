import discord
import json
import os
from discord.ext import commands

class User(commands.Cog):
    
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print("[INFO] [COGS] Module avatar loaded")

    @commands.command(name = "avatar")
    async def avatar(self, ctx, *, avamember : discord.Member=None):
        userAvatarUrl = avamember.avatar_url
        embed=discord.Embed(title=f"Аватар участника", description="", color=0x292B2F)  
        embed.set_image(url = userAvatarUrl)
        await ctx.send(embed=embed)

def setup(client):
    client.add_cog(User(client))