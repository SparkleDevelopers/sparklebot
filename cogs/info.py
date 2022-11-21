import disnake
import platform
import sys
import psutil
from disnake.ext import commands
from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw
from core.classes.another_embeds import Field, Footer
import time
import core
import datetime
from datetime import datetime
def time4logs():
    return f'[{datetime.datetime.now().strftime("%d.%m.%Y %H:%M:%S")}]'
start = time.time()


class Info(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.start_time = datetime.now()

    @commands.slash_command(aliases=["botstats"])
    async def stats(self, ctx):
        shard_names = {
            '0': 'Саня',
            '1': 'Кристина',
            '2': 'Виктория',
            '3': 'Клэр'
        }
        guilds_info = (
            f"Количество серверов: **{len(self.bot.guilds)}**",
            f"Количество пользователей: **{len(self.bot.users)}**",
            f"Количество стикеров: **{len(self.bot.stickers)}**",
            f"Количество эмодзи: **{len(self.bot.emojis)}**",
        )
        about_me_info = (
            f"Я создан: **13 июля, 2022 года.** \n[Мой сервер поддержки](https://discord.gg/xurCjm7cyK) \nОперационная система: **{platform.platform()}** \nЯзык программирования: **Python {sys.version}**")
        other_info = (
            f"Мой ID: **{ctx.me.id}** \nКоличество слэш команд: **{len(self.bot.global_slash_commands)}** \nКоличество обычных команд: **{len([i for i in self.bot.commands if not i.name == 'jishaku' and not i.name == 'justify'])}** \nЗадержка: **{round(self.bot.latency*1000, 2)}ms** \nRAM: **{psutil.virtual_memory().percent}%** \nCPU: **{psutil.Process().cpu_percent()}%** \nКластеров: **{len(self.bot.shards)}**")

        dpyVersion = disnake.__version__
        servers = len(self.bot.guilds)
        members = len(set(self.bot.get_all_members()))

        shard_id = ctx.guild.shard_id
        shard = self.bot.get_shard(shard_id)
        shard_ping = round(shard.latency * 1000)
        shard_servers = len([guild for guild in self.bot.guilds if guild.shard_id == shard_id])
        diff = datetime.now() - self.start_time
        seconds = diff.seconds % 60
        minutes = (diff.seconds // 60) % 60
        hours = (diff.seconds // 3600) % 24
        days = diff.days
        text=f"{days} дней {hours}:{minutes}:{seconds}"

        embed=disnake.Embed(title=f"Моя статистика и информация обо мне | Кластер сервера: {shard_names[str(ctx.guild.shard_id)]}", description=f" - ||спасите... ***моргнул 3 раза***||", color=0x292B2F)  

        embed.add_field(name="Информация о серверах", value=guilds_info)
        embed.add_field(name="Информация о серверах", value=about_me_info)
        embed.add_field(name="Всё прочее", value=other_info)

        await ctx.send(embed=embed)

def setup(bot: commands.Bot):
    bot.add_cog(Info(bot))