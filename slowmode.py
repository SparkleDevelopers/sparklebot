import discord
from discord.ext import commands


class User(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print("[INFO] [COGS] Module serverinfo loaded")

    @commands.command(name="slowmode")
    async def slowmode(ctx, seconds: int):
        await ctx.channel.edit(slowmode_delay=seconds)
        embed=discord.Embed(title="", description="<:galka:946355338339307561> Слоумод активирован в этом канале на {seconds} секунд", color=0x292B2F)
        await ctx.send(embed=embed)

def setup(client):
    client.add_cog(User(client))