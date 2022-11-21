import disnake
from disnake.ext import commands
import random

class RussianRulet(commands.Cog):
    def __init__(self, client):
        self.client = client
      
    @commands.slash_command()
    async def rr(self,ctx):
        random_text=['Победил', 'Проиграл']
        if random.choice(random_text) == "Победил":
            embed=disnake.Embed(color = disnake.Color.dark_theme(),title="Победа!",description="Поздравляем, в этот раз Вам повезло",timestamp=ctx.message.created_at)
            embed.set_image(url="https://media.disnakeapp.net/attachments/980248813459623996/1002154191629848596/32fb79291a5d72a6dcf746c145a1ef45b5e86149r1-540-304_hq.gif")

        if random.choice(random_text) == "Проиграл":
            embed = disnake.Embed(color = disnake.Color.dark_theme(),title="Проиграл",description="К сожалению, Вы проиграли! Может в следующий раз повезёт!",timestamp=ctx.message.created_at)
            embed.set_image(url="https://media.disnakeapp.net/attachments/980248813459623996/1001368350179467384/suchadojikko-headshot_1.gif")

        await ctx.send(embed=embed)


def setup(client):
    client.add_cog(RussianRulet(client))