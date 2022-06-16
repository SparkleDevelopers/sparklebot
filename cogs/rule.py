import discord
from discord.ext import commands


class User(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print("[INFO] [COGS] Module serverinfo loaded")

    @commands.command(name="rule")
    async def rule(self, ctx):
        embed=discord.Embed(title="Правила Discord сервера", description="**1.** Запрещаются оскорбления в любом возможном виде. \n**2.** Запрещается использование твинков в корыстных целях. \n**3.** Запрещена отправка сообщений не по теме канала. \n**4.** Запрещается реклама любого вида на сервере или же в личных сообщениях. \n**5.** Запрещается политическая пропаганда.", color=0x292B2F)
        embed2=discord.Embed(title="Правила пользования ботом", description="Все пункты вынесены на [страницу сайта.](http://souresbot.tk/terms)", color=0x292B2F)
        embed2.set_image(url="https://i.ibb.co/3fjKBJF/rules.png")
        await ctx.send(embed=embed)
        await ctx.send(embed=embed2)

def setup(client):
    client.add_cog(User(client))
