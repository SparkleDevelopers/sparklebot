import disnake
from disnake.ext import commands
import json
from utils import prefix as prefixes


class Help(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        CONFIG = json.load(open("config.json"))

    @commands.slash_command(name="help")
    async def help(self, ctx):
        prefix = "/"   #prefixes.get(ctx.guild.id)
        embed=disnake.Embed(title="Навигация по командам :pushpin:", description="Скоро будет меню \nЕсть много чего в слешах", color=0x292B2F)  
        embed.add_field(name="📰 Информация", value=f"` {prefix}help ` ` {prefix}user ` ` {prefix}avatar ` ` {prefix}stats ` ` /guild ` ` {prefix}ping `.", inline=False)
        embed.add_field(name="🛡️  Модерирование", value=f"` {prefix}mute ` ` {prefix}unmute ` ` {prefix}ban ` ` {prefix}unban ` ` {prefix}kick ` `{prefix}clear` ` /setprefix `", inline=False)
        embed.add_field(name="🔧  Утилиты", value=f"` {prefix}bug ` `{prefix}suggest `, ` {prefix}report ` `{prefix}suggest_set ` ` {prefix}report_set `.", inline=False)
        embed.add_field(name="😹 Развлечения", value=f"` {prefix}8ball ` ` {prefix}sap", inline=False)
        embed.add_field(name="👦 РП", value=f"` {prefix}kiss ` ` {prefix}bite ` ` {prefix}eat ` ` {prefix}marry ` ` {prefix}divorce ` ` /rp `", inline=False)
        embed.add_field(name="🎶 Музыка", value=f"**Не работает**", inline=False)
        embed.add_field(name=":microphone2: Голосовые каналы", value=f"` {prefix}voice setup ` ` {prefix}voice setlimit ` ` {prefix}voice lock ` ` {prefix}voice unlock ` ` {prefix}voice permit ` ` {prefix}voice reject ` ` {prefix}voice limit ` ` {prefix}voice name ` ` {prefix}voice claim ` ", inline=False)
        embed.set_footer(text="ЗОВУТ МАКСИМ#3903 • https://sparklebot.fun/", icon_url = "https://i.ibb.co/hf7JvSB/image.jpg")
        embed.set_image(url="https://www.coinopsy.com/static/img/discordc.svg")
        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(Help(bot))