import discord
from discord.ext import commands


class User(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print("[INFO] [COGS] Module Help loaded")

    @commands.command(name="help")
    async def help(self, ctx):
        embed=discord.Embed(title="Навигация по командам :pushpin:", description="`< >`  ─ Необязательные аргументы. \n`[ ]`  ─ Обязательные аргументы.", color=0x292B2F)  
        embed.add_field(name="📋  Информация", value=f"`,online` `,plist` `,suggest [текст]` `,ping `.", inline=False)
        embed.add_field(name="🛡️  Модерирование", value=f"`,mute` `,unmute` `,ban` `,unban` `,kick` `,warn` `,warns` `,remwarn` `,resetwarns` `,clear` ", inline=False)
        embed.add_field(name="🔧  Утилиты", value=f"` .avatar `, ` .bug ` , `,suggest `.", inline=False)
        embed.set_footer(text="ЗОВУТ МАКСИМ#3903 • https://sparkle.mrezer.ml/", icon_url = "https://i.ibb.co/hf7JvSB/image.jpg")
        embed.set_image(url="https://www.coinopsy.com/static/img/discordc.svg")
        await ctx.send(embed=embed)

def setup(client):
    client.add_cog(User(client))