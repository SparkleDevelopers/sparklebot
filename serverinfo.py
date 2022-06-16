import discord
from discord.ext import commands


class User(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print("[INFO] [COGS] Module serverinfo loaded")

    @commands.command(name="serverinfo")
    async def serverinfo(ctx, guild):
        name = guild.name
        channels = guild.channels
        owner = guild.owner_name
        members = guild.member_count
        embed=discord.Embed(title=f"Информация о сервере {name}", description="", color=0x292B2F)
        embed.add_field(name="Участники:", value=f"<:icons_people:964425853930995783>Всего: **{members}** \n<:icons_Person:859388129932214292>Людей: 68 \n<:bot:934826661654974566> Ботов: 14", inline=True)
        embed.add_field(name="Каналы:", value=f"<:icons_bank:949635040252428318>Всего: **{channels}**", inline=False)
        embed.add_field(name="Владелец:", value=f"<:icons_owner:859429432380227594> **{owner}**", inline=True)
        embed.set_footer(text=f"Sparkle Bot 🧡 | Информация о сервере | Я не умею фильтровать людей и ботов, содержание Ботов и Участников неправильное")
        await ctx.send(embed=embed)

def setup(client):
    client.add_cog(User(client))