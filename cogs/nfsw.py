import disnake
from disnake.ext import commands
import hmtai
import core


NSFW_DESCRIPTIONS = {
    'Анал :³ (anal)': 'anal',
    'Зопки :³ (ass)': 'ass',
    'БДСМ (Асуждаю) (bdsm)': 'bdsm',
    'КониТИВАААА (Слишком много йогуртика) (cum)': 'cum',
    'Да. (creampie)': 'creampie', 
    'Девушки тоже умеют... (femdom)': 'femdom', 
    'Просто хентай (hentai)': 'hentai',
    '×Агрессивные звуки осуждения× (incest)': 'incest',
    'Оказывается, не только мальчики др×чат (masturbation)': 'masturbation',
    'Эээ.. Ладно. (public)': 'public', 
    'ПаЛюБуЙтЕсЬ (ero)': 'ero', 
    'Оргия (orgy)': 'orgy', 
    'Эльфики uwu (elves)': 'elves', 
    'Девочка и девочка, хмм... (yuri)': 'yuri', 
    '(Мы, если честно, сами не знаем, что это.) (pantsu)': 'pantsu', 
    'В очках тоже неплохо) (glasses)': 'glasses', 
    'Куколд (cuckold)': 'cuckold', 
    'Блоуджоб (blowjob)': 'blowjob', 
    'Работа грудью, что))) (boobjob)': 'boobjob', 
    'Ношшшшшшшшшки (foor)': 'footjob', 
    'Ещё больше хентая (hentai gifs)': 'gif', 
    'Дыротька, не моя, нет( (pussy)': 'pussy', 
    'Ахегао, что ещё говорить? (ahegao)': 'ahegao', 
    'Школьницы и не только... ой. (uniform)': 'uniform', 
    'Щупальца (tentacles)': 'tentacles'
}


class NSFW(commands.Cog, name="nsfw", description="NSFW команды, что-то ещё?"):

    COG_EMOJI = "🥵"

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.slash_command(
        description='Ну... Это было неплохо.',
        options=[
            disnake.Option(
                'choice', 'Выбор картинки', 
                type=disnake.OptionType.string,
                required=True, 
                choices=[disnake.OptionChoice(x, x) for x in NSFW_DESCRIPTIONS.keys()]
            ),
        ]
    )
    @commands.is_nsfw()
    async def nsfw(self, inter: disnake.ApplicationCommandInteraction, choice: str = None):
        e = disnake.Embed()
        e.set_image(url=hmtai.useHM("29", NSFW_DESCRIPTIONS[choice]))
        return await inter.send(embed=e)


def setup(bot: commands.Bot):
    bot.add_cog(NSFW(bot))