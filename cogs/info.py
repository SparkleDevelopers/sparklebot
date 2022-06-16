import discord
from discord.ext import commands


class User(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print("[INFO] [COGS] Module info loaded")

    @commands.command(name="info")
    async def info(self, ctx):
        embed=discord.Embed(title="SparkleBot", description="Привет! Меня зовут Спаркли! Я небольшой бот с кучкой всяких полезностей. \n \nМой префикс ` , `. Взгляни на команду ` ,help ` для более детальной информации о моих возможностях", URL = " https://sparkle.mrezer.ml/", color=0x292B2F)  
        embed.set_footer(text="ЗОВУТ МАКСИМ#3903 • https://sparkle.mrezer.ml/", icon_url = "https://i.ibb.co/hf7JvSB/image.jpg")
        embed.add_field(name="Сборка:", value=f"1.0 BETA ( <t:1655369400:D> )", inline=True)
        embed.add_field(name="Мой разработчик:", value=f"<:ezer:986914077311922176> ЗОВУТ МАКСИМ#3903", inline=False)
        embed.add_field(name="Полезные ссылки:", value=f"[Веб-сайт](https://sparkle.mrezer.ml/) \n[Сервер поддержки](https://discord.gg/xurCjm7cyK)", inline=True)
        await ctx.reply(embed=embed)

def setup(client):
    client.add_cog(User(client))