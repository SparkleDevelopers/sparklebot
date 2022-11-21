import asyncio
import calendar as cld
import json
import random
import re
import typing
from datetime import datetime, timedelta
from io import BytesIO
from os import environ
from urllib.parse import quote
from typing import Literal
from bs4 import BeautifulSoup

import aiohttp
from humanize import naturaldelta
from PIL import Image
from textwrap3 import wrap

import disnake
from google.translator import GoogleTranslator
import emoji as emj
from bs4 import BeautifulSoup
from disnake.ext import commands
from disnake import SelectOption
import wikipedia

from Tools.buttons import CurrencyButton
from Tools.decoders import Decoder
from Tools.exceptions import CustomError
from Tools.links import emoji_converter
from Tools.paginator import Paginator
from core.classes.another_embeds import Field, Footer
import core


class WikiDropdown(disnake.ui.Select):
    def __init__(self, bot, author: disnake.Member, wiki_options: list):
        self.bot = bot
        self.author = author

        options = wiki_options
        super().__init__(
            placeholder="Выберите статью",
            min_values=1,
            max_values=1,
            options=options,
            custom_id="wiki_dropdown"
        )

    async def callback(self, inter):
        await inter.response.defer()

        if inter.author.id == self.author.id:
            data = wikipedia.page(title=wikipedia.search(self.values[0])[0])
            embeds = [disnake.Embed(title=data.title, url=data.url, description=i) for i in wrap(data.content, 1998)]
            await inter.edit_original_message(embed=embeds[0], view=Paginator(pages=embeds, author=inter.author))
        else:
            await inter.send('Не ты вызывал команду!', ephemeral=True)


