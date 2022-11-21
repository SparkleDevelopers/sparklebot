import disnake
from disnake.ext import commands
import json
import sqlite3
import requests
path = r"welcomeimage.png"
from PIL import Image, ImageDraw, ImageFilter, ImageFont

class Welcome(commands.Cog):

    def __init__(self, client):
        CONFIG = json.load(open("config.json"))
        self.client = client
        
    db = sqlite3.connect("data/welcome.db")
    cursor = db.cursor()
    cursor.execute("""CREATE TABLE IF NOT EXISTS welcome(
    wchannel BIGINT,
    guildid BIGINT)""")

    @commands.Cog.listener()
    async def on_member_join(self, member):
        db = sqlite3.connect("data/welcome.db")
        cursor = db.cursor()
        cursor.execute(f"SELECT wchannel FROM welcome WHERE guildid='{member.guild.id}'")
        res = cursor.fetchall()
        if not res:
            pass
        else:
            for wchannel in cursor.execute(f"SELECT wchannel FROM welcome WHERE guildid='{member.guild.id}'"):
                channel = wchannel[0]
                welchannel = self.client.get_channel(channel)
                with requests.get(member.display_avatar) as r:
                    img_data = r.content
                    with open('assets/profile.jpg', 'wb') as handler:
                        handler.write(img_data)
                        im1 = Image.open("assets/background.png")
                        im2 = Image.open("assets/profile.jpg")

                        # Font Stuff
                        draw = ImageDraw.Draw(im1)
                        font = ImageFont.truetype("fonts/BebasNeue-Regular.ttf", 32)
                        # Add the Text to the result image
                        draw.text((160, 40),f"Welcome {member.name}",(255,255,255),font=font)


                        size = 129

                        im2 = im2.resize((size, size), resample=0)
                        # Creates the mask for the profile picture
                        mask_im = Image.new("L", im2.size, 0)
                        draw = ImageDraw.Draw(mask_im)
                        draw.ellipse((0, 0, size, size), fill=255)

                        mask_im.save('mask_circle.png', quality=95)

                        # Masks the profile picture and adds it to the background.
                        back_im = im1.copy()
                        back_im.paste(im2, (11, 11), mask_im)


                        back_im.save('welcomeimage.png', quality=95)
                        # Stuff to send the embed with a local image.
                        f = disnake.File(path, filename="welcomeimage.png")

                        embed = disnake.Embed()
                        embed.set_image(url="attachment://welcomeimage.png")
                
                        await welchannel.send(member, file=f, embed=embed)
                        db.close()
 
    @commands.slash_command()
    @commands.has_permissions(administrator= True)
    async def welcome_set(self, ctx, id):
        if not id:
            return await ctx.send(":x: Обязательно укажите канал для приветствия!",delete_after=5)
        db = sqlite3.connect("data/welcome.db")
        cursor = db.cursor()
        cursor.execute(f"SELECT wchannel FROM welcome WHERE guildid='{ctx.message.guild.id}'")
        res = cursor.fetchall()
        if not res:
            cursor.execute(f"INSERT INTO welcome VALUES('{id}',{ctx.message.guild.id}) ")
            await ctx.send("Канал для приветствия успешно установлен!!!")
            db.commit()
			
        else:
            cursor.execute(f"UPDATE report SET wchannel='{id}'WHERE guildid='{ctx.message.guild.id}'")
            await ctx.send("Канал для жалоб обновлен")
            db.commit()
        db.close()
        
    @commands.slash_command()
    @commands.has_permissions(administrator= True)
    async def welcome_off(self, ctx):
        db = sqlite3.connect("data/welcome.db")
        cursor = db.cursor()
        cursor.execute(f"SELECT wchannel FROM welcome WHERE guildid='{ctx.message.guild.id}'")
        res = cursor.fetchall()
        if not res:
            return await ctx.send("Приветствие и так отключено")
        else:
            cursor.execute(f"DELETE FROM welcome WHERE guildid='{ctx.message.guild.id}'")
            await ctx.send("Приветствие успешно отключено!")
            db.commit()
            db.close()

def setup(client):
    client.add_cog(Welcome(client))