from asyncio import sleep
from io import BytesIO
from typing import Literal
from random import randint, choices
from string import punctuation
from typing import Literal
from threading import Thread
import blurplefier
import aiohttp

import disnake
from disnake.ext import commands

from Tools.exceptions import CustomError
from Tools.images import ship_image
from services import waifu_pics

OVERLAY_DESCRIPTIONS = {
    'jail': '`{0}` За шо сидим?',
    'wasted': 'R.I.P. `{0}` погиб(-ла) смертью храбрых :D',
    'gay': '🤭',
    'triggered': 'ВЫАЫВОАЫАОЫВАЫВАРЫРАВЫРАЛО'
}



class Fun(commands.Cog, name="развлечения", description="Всякие там развлекающие команды, да."):

    def __init__(self, client):
        self.client = client
        self.client.session = aiohttp.ClientSession()

    @commands.slash_command(name="8ball")
    async def eightball(self, ctx, *, question):
        responses = ['Это точно',
                     'Без сомнения',
                     'Вы можете положиться на это',
                     'Определенно да',
                     'Это точно так',
                     'Как я вижу, да',
                     'Более вероятно',
                     'Да',
                     'Перспектива хорошая',
                     'Знаки указывают на да',
                     'Смешно,.. смешно',
                     'Отвыт туманный, попробуй ещё раз',
                     'Лучше не говорить тебе сейчас',
                     'Спроси позже',
                     'Сейчас не могу предсказать',
                     'Сконцентрируйся и спроси еще раз',
                     'Не рассчитывай на это',
                     'Перспектива не очень хорошая',
                     'Мои источники говорят нет',
                     'Очень сомнительно',
                     'Нет']

        message = disnake.Embed(title="8 Ball", colour=disnake.Colour.orange())
        message.add_field(name="Вопрос:", value=question, inline=False)
        message.add_field(name="Ответ:", value=random.choice(responses), inline=False)
        await ctx.send(embed=message)
        

                
    @commands.slash_command(description="Случайное число от a до b")
    async def random(self, inter: disnake.ApplicationCommandInteraction, a: int = commands.Param(description="Первое число"), b: int = commands.Param(description="Второе число")):
        if b < a or a == b:
            raise CustomError('Второе число не должно быть равно первому либо быть меньше чем оно owo')

        return await inter.send(f'Выпавшее число: {randint(a, b)}')
    
    @commands.slash_command(
        name="rps",
        description="Классическая для многих игра: камень, ножницы, бумага",
    )
    async def fun_rps(self, inter, user_choice: Literal['камень', 'ножницы', 'бумага']):
        variants = {'ножницы': 'бумага', 'камень': 'ножницы', 'бумага': 'камень'}
        bot_choice = ''.join(choices(list(variants.keys()), weights=[50, 30, 35], k=1))

        if user_choice == variants[bot_choice]:
            await inter.send(f'Я победила u-u! Мой выбор был: `{bot_choice}`')
        else:
            await inter.send(f'Ты победил(-а) (. Мой выбор был: `{bot_choice}`' if bot_choice != user_choice else f'Ничья, никто не победил 😅\n ||{user_choice} - {bot_choice}||')
            
    @commands.slash_command()
    async def fox(self, ctx):
        av = random.randint(1, 120)
        await ctx.send(f"https://randomfox.ca/?i={av}")
        
    @commands.slash_command(name="iq", description="Узнать IQ (это шутка)")       
    async def _iq(self, ctx, member: disnake.Member = None):
        iq = random.randint(10,300)
        if member == None:
            emb=disnake.Embed(color=0x600C90, title= "Тест на IQ", description=f"Мне кажеться что у вас **{iq}** IQ")
            await ctx.send(embed=emb)
        else:
            emb=disnake.Embed(color=0x600C90, title= "Тест на IQ", description=f"Мне кажеться что у {member.name} **{iq} IQ**")
            await ctx.send(embed=emb)
        
    @commands.slash_command(
        options=[
            disnake.Option(
                'choice', 'Выберите девАтЬку owo', 
                type=disnake.OptionType.string,
                required=True, 
                choices=['megumin', 'shinobu', 'awoo', 'neko', 'poke']
            )
        ],
        name='anime-girl',
        description="Аниме тянки"
    )
    async def anime_girl(self, inter: disnake.ApplicationCommandInteraction, choice: str):
        embed = disnake.Embed(title=f'{choice.title()} OwO')
        embed.set_image(url=await waifu_pics.get_image('sfw', choice.lower()))
        return await inter.send(embed=embed)

    @commands.slash_command(name="ship", description="Создание шип-картинки")
    async def ship_not_ship(
        self, 
        inter, 
        user_one: disnake.User,
        second_user: disnake.User
    ):
        await inter.response.defer()
        percentage = randint(1, 100)
        get_image = ship_image(percentage, user_one, second_user)
        file = disnake.File(get_image.image_bytes, 'ship_img.png')
        
        embed=disnake.Embed(title=f'*Связаны {user_one.name} на {second_user.name}*' if percentage > 30 else 'Хрусь 💔')
        embed.set_image(url='attachment://ship_img.png')

        await inter.send(embed=embed, file=file)
        
    @commands.slash_command(
        options=[
            disnake.Option(
                'overlay', 'выберите наложение', 
                type=disnake.OptionType.string,
                required=True, 
                choices=['wasted', 'jail', 'comrade', 'gay', 'glass', 'passed', 'triggered', 'blurple']
            ),
            disnake.Option('user', 'Выберите пользователя', type=disnake.OptionType.user, required=False)
        ],
        name='avatar-overlay',
        description="Накладывает разные эффекты на аватар."
    )
    async def overlay_image(self, inter: disnake.ApplicationCommandInteraction, overlay: str, user: disnake.User = commands.Param(lambda inter: inter.author)):
        if overlay == 'blurple':
            input_bytes = await user.display_avatar.read()
            extension, blurplefied_bytes = blurplefier.convert_image(
                input_bytes, blurplefier.Methods.CLASSIC
            )
            avatar_bytes = BytesIO(blurplefied_bytes)

            await inter.send(file=disnake.File(avatar_bytes, filename=f'blurplefied_file.{extension}'))
        else:
            async with self.client.session.get(f'https://some-random-api.ml/canvas/{overlay}?avatar={user.display_avatar.url}') as response:
                data = await response.read()
                image_bytes = BytesIO(data)
                image_filename = f'overlay.{"png" if overlay != "triggered" else "gif"}'
                embed = disnake.Embed(title=OVERLAY_DESCRIPTIONS.get(overlay).format(user) if overlay in OVERLAY_DESCRIPTIONS else disnake.embeds.EmptyEmbed)
                embed.set_image(url=f'attachment://{image_filename}')
                await inter.send(embed=embed, file=disnake.File(image_bytes, filename=image_filename))

def setup(client):
    client.add_cog(Fun(client))	