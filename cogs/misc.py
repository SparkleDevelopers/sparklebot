import disnake,sqlite3
from disnake.ext import commands
from utils import prefix as prefixes

class Misc(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.filtered_words = ['idiot', 'Idiots', "DIE", "ass", "butt", "Fool", "shit", "bitch"]
        self.INVITE_LINK = "https://disnakeapp.com/oauth2/authorize?&client_id=768695035092271124&scope=bot&permissions=21474836398"
        db = sqlite3.connect("data/Suggest.db")
        cursor = db.cursor()
        cursor.execute("""CREATE TABLE IF NOT EXISTS suggestion(
        schannel BIGINT,
        guildid BIGINT)""")
        db.commit()
        db.close()
	
    @commands.slash_command()
    async def suggest(self,ctx,*,sugest = None):
        prefix = prefixes.get(ctx.guild.id)
        if sugest == None:
            return await ctx.send("Обязательно укажите идею!") 
        db = sqlite3.connect("data/Suggest.db")
        cursor = db.cursor()
        cursor.execute(f"SELECT schannel FROM suggestion WHERE guildid='{ctx.message.guild.id}'")
        res = cursor.fetchall()
        if not res:
            await ctx.send("На этом сервере идеи отключены.\n Включить можно командой `suggest_set`")
        else:
            for i in cursor.execute(f"SELECT schannel FROM suggestion WHERE guildid='{ctx.message.guild.id}'"):
                suggest = i[0]
                sug = self.bot.get_channel(suggest)
                embed = disnake.Embed(title=f"{ctx.message.author} отправил идею!",description=f"Текст идеи: \n{sugest}",color =0x26bbe0)
                embed.set_footer(text=f'Чтобы отправить идею вам необходимо написать команду {prefix}suggest [Текст идеи]')
                mesage = await sug.send(embed = embed)
                await ctx.reply("Вы успешно отправили свою идею!")
                await mesage.add_reaction("<:yes:987416897073086565>")
                await mesage.add_reaction("➖")
                await mesage.add_reaction("<:no:987416933282488341>")
        db.close()
    
    @commands.slash_command()
    @commands.has_permissions(administrator= True)
    async def suggest_set(self, ctx, id):
        prefix = prefixes.get(ctx.guild.id)
        db = sqlite3.connect("data/Suggest.db")
        cursor = db.cursor()
        cursor.execute(f"SELECT schannel FROM suggestion WHERE guildid='{ctx.message.guild.id}'")
        res = cursor.fetchall()
        if not res:
            cursor.execute(f"INSERT INTO suggestion VALUES('{id}','{ctx.message.guild.id}')")
            await ctx.send("Канал для идей успешно установлен")
            channel=self.bot.get_channel(id)
            embed = disnake.Embed(title=f"Приветствую!", description="В этом канале будут идеи для обновлений сервера!", color=0x292B2F)
            embed.set_footer(text=f'Чтобы отправить идею вам необходимо написать команду {prefix}suggest [Текст идеи]')
            await channel.send(embed=embed)
            db.commit()
        else:
            cursor.execute(f"UPDATE suggestion SET schannel='{id}' WHERE guildid='{ctx.message.guild.id}'")
            await ctx.send("Канал идей успешно обновлен")
            channel=self.bot.get_channel(id)
            embed = disnake.Embed(title=f"Приветствую!", description="В этом канале будут идеи для обновлений сервера!", color=0x292B2F)
            embed.set_footer(text=f'Чтобы отправить идею вам необходимо написать команду {prefix}suggest [Текст идеи]')
            await channel.send(embed=embed)
            db.commit()
        db.close()

    @commands.slash_command()
    @commands.has_permissions(administrator=True)
    async def suggest_off(self, ctx):
        db = sqlite3.connect("data/Suggest.db")
        cursor = db.cursor()
        cursor.execute(f"SELECT schannel FROM suggestion WHERE guildid='{ctx.message.guild.id}'")
        res = cursor.fetchall()
        if not res:
            return await ctx.send("На этом сервере и так отключены идеи")
        else:
            cursor.execute(f"DELETE FROM suggestion WHERE guildid='{ctx.message.guild.id}'")
            db.commit()
            await ctx.send("Идеи успешно отключены")
            
    @commands.slash_command()
    async def invite(self, ctx):
        embed = disnake.Embed(title = "Invite Link:", color = ctx.author.color)
        embed.add_field(name = "Here:", value = f"[Click me]({self.INVITE_LINK})")
        await ctx.send(embed = embed)

    @commands.slash_command(aliases = ["sc"])
    async def servercount(self, ctx):
        sc = 0
        for i in self.bot.guilds:
            sc += 1
        embed = disnake.Embed(title = "Server Count", color = ctx.author.color)
        embed.add_field(name = "Server Count:", value = f"`{sc}`")
        embed.add_field(name = "User Count:", value = f'`{len(self.bot.users)}`')
        await ctx.send(embed = embed)

def setup(bot):
    bot.add_cog(Misc(bot))