import discord
import sys
import os
import asyncio
import time
import random
from discord.ext import commands
from discord.utils import get
from discord import utils
from asyncio import sleep

global client
client = commands.Bot(command_prefix=',')
client.remove_command("help")
TOKEN = "OTMyMjgxMTAyNDg2MzcyNDQz.GAln7f.V7sWcwxs-ZLeRoc3eKCavbT5jMwk6oM657vOZ8"
client.author_id = 578533097293873162

@client.event
async def on_ready():
    global bot
    bot={client}
    while True:
        servers = len(client.guilds)
        members = 0
        for guild in client.guilds:
            members += guild.member_count - 1
        await client.change_presence(status=discord.Status.online, activity=discord.Game(",help | sparkle.mrezer.ml"))
        await sleep(15)
        await client.change_presence(status=discord.Status.online,activity=discord.Game("https://sparkle.mrezer.ml"))
        await sleep(15)
        await client.change_presence(activity = discord.Activity (type = discord.ActivityType.watching,name = f'{servers} сервера {members} участников'))
        await sleep(15)

@client.command()
async def load (ctx, extension):
    if ctx.author.id == 578533097293873162:
        client.load_extension(f"cogs.{extension}")
        embed=discord.Embed(title="Load", description=f"Module ` {extension} ` successfully loaded!", color=0x292B2F)
        await ctx.send(embed=embed)
    else:
        await ctx.send("<:X_:946355338364469258> Данная команда недоступна!")

@client.command()
async def unload (ctx, extension):
    if ctx.author.id == 578533097293873162:
        client.unload_extension(f"cogs.{extension}")
        embed=discord.Embed(title="Unload", description=f"Module ` {extension} ` successfully unloaded!", color=0x292B2F)
        await ctx.send(embed=embed)
    else:
        await ctx.send("<:X_:946355338364469258> Данная команда недоступна!")    

@client.command()
async def reload (ctx, extension):
    if ctx.author.id == 578533097293873162:
        client.unload_extension(f"cogs.{extension}")
        client.load_extension(f"cogs.{extension}")
        embed=discord.Embed(title="Reload", description=f"Module ` {extension} ` successfully reloaded!", color=0x292B2F)  
        await ctx.send(embed=embed)
    else:
        await ctx.send("<:X_:946355338364469258> Данная команда недоступна!")     

@client.command(name="ping")
async def ping(ctx: commands.Context):
    print("[INFO] [PING] Mention used ,ping")
    embed=discord.Embed(title=f"<:pingapii:979447062947049513> Bot latency: {round(client.latency * 1000)}ms.", color=0x292B2F)
    await ctx.send(embed=embed)

for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        client.load_extension(f'cogs.{filename[:-3]}')

class MyClient(discord.Client):
    async def on_ready(self):
        print('Logged on as {0}!'.format(self.user))
        
    async def on_message(self, message):
        print('Message from {0.author}: {0.content}'.format(message))

client.run(TOKEN)