class Utilities(commands.Cog, name="слэш-утилиты", description="Вроде некоторые команды полезны, хд."):

    COG_EMOJI = "🔧"

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.slash_command(
        description="Вывод аватара участника"
    )
    async def avatar(self, inter, user: disnake.User = commands.Param(lambda inter: inter.author)):
        formats = [
            f"[PNG]({user.display_avatar.replace(format='png', size=1024).url}) | ",
            f"[JPG]({user.display_avatar.replace(format='jpg', size=1024).url})",
            f" | [GIF]({user.display_avatar.replace(format='gif', size=1024).url})" if user.display_avatar.is_animated() else ""
        ]
        embed = disnake.Embed(
            title=f"Аватар {'бота' if user.bot else 'пользователя'} {user.name}",
            description=''.join(formats),
        )
        embed.set_image(url=user.display_avatar.url)
        return await inter.send(embed=embed)

    @commands.slash_command(
        description='Перевод в/из азбуки морзе.'
    )
    async def crypter(self, inter, decoder: typing.Literal['Морзе', 'Шифр Цезаря'],
                      variant: typing.Literal['crypt', 'decrypt'], text):
        if decoder == "Морзе":            
            if variant == 'crypt':
                morse = Decoder().to_morse(text)
            elif variant == 'decrypt':
                morse = Decoder().from_morse(text)

            embed = disnake.Embed(
                title='Decoder/Encoder морзе.',
                description=morse
            )

        elif decoder == "Шифр Цезаря":
            if variant == 'crypt':
                cezar = ''.join([chr(ord(i) + 3) for i in text])

            elif variant == 'decrypt':
                cezar = ''.join([chr(ord(i) - 3) for i in text])

            embed = disnake.Embed(
                title='Decoder/Encoder шифра Цезаря (3).',
                description=' '.join([i for i in cezar.split()])
            )

        await inter.send(embed=embed)

    @commands.slash_command(
        description="Вывод информации"
    )
    async def guild(self, inter: disnake.ApplicationCommandInteraction, guild: disnake.Guild = commands.Param(lambda inter: inter.guild)):
        channel_ids = sorted(list(i.id for i in guild.channels if not isinstance(i, disnake.CategoryChannel)))
        role_ids = sorted(list(i.id for i in guild.roles if i.id != guild.default_role.id and not i.is_integration()))
        member_ids = sorted(list(i.id for i in guild.members if not i.bot))
        last_joined = list(i.mention + ' | ' + f'<t:{round(i.joined_at.timestamp())}:R>' for i in guild.members if i.joined_at == sorted(list(map(lambda x: x.joined_at, list(filter(lambda x: x.id != guild.owner_id, guild.members)))))[-1])
        first_joined = list(i.mention + ' | ' + f'<t:{round(i.joined_at.timestamp())}:R>' for i in guild.members if i.joined_at == sorted(list(map(lambda x: x.joined_at, list(filter(lambda x: x.id != guild.owner_id, guild.members)))))[0])

        members = (f'Ботов: **{len(list(i.id for i in guild.members if i.bot))}** \nУчастников (не считая ботов): **{len(list(i.id for i in guild.members if not i.bot))}** \nУчастников <:offline:987690889147211776> (считая ботов): **{len(list(filter(lambda x: x.status == disnake.Status.online, guild.members)))}** \nУчастников <:dnd:987690886198595665>: **{len(list(filter(lambda x: x.status == disnake.Status.dnd, guild.members)))}** \nУчастников <:idle:987690887876345946>: **{len(list(filter(lambda x: x.status == disnake.Status.idle, guild.members)))}** \nУчастников <:offline:987690889147211776>: **{len(list(filter(lambda x: x.status == disnake.Status.offline, guild.members)))}**')
        dates = (f'Дата создания сервера: <t:{round(guild.created_at.timestamp())}:R> \nСамый старый канал: {guild.get_channel(channel_ids[0]).mention} | <t:{round(guild.get_channel(channel_ids[0]).created_at.timestamp())}:R> \nСамый молодой канал: {guild.get_channel(channel_ids[-1]).mention} | <t:{round(guild.get_channel(channel_ids[-1]).created_at.timestamp())}:R> \nСамая старая роль: {guild.get_role(role_ids[0]).mention} | <t:{round(guild.get_role(role_ids[0]).created_at.timestamp())}:R> \nСамая молодая роль: {guild.get_role(role_ids[-1]).mention} | <t:{round(guild.get_role(role_ids[-1]).created_at.timestamp())}:R> \nСамый старый участник: {guild.get_member(member_ids[0]).mention} | <t:{round(guild.get_member(member_ids[0]).created_at.timestamp())}:R> \nСамый молодой участник: {guild.get_member(member_ids[-1]).mention} | <t:{round(guild.get_member(member_ids[-1]).created_at.timestamp())}:R> \nПервый зашедший участник: {"".join(first_joined)} \nПоследний зашедший участник: {"".join(last_joined)}')
        boosts = (f'Включен ли прогресс бустов: **{"Да" if guild.premium_progress_bar_enabled else "Нет"}** \nБустеров: **{len(guild.premium_subscribers)}** \nУровень буста: **{guild.premium_tier}**')
        channels = (f'Всего каналов: **{len(guild.channels)}** \nГолосовых: **{len(guild.voice_channels)}** \nТекстовых: **{len(guild.text_channels)}** \nВеток: **{len(guild.threads)}** \nКанал правил: {guild.rules_channel.mention if guild.rules_channel else "Отсутствует"} \nСистемный канал (чат, куда приходят о том, что кто-то зашёл, бустах и пр.): {guild.system_channel.mention if guild.system_channel else "Отсутствует"}')
        other = (f'Стикеров: **{len(guild.stickers)}** \nЭмодзи: **{len(guild.emojis)}** \nСплэш: Отсутствует' if not guild.splash else f'Сплэш: [ссылка здесь]({guild.splash}) \nВладелец: {guild.owner.name} \nМаксимальное количество участников: **{guild.max_members}** \nАйди шарда: **{guild.shard_id}**')
        roles = (f'Количество ролей: **{len(guild.roles)}** \nВаша высшая роль: {inter.author.top_role.mention if inter.author in guild.members else "Вам нет на этом сервере("} \nРоль бустеров: {guild.premium_subscriber_role.mention if bool(guild.premium_subscriber_role) else "На сервере нет роли бустеров"}')

        embed = disnake.Embed(
            title=f'Информация о {guild.name}', 
            description='У сервера нет описания :(' if not guild.description else guild.description, 
        )
        embed.add_field(name="> Участники", value=members, inline=False)
        embed.add_field(name="> Даты", value=dates, inline=False)	
        embed.add_field(name="> Бусты", value=boosts, inline=False)	
        embed.add_field(name="> Каналы", value=channels, inline=False)	
        embed.add_field(name="> Роли", value=roles, inline=False)	
        embed.add_field(name="> Прочее", value=other, inline=False)	

        if guild.icon:
            embed.set_thumbnail(url=guild.icon.url)

        if guild.banner:
            embed.set_image(url=guild.banner.url)

        await inter.send(embed=embed)

    @commands.slash_command(name="user", description="Вывод информации о юзере")
    async def user(self, inter, user: disnake.User = commands.Param(lambda inter: inter.author)):
        statuses = {
            disnake.Status.online: '<:online:987690890443247646>',
            disnake.Status.dnd: '<:dnd:987690886198595665>',
            disnake.Status.idle: '<:idle:987690887876345946>',
            disnake.Status.offline: '<:offline:987690889147211776>'
        }
        embed = disnake.Embed(title=f'Информация о {"боте" if user.bot else "пользователе"} {user.name}')
        user = await self.bot.fetch_user(user.id)

        if user.banner:
            embed.set_image(url=user.banner.url)
        else:
            color = Image.open(BytesIO(await user.display_avatar.read())).resize((720, 720)).convert('RGB')
            img = Image.new('RGBA', (500, 200), '#%02x%02x%02x' % color.getpixel((360, 360)))
            img.save('banner.png', 'png')
            file = disnake.File(BytesIO(open('banner.png', 'rb').read()), filename='banner.png')
            
            embed.set_image(url='attachment://banner.png')

        embed.set_thumbnail(url=user.display_avatar.url)
        embed.set_footer(text=f"ID: {user.id}")
        embed.add_field(name='Статус в боте', value='Разработчик' if user.id in [578533097293873162, 805881717415346236] else 'Это я!' if user.id == self.bot.user.id else 'Пользователь', inline=True)

        main_information = [
            f"Зарегистрировался: **<t:{round(user.created_at.timestamp())}:R>** | {(datetime.utcnow() - user.created_at.replace(tzinfo=None)).days} дней",
            f"Полный никнейм: **{str(user)}**",
        ]

        if user in inter.guild.members:
            user_to_member = inter.guild.get_member(user.id)
            bool_to_symbol = {True: '+', False: '-'}

            embed.title = f'Информация о {"боте" if user.bot else "пользователе"} {user.name} {"📱" if user_to_member.is_on_mobile() else "🖥️"}'

            permissions_embed = disnake.Embed(
                title=f'Права {user_to_member}',
                description='```' + 'diff\n' + '\n'.join([f'{bool_to_symbol[i[-1]]} {i[0].replace("_", " ").capitalize()}' for i in user_to_member.guild_permissions]) + '```'
            )

            spotify = list(filter(lambda x: isinstance(x, disnake.activity.Spotify), user_to_member.activities))
            second_information = [
                f"Зашёл(-ла) на сервер: **<t:{round(user_to_member.joined_at.timestamp())}:R> | {(datetime.utcnow() - user_to_member.joined_at.replace(tzinfo=None)).days} дней**",
                f"Количество ролей: **{len(list(filter(lambda role: role, user_to_member.roles)))}**",
                f"Статус: {str(user_to_member.activity) + ' | ' if user_to_member.activity else ''}{statuses[user_to_member.status]}"
            ]

            if len(spotify):
                data = spotify[0]
                timestamps = (str(data._timestamps['end'])[:10], str(data._timestamps['start'])[:10])

                embed.add_field(
                    name="Информация про трек спотифай", 
                    value=f"Песня: [{data.title} | {', '.join(data.artists)}]({data.track_url})\n" \
                        f"Альбом: [{data.album}]({data.album_cover_url})\n" \
                        f"Длительность песни: {naturaldelta(data.duration.total_seconds())} | <t:{timestamps[0]}:R> - <t:{timestamps[-1]}:R>"
                )

        embed.description = "\n".join(main_information) + "\n" + "\n".join(
            second_information) if user in inter.guild.members else "\n".join(main_information)

        try:
            embeds = [embed, permissions_embed]
        except UnboundLocalError:
            embeds = [embed]
        
        if len(embeds) > 1:
            view = Paginator(embeds, inter.author)
        else:
            view = None

        try:
            await inter.send(embed=embeds[0], file=file)
        except UnboundLocalError:
            await inter.send(embed=embeds[0], view=view)


    @commands.slash_command(
        description="Получить эмодзик"
    )
    async def emoji(self, inter, emoji):
        if emoji in emj.UNICODE_EMOJI_ALIAS_ENGLISH:
            await inter.send(emoji)
        else:
            get_emoji_id = int(''.join(re.findall(r'[0-9]', emoji)))
            url = f"https://cdn.discordapp.com/emojis/{get_emoji_id}.gif?size=480&quality=lossless"
            embed = disnake.Embed(
                title=f"Эмодзи **{emoji}**",
                image=await emoji_converter('webp', url)
            )

            await inter.send(embed=embed)

    @commands.is_nsfw()
    @commands.slash_command(name='emoji-random', description="Я найду тебе рандомный эмодзик :3")
    async def random_emoji(self, inter):
        emoji = random.choice(self.bot.emojis)
        
        embed = disnake.Embed(description="Эмодзяяяяяяяя")
        embed.set_image(url=emoji.url)
        embed.add_field(name="Скачать эмодзик", value=f'[ТЫКТЫКТЫК]({emoji.url})')
        await inter.send(embed = embed)

    @commands.slash_command(
        name="random-anime",
        description="Вы же любите аниме? Я да, а вот тут я могу порекомендовать вам аниме!",
        guild_ids=[958094412397834321]
    )
    async def random_anime(self, inter):
        url = 'https://animego.org'

        async with aiohttp.ClientSession(
                headers={
                    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
                    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36 OPR/80.0.4170.91',
                }) as session:
            async with session.get(f'{url}/anime/random') as res:
                soup = BeautifulSoup(await res.text(), 'html.parser')
                name = soup.select('.anime-title')[0].find('h1', class_=False).text
                img = soup.find('div', class_='anime-poster').find('img', class_=False).get('src')
                desc = soup.find('div', class_='description').text
                url = f'{url}{res.url._val.path}'
                await session.close()
        desc = re.sub('\n', '', desc, 1)
        await inter.send(
            embed = disnake.Embed(
                description=f'**[{name}]({url})**\n**Описание**\n> {desc}',
                thumbnail=re.sub('media/cache/thumbs_\d{3}x\d{3}', '', img)
            )
        )

    @commands.slash_command(name="currency", description="Подскажу вам курс той или иной валюты :) (В рублях!)")
    async def currency_converter(self, inter, currency, how_many: float = 0):
        async with self.bot.session.get('https://www.cbr-xml-daily.ru/daily_json.js') as response:
            cb_data = await response.text()

        json_cb_data = json.loads(cb_data)
        get_currency = {i: j['Name'] for i, j in json_cb_data['Valute'].items()}
        data = json_cb_data["Valute"]
        view = CurrencyButton()

        if currency.upper() in data:
            upper_currency = currency.upper()
            embed = disnake.Embed(title=f'Курс - {get_currency[upper_currency]} ({upper_currency})', description=f'Один {get_currency[upper_currency]} на данный момент стоит **{round(data[upper_currency]["Value"], 2) / data[upper_currency]["Nominal"]}** рублей. ({round(data[upper_currency]["Value"] - data[upper_currency]["Previous"], 1)})')
            embed.add_field(name="Абсолютная погрешность", value=abs(data[upper_currency]["Value"] - round(data[upper_currency]["Value"])))
            embed.add_field(name="Прошлая стоимость", value=data[upper_currency]['Previous'] / data[upper_currency]['Nominal'])
            embed.add_field(name=f"Сколько **{how_many} {upper_currency}** в рублях", value=round(how_many * (data[upper_currency]['Value'] / data[upper_currency]['Nominal'])))
            embed.set_footer(text="Вся информация взята с официального API ЦБ РФ.", icon_url="https://cdn.discordapp.com/attachments/894108349367484446/951452412714045460/unknown.png?width=493&height=491")
            await inter.send(embed = embed, view=view)
        else:
            await inter.send(
                embed=disnake.Embed(
                    title='Курс... Так, стоп',
                    description="Такой валюты не существует! Попробуйте выбрать любую из валют (Кнопка ниже)"
                ), view=view
            )

    @commands.slash_command(description="Переведу тебе всё, что можно!")
    async def translate(self, inter, text, to_language, from_language='auto'):
        google = GoogleTranslator()
        data = await google.translate_async(text, to_language, from_language)
        
        embed = disnake.Embed(title='Спаркли-переводчик', description=data)
        embed.add_field(name="Оригинальный текст", value=text)
        embed.set_footer(text=f'Переводено с {from_language} на {to_language}', icon_url='https://upload.wikimedia.org/wikipedia/commons/thumb/d/d7/Google_Translate_logo.svg/1200px-Google_Translate_logo.svg.png')

        await inter.send(embed = embed)
        

    @commands.slash_command(description="Помогу решить почти любой пример!")
    async def calculator(self, inter, expression: str):
        async with self.bot.session.get(f'http://api.mathjs.org/v4/?expr={quote(expression)}') as response:
            data = await response.text()
        embed = disnake.Embed(title='Калькулятор')
        embed.add_field(name="Введённый пример", value = expression)
        embed.add_field(name="Результат", value = data)

        await inter.send(embed = embed)

    @commands.slash_command(name='role-info', description="Выдам информацию о любой роли на сервере")
    async def utilities_role_info(self, inter, role: disnake.Role):
        role_info_array = [
            f'Цвет роли: **{hex(role.color.value)}**',
            f'Интеграция: **{"Да" if role.is_integration() else "Нет"}**',
            f'Участников на этой роли: **{len(role.members)}**',
            f'ID роли: **{role.id}**',
            f'Упоминание роли: {role.mention}',
            f'Позиция: **{role.position}**',
            f'Роль создана: <t:{round(role.created_at.timestamp())}:D>'
        ]
        embed = disnake.Embed(
            title=f"Информация о {role.name}",
            description='\n'.join(role_info_array),
        )

        if role.icon:
            embed.set_thumbnail(url=role.icon.url)

        await inter.send(embed=embed)

    @commands.slash_command(
        name='wikipedia',
        description="Найдётся всё!"
    )
    async def utilities_wiki(self, inter, query: str) -> str:
        wikipedia.set_lang(prefix='ru')
        wiki_view = disnake.ui.View()

        if len(wikipedia.search(query)):
            wiki_view.add_item(
                WikiDropdown(
                    wiki_options=[SelectOption(label=i) for i in wikipedia.search(query)],
                    bot=self.bot,
                    author=inter.author
                )
            )
        else:
            wiki_view.add_item(disnake.ui.Button(label='Ничего не найдено :(', disabled=True))

        await inter.send(view=wiki_view)
        
    @commands.slash_command(
        name="invites",
        description="Показывает топ приглашений"
    )
    async def invites_top_info(self, inter):
        data = enumerate(sorted([(i.uses, str(i.inviter), i.url) for i in await inter.guild.invites()], key=lambda x: x[0], reverse=True))
        invite_data = list(data)
        yield_invite_data = lambda _: (f'{i[0]+1}. "{i[-1][-1].split("/")[-1]}" -> {i[1][0]} | {i[1][1]}' for i in invite_data if i[0]+1 <= 15)

        await inter.send(embed=disnake.Embed(title="Топ тех, кто приглашал", description='```py\n' + '\n'.join(list(yield_invite_data(invite_data))) + '```'))

def setup(bot: commands.Bot):
    bot.add_cog(Utilities(bot))