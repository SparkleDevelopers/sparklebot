import discord
import json
import os
from discord.ext import commands
import asyncio

class User(commands.Cog):
    
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print("[INFO] [COGS] module clear loaded")

    @commands.command(name="clear")
    async def clear(self, ctx, number=5):
        channel = ctx.message.channel
        try:
            number = int(number) 
        except ValueError:
            return await self.client.send_message(channel, "Please enter a valid number.")

        async for x in self.client.logs_from(channel, limit=number):
            await self.cliant.delete_message(x)
            await asyncio.sleep(0.5) 


def setup(client):
    client.add_cog(User(client))