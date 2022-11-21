from disnake.ext import commands
import disnake
import json


class Servers(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        shard_id = guild.shard_id
        name = guild.name
        id = guild.id
        guild_owner = guild.owner
        members = guild.member_count
        servers = len(self.bot.guilds)
        embed=disnake.Embed(title=f"<a:yes:987790425135935578> Бот был добавлен на сервер!", description="", color=0x2ecc71)
        embed.add_field(name="Название сервера:", value=f"` {name}  [Shard #{shard_id}] `", inline=False)
        embed.add_field(name="Владелец сервера:", value=f"` {guild_owner} `", inline=False)
        embed.add_field(name="ID сервера:", value=f"` {id} `", inline=False)
        embed.add_field(name="Участников на сервере:", value=f"` {members} `", inline=False)
        embed.add_field(name="Серверов у бота:", value=f"` {servers} `", inline=False)
        channel = self.bot.get_channel(986593661259227196)
        await channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_guild_remove(self, guild):
        shard_id = guild.shard_id
        name = guild.name
        id = guild.id
        owner = guild.owner
        members = guild.member_count
        servers = len(self.bot.guilds)
        embed=disnake.Embed(title=f"<a:no:987790686793367654> Бот был удален с сервера!", description="", color=0xe74c3c)
        embed.add_field(name="Название сервера:", value=f"` {name}  [Shard #{shard_id}] `", inline=False)
        embed.add_field(name="Владелец сервера:", value=f"` {owner} `", inline=False)
        embed.add_field(name="ID сервера:", value=f"` {id} `", inline=False)
        embed.add_field(name="Участников на сервере:", value=f"` {members} `", inline=False)
        embed.add_field(name="Серверов у бота:", value=f"` {servers} `", inline=False)
        channel = self.bot.get_channel(986593661259227196)
        await channel.send(embed=embed)


def setup(bot: commands.Bot):
    bot.add_cog(Servers(bot))