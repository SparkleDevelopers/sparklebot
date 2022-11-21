import disnake
from disnake.ext import commands
import random

class Ben(commands.Cog):
    def __init__(self, client):
        self.client = client
      
    @commands.slash_command()
    async def ben(self, ctx, *, text):
        random_text=['YES', 'NO', 'HOHOHO']       
        if random.choice(random_text) == "YES":
            embed=disnake.Embed(color = disnake.Color.dark_theme(),title="Говорящий Бен", description = "",timestamp=ctx.message.created_at)
            embed.set_image(url="https://i.imgur.com/WkzrLsa.gif")
            embed.add_field(name="Вопрос", value=text, inline=False)
            embed.add_field(name="Ответ", value="Да", inline=False)

        if random.choice(random_text) == "NO":
            embed = disnake.Embed(color = disnake.Color.dark_theme(),title="Говорящий Бен" ,description = "",timestamp=ctx.message.created_at)
            embed.set_image(url="https://i.imgur.com/Yiuu8Jn.gif")
            embed.add_field(name="Вопрос", value=text, inline=False)
            embed.add_field(name="Ответ", value="Нет", inline=False)
        
        if random.choice(random_text) == "HOHOHO":
            embed = disnake.Embed(color = disnake.Color.dark_theme(),title="Говорящий бен",description = "",timestamp=ctx.message.created_at)
            embed.set_image(url="https://c.tenor.com/e8urEO5XU-kAAAAd/hohho-ho.gif")
            embed.add_field(name="Вопрос", value=text, inline=False)
            embed.add_field(name="Ответ", value="Хо-хо-хо", inline=False)
            await ctx.send(embed=embed)


def setup(client):
    client.add_cog(Ben(client))