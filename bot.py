import time
import datetime
def time4logs():
    return f'[{datetime.datetime.now().strftime("%d.%m.%Y %H:%M:%S")}]'
print(time4logs(), 'Начало запуска бота')
start = time.time()
import logging
import sys
import os
import asyncio
import random
import sqlite3
import json
import traceback
import copy
import aiohttp
import Tools
import requests
from memory_profiler import memory_usage
import requests
import json
import io
import contextlib
import oauth
import textwrap
from traceback import format_exception
import asyncio
import subprocess
from disnake.utils import get
from disnake.ext import commands, tasks #del tasks after ver

from PIL import Image, ImageDraw, ImageFilter, ImageFont

from disnake.ext import commands #commands from external
from disnake.ext.commands import has_role #has a role
from disnake.ext.commands import has_permissions #permissions
from disnake.ext.commands import MissingPermissions #the missing perms
from disnake.ext.commands import BadArgument #incorrect arguments
from disnake.ext.commands import CheckFailure #failure

from disnake.utils import get
from disnake import utils

from asyncio import sleep

from disnake.ext.commands.errors import MissingPermissions
from disnake.ext.commands.errors import BadArgument
from disnake.ext.commands.errors import CheckFailure
from disnake.ext.commands import cooldown, BucketType
from config import *
from os import listdir

import disnake
import humanize
from disnake.ext import commands
from disnake.gateway import DiscordWebSocket
from jishaku.modules import find_extensions_in

from core.classes.embeds import Embeds
from core.classes.another_embeds import SparkleEmbed
from core.classes.custom_context import SparkleContext

from Tools.mobile_status import sparkle_mobile_identify

from Tools import prefix as prefixes
print(time4logs(), 'Библиотеки импортированы')
print(time4logs(), "Версия disnake:", disnake.__version__)


#Начало кода бота

CONFIG = json.load(open("config.json"))
TOKEN = CONFIG["token"]
DEFAULTPREFIX = CONFIG["default_prefix"]
INVITE = "https://discord.com/api/oauth2/authorize?client_id=932281102486372443&permissions=8&scope=bot"
EMBEDFOOTER = "ЗОВУТ МАКСИМ#3903 | sparklebot.fun"
release = oauth.release
if release:
    token = Auth.discord_auth["release"]
else:
    token = Auth.discord_auth["debug"]
    
begin = time.time()

class Sparkle(commands.AutoShardedBot):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.humanize = humanize.i18n.activate("ru_RU")
        self.embeds = Embeds(0xa8a6f0)
        self.embed = SparkleEmbed
        self.config = Config()
        DiscordWebSocket.identify = sparkle_mobile_identify
        
    def __getitem__(self, item: str) -> commands.Command:
        return self.get_command(item)


    def __delitem__(self, item: str) -> commands.Command:
        return self.remove_command(item)
        
    async def get_context(self, message, *, cls=SparkleContext):
        return await super().get_context(message=message, cls=cls)

    async def on_ready(self):
        if not self.checks.nsfw.is_running():
            self.checks.nsfw.start()

intents = disnake.Intents.all()
client = Sparkle(command_prefix=prefixes.get2, intents=intents, strip_after_prefix=True, case_insensitive=True, enable_debug_events=False,status=disnake.Status.online)
client.remove_command("help")

intents = disnake.Intents.all()
client = Sparkle(command_prefix=prefixes.get2, intents=intents, strip_after_prefix=True, case_insensitive=True, enable_debug_events=False,status=disnake.Status.online)
client.remove_command("help")

#База Данных
db = sqlite3.connect("data/database.db")
sql = db.cursor()

print(time4logs(), 'Подключение шардов')

for filename in os.listdir("./cogs"):
    if filename.endswith(".py") and not filename.startswith("_"):
        client.load_extension(f'cogs.{filename[:-3]}')
        print(time4logs(), f"Module {filename} is loaded!")

print(time4logs(), f"All modules is loaded!")
print(time4logs())



