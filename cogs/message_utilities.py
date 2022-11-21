import platform
import sys
import asyncio
import re
import random
from datetime import datetime
from contextlib import suppress

import disnake
import psutil
from disnake.ext import commands

from core.classes.another_embeds import Field, Footer


class ProfileMenu(disnake.ui.Select):
    def __init__(self, user):
        self.user = user
        super().__init__(
            placeholder="Выбрать пол",
            custom_id='gender',
            min_values=1,
            max_values=1,
            options=[
                disnake.SelectOption(label='Мужской'),
                disnake.SelectOption(label='Женский')
            ]
        )

    async def callback(self, inter):
        ru_to_eng = {
            'Мужской': "male",
            'Женский': "female"
        }

        db = inter.bot.config.DB.gender
        
        if self.user.id == inter.author.id:
            if await db.count_documents({"_id": inter.author.id}) > 0:
                await db.update_one({"_id": inter.author.id}, {"$set": {"gender": ru_to_eng[self.values[0]]}})
            else:
                await db.insert_one({"_id": inter.author.id, "gender": ru_to_eng[self.values[0]]})

            await inter.send('Пол был указан.', ephemeral=True)
        else:
            await inter.send('Не пытайтесь поменять пол другим', ephemeral=True)


class MessageUtilities(commands.Cog, name='утилиты', description="Всякие ненужные, а может быть, и, вспомогательные команды"): # type: ignore

    def __init__(self, bot):
        self.bot = bot

    COG_EMOJI = '🔧'

    async def message_reference_author(self, ctx, message_id: int):
        data = await ctx.channel.fetch_message(message_id)
        return data.author


    @commands.slash_command(name="afk", description="Встали в афк? Ну ладно, подождём.", usage='afk [Причина]')
    async def message_utilities_afk_command(self, inter, *, reason: str = None):
        if await self.bot.config.DB.afk.count_documents({"guild": inter.guild.id, "member": inter.author.id}) == 0:
            await self.bot.config.DB.afk.insert_one({"guild": inter.guild.id, "member": inter.author.id,
                                                     "reason": reason if reason else "Без причины",
                                                     "time": datetime.now()})

        await inter.send(
            embed=await self.bot.embeds.simple(
                description=f"Я поставил вас в список AFK, ждём вашего возвращения :relaxed:\nПричина: {reason if reason else 'Без причины'}"
            )
        )

    @commands.slash_command(name="profile", description="Информация о вас во мне, как бы странно это не звучало", usage="profile <Пользователь>")
    async def message_utilities_profile(self, ctx, _user: disnake.User = None):
        user = _user if _user else await self.message_reference_author(ctx, ctx.message.reference.message_id if ctx.message.reference else ctx.message.id)

        if ctx.author.id == user.id:
            view = disnake.ui.View()

            view.add_item(disnake.ui.Button(label='Указать биографию', style=disnake.ButtonStyle.blurple, custom_id='bio_btn'))
            view.add_item(disnake.ui.Button(label='Указать возраст', style=disnake.ButtonStyle.blurple, custom_id='age_btn'))
            view.add_item(ProfileMenu(user=user))

        warns_count = await self.bot.config.DB.warns.count_documents({"member": user.id})
        warns_guild_count = await self.bot.config.DB.warns.count_documents({"guild": ctx.guild.id, "member": user.id})

        gender = {
            'male': "Мужской",
            'female': "Женский"
        }
        gender_db = self.bot.config.DB.gender

        if await gender_db.count_documents({'_id': user.id}) > 0:
            get_gender = gender[dict(await gender_db.find_one({"_id": user.id}))['gender']]
        else:
            get_gender = 'Не указан'

        if await self.bot.config.DB.marries.count_documents({'$or': [{'_id': user.id}, {'mate': user.id}]}) > 0:
            data = await self.bot.config.DB.marries.find_one({'$or': [{'_id': user.id}, {'mate': user.id}]})
            key = {v:k for k, v in data.items()}[user.id]
            marry_data: disnake.User = await self.bot.fetch_user(int(data['_id'] if key == 'mate' else data['mate']))
        else:
            marry_data = 'Нет пары'

        if await self.bot.config.DB.badges.count_documents({"_id": user.id}) > 0:
            badge_data = ' '.join(dict(await self.bot.config.DB.badges.find_one({"_id": user.id}))['badges'])
        else:
            badge_data = 'Значков нет'
        
        level_data = await self.bot.config.DB.levels.find_one({"guild": ctx.guild.id, "member": user.id})

        if await self.bot.config.DB.levels.find_one({"_id": ctx.guild.id}):
            if user.bot:
                levels = 'У ботов нет рангов('
            else:
                levels = f'LVL: {level_data["lvl"]}\nXP: {level_data["xp"]} / {5*(level_data["lvl"]**2)+50*level_data["lvl"]+100}'
        else:
            levels = 'Выключено'

        bio_and_age = lambda x: self.bot.config.DB.get_collection(x)

        if await bio_and_age('bio').count_documents({"guild": ctx.guild.id, "member": user.id}) > 0:
            data = await bio_and_age('bio').find_one({"guild": ctx.guild.id, "member": user.id})
            bio = data['bio']
        else:
            bio = 'Биография не указана'

        if await bio_and_age('age').count_documents({"_id": user.id}) > 0:
            data = await bio_and_age('age').find_one({"_id": user.id})

            age = data['age']
        else:
            age = 'Возраст не указан'

        embed = self.bot.embed(
            title=f'Профиль {user.name}',
            description=bio,
            thumbnail=user.display_avatar.url,
            footer=Footer(
                text='Всё защищено, правда-правда!', 
                icon_url=self.bot.user.avatar.url
            )
        )

        embed.field(name='Уровни', value=levels, inline=True)
        embed.field(name='Предупреждений', value=f'Сервер: {warns_guild_count} | Глобально: {warns_count}', inline=True)
        embed.field(name='Статус в боте', value='Разработчик' if user.id in self.bot.owner_ids else 'Это я! <:AVAVVAVA:919119257063792670>' if user.id == self.bot.user.id else 'Пользователь', inline=True)
        embed.field(name='Вторая половинка', value=str(marry_data), inline=True)
        embed.field(name='Пол', value=get_gender, inline=True)
        embed.field(name='Возраст', value=age, inline=True)

        if badge_data != 'Значков нет':
            embed.field(name='Значки', value=badge_data, inline=True)
        
        if ctx.author.id == user.id:
            message = await ctx.send(
                embed=embed.start(),
                view=view
            )

            await asyncio.sleep(60) # timeout от View не работает(

            view.children[0].disabled = True # type: ignore
            view.children[1].disabled = True # type: ignore
            view.children[2].disabled = True # type: ignore

            await message.edit(view=view)
        else:
            await ctx.send(embed=embed.start())
        

    @commands.Cog.listener()
    async def on_button_click(self, inter):
        bio_and_age = lambda x: self.bot.config.DB.get_collection(x)

        if inter.component.custom_id == 'bio_btn':
            await inter.send('Напишите в чат вашу замечательную биографию! У вас есть 10 минут')

            with suppress(asyncio.TimeoutError):
                msg = await self.bot.wait_for('message', check=lambda x: x.author.id == inter.author.id and x.channel.id == inter.channel.id, timeout=600)

                if len(msg.content) > 2048:
                    await inter.send('Слишком длинная биография, попробуй меньше **2048** символов!')
                else:
                    if await bio_and_age('bio').count_documents({"guild": inter.guild.id, "member": inter.author.id}) == 0:
                        await self.bot.config.DB.bio.insert_one({"guild": inter.guild.id, "member": inter.author.id, "bio": msg.content})
                    else:
                        await self.bot.config.DB.bio.update_one({"guild": inter.guild.id, "member": inter.author.id}, {"$set": {"bio": msg.content}})

                    await msg.add_reaction('✅')

        if inter.component.custom_id == 'age_btn':
            await inter.send('Введите в чат Ваш возраст. У вас минута')

            with suppress((ValueError, asyncio.TimeoutError)):
                age_msg = await self.bot.wait_for('message', check=lambda x: x.author.id == inter.author.id and isinstance(int(x.content), int), timeout=60)
                
                if int(age_msg.content) < 13:
                    await inter.send('В смысле ты младше 13? Что ты тут делаешь?')
                elif int(age_msg.content) >= 120:
                    await inter.send('Тиво-тиво? Сколько-сколько лет?')
                else:
                    if await bio_and_age('age').count_documents({"_id": inter.author.id}) == 0:
                        await self.bot.config.DB.age.insert_one({"_id": inter.author.id, "age": age_msg.content})
                    else:
                        await self.bot.config.DB.age.update_one({"_id": inter.author.id}, {"$set": {"age": age_msg.content}})
                        
                    await age_msg.add_reaction('✅')
        
    @commands.slash_command(name='joke', description='Не смешно. Не смеёмся')
    async def message_utilities_joke(self, ctx):
        response = await self.bot.session.get(f'https://millionstatusov.ru/umor/page-{random.randint(1, 523)}.html')
        data = await response.read()

        data = data.decode('utf-8')
        quote = random.choice([i.strip() for i in re.findall(r'(?s)class="(?:t0|cont_text)">(.*?)<', data)])

        await ctx.reply(quote)

def setup(bot):
    bot.add_cog(MessageUtilities(bot))