@client.event
async def on_ready():
    servers = len(client.guilds)
    members = 0
    for guild in client.guilds:
        members += guild.member_count - 1
    print(time4logs(), f"[INFO]")
    print(time4logs(), f"[INFO] Бот запущен под ником: {client.user}")
    print(time4logs(), f"[INFO] Разработчик: ЗОВУТ МАКСИМ#3903")
    print(time4logs(), f"[INFO] Айди бота: {client.user.id}")
    print(time4logs(), f"[INFO]")
    print(time4logs(), '[INFO] [STATUS] Статус включен!')
    #статус
    while True:
        await client.change_presence(activity=disnake.Game(name="🔥,help | sparklebot.tk"))
        await sleep(15)
        await client.change_presence(activity=disnake.Activity(type=disnake.ActivityType.watching, name="Beta 4.2"))
        await sleep(15)
        await client.change_presence(activity=disnake.Activity(type=disnake.ActivityType.watching, name=f"за {servers} серверов и {members} участников"))
        await sleep(15)

@client.event
async def on_guild_join(guild):
    prefixes.set(guild.id, DEFAULTPREFIX)
    print(f'{time4logs()} [INFO] Меня добавили на сервер! Айди: {guild.id}')
    

@client.event
async def on_shard_connect(shard_id):
    print(time4logs(), f'Шард {shard_id} готов к работе ;)')
        
@client.event
async def on_socket_raw_receive(msg):
    print('<<', msg)

@client.event
async def on_socket_raw_send(payload):
    print('>>', payload)
    
@client.command(name="ram", aliases = ["rams", "memory", "оперативка"])
async def ram(ctx):
    if ctx.author.id in [578533097293873162, 743821499839807608, 805881717415346236]:
        emb = disnake.Embed()
        emb.color = 0xffffff
        emb.title = "💿 | Оперативная память"
        emb.description = f"Использовано памяти: **{round(memory_usage()[0], 2)} Мб**."
        await ctx.send(embed = emb)
    else:
        await ctx.send("Недостаточно прав(")

@client.slash_command(name="ram", description="Посмотреть использованную оперативную память.")
async def ram(ctx):
    if ctx.author.id in [578533097293873162, 743821499839807608, 805881717415346236]:
        emb = disnake.Embed()
        emb.color = 0xffffff
        emb.title = "💿 | Оперативная память"
        emb.description = f"Использовано памяти: **{round(memory_usage()[0], 2)} Мб**."
        await ctx.send(embed = emb)
    else:
        await ctx.send("Недостаточно прав(")
        
        
async def print_ram():
    while True:
        print(f"Использовано памяти: {round(memory_usage()[0], 2)} Мб.")
        await asyncio.sleep(30)
        
guilds, ts = [], []

def clean_code(content):
    if content.startswith("```") and content.endswith("```"):
        return "\n".join(content.split("\n")[1:])[:-3]
    else:
        return content
        
@client.command(name="exec", aliases = ["eval", "e"])
async def _eval(ctx, *, code):
    #await ctx.message.delete()
    if ctx.author.id in [578533097293873162, 805881717415346236]:
        pending_embed = disnake.Embed(title = 'Добрый день!', description = 'Код выполняется, подождите...', color = disnake.Colour.from_rgb(255, 255, 0))
        message = await ctx.reply(embed = pending_embed)
        success_embed = disnake.Embed(title = 'Выполнение кода - успех', color = disnake.Colour.from_rgb(0, 255, 0))
        code = clean_code(code)
        local_variables = {
            "discord" : disnake,
            "disnake": disnake,
            "db": db,
            "commands": commands,
            "client": client,
            "bot": client,
            "ctx": ctx,
            "channel": ctx.channel,
            "author": ctx.author,
            "guild": ctx.guild,
            "message": ctx.message
        }
        stdout = io.StringIO()
        try:
            with contextlib.redirect_stdout(stdout):
                exec(
                    f"async def func():\n{textwrap.indent(code, '    ')}", local_variables,
                )
                obj = await local_variables["func"]()
                result = stdout.getvalue()
                success_embed.add_field(name = 'Выполненный код:', value = f'```py\n{code}\n```', inline = False)
                what_returned = None
                if obj != None:
                    if isinstance(obj, int) == True:
                        if obj == True:
                            what_returned = 'Логическое значение'
                        elif obj == False:
                            what_returned = 'Логическое значение'
                        else:
                            what_returned = 'Целое число'
                    elif isinstance(obj, str) == True:
                        what_returned = 'Строка'
                    elif isinstance(obj, float) == True:
                        what_returned = 'Дробное число'
                    elif isinstance(obj, list) == True:
                        what_returned = 'Список'
                    elif isinstance(obj, tuple) == True:
                        what_returned = 'Неизменяемый список'
                    elif isinstance(obj, set) == True:
                        what_returned = 'Уникальный список'
                    else:
                        what_returned = 'Неизвестный тип данных...'
                    success_embed.add_field(name = 'Тип данных:', value = f'```\n{what_returned}\n```', inline = False)
                    success_embed.add_field(name = 'Вернулось:', value = f'```\n{obj}\n```', inline = False)
                else:
                    pass
                if result:
                    success_embed.add_field(name = 'Результат выполнения:', value = f'```py\nКонсоль:\n\n{result}\n```', inline = False)
                else:
                    pass
                await message.edit(embed = success_embed)
        except Exception as e:
            result = "".join(format_exception(e, e, e.__traceback__))
            fail_embed = disnake.Embed(title = 'Выполнение кода - провал', color = disnake.Colour.from_rgb(255, 0, 0))
            fail_embed.add_field(name = 'Выполненный код:', value = f'```py\n{code}\n```', inline = False)
            fail_embed.add_field(name = 'Ошибка:', value = f'```py\n{e}\n```', inline = False)
            await message.edit(embed = fail_embed, delete_after = 60)
    else:
        fail_embed = disnake.Embed(title = 'Выполнение кода - провал', color = disnake.Colour.from_rgb(255, 0, 0))
        fail_embed.add_field(name = 'Выполненный код:', value = f'```py\nкод скрыт из-за соображений безопасности.\n```', inline = False)
        fail_embed.add_field(name = 'Ошибка:', value = f'```\nВы не имеете право запускать данную команду.\n```', inline = False)
        await ctx.reply(embed = fail_embed, delete_after = 60)

@client.slash_command(name="setprefix", description="Установить кастомный префикс.")
async def setprefix(ctx, newprefix: str = None):
    if ctx.author.guild_permissions.administrator:
        if newprefix is not None:
            prefixes.set(ctx.guild.id, newprefix)
            prefix = prefixes.get(ctx.guild.id)
            
            embed = disnake.Embed(title="<:yes:987416897073086565> Успешно!", description=f"На сервере теперь установлен префикс ` {prefix} `!", color=disnake.Color.green())

            await ctx.send(embed=embed)

        else:
            prefix = prefixes.get(ctx.guild.id)
            
            embed = disnake.Embed(title="<:no:987416933282488341> Неправильное использование", description=f"Попробуйте: `{prefix}setprefix (префикс)`", color=disnake.Color.red())

            await ctx.send(embed=embed)

@client.slash_command(name="load", description="Загрузить модуль.")
async def load (ctx, extension):
    if ctx.author.id in [578533097293873162, 805881717415346236]:
        client.load_extension(f"cogs.{extension}")
        embed=disnake.Embed(title="Load", description=f"Module ` {extension} ` successfully loaded!", color=0x292B2F)
        await ctx.send(embed=embed)
    else:
        await ctx.send("<:X_:946355338364469258> Данная команда недоступна!")
        

@client.slash_command(name="unload", description="Выгрузить модуль.")
async def unload (ctx, extension):
    if ctx.author.id in [578533097293873162, 805881717415346236]:
        client.unload_extension(f"cogs.{extension}")
        embed=disnake.Embed(title="Unload", description=f"Module ` {extension} ` successfully unloaded!", color=0x292B2F)
        await ctx.send(embed=embed)
    else:
        await ctx.send("<:X_:946355338364469258> Данная команда недоступна!")    

@client.slash_command(name="reload", description="Перезагрузит модуль.")
async def reload (ctx, extension):
    if ctx.author.id in [578533097293873162, 805881717415346236]:
        client.unload_extension(f"cogs.{extension}")
        client.load_extension(f"cogs.{extension}")
        embed=disnake.Embed(title="Reload", description=f"Module ` {extension} ` successfully reloaded!", color=0x292B2F)  
        await ctx.send(embed=embed)
    else:
        await ctx.send("<:X_:946355338364469258> Данная команда недоступна!")     

@client.command(name="ping")
async def ping(ctx: commands.Context):
    dpyVersion = disnake.__version__
    servers = len(client.guilds)
    members = len(set(client.get_all_members()))

    shard_id = ctx.guild.shard_id
    shard = client.get_shard(shard_id)
    shard_ping = round(shard.latency * 1000)
    shard_servers = len([guild for guild in client.guilds if guild.shard_id == shard_id])
    embed=disnake.Embed(title=f"<:pingapii:979443700721664010> API Connection: {round(client.latency * 1000)}ms.", color=0x292B2F)
    embed.add_field(name="Состояние шардов", value=f"Cкоро")
    await ctx.reply(embed=embed)
    

client.run(TOKEN)