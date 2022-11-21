import math
import random
from typing import Literal, Optional

import disnake
import emoji as emj
from disnake.ext import commands

from core.classes.another_embeds import Field
from Tools.exceptions import CustomError


class Settings(commands.Cog, name='настройки', description="ЧТО ДЕЛАЕТ ЭТА КОМАНДА?!?!?!"):

    COG_EMOJI = "⚙️"

    def cog_check(self, inter):
        if not inter.author.guild_permissions.administrator:
            raise commands.MissingPermissions(['administrator'])
    
    @commands.slash_command(description="Настройки")
    @commands.has_permissions(administrator=True)
    async def settings(self, inter):
        ...

    @settings.sub_command_group(description="Автороли")
    async def autoroles(self, inter):
        ...

    @settings.sub_command_group(description="Логи")
    async def logs(self, inter):
        ...


    @settings.sub_command_group(name='reaction-role', description="Роли за реакцию")
    async def reaction_role(self, inter):
        ...

    @settings.sub_command_group(description="Установка авто-постинга NSFW канала")
    @commands.is_nsfw()
    async def nsfw(self, inter):
        ...

    @nsfw.sub_command(name='set', description='Установка авто-постинга NSFW канала')
    @commands.is_nsfw()
    async def nsfw_set(self, inter, channel: disnake.TextChannel):
        if await inter.bot.config.DB.nsfw.count_documents({"_id": inter.guild.id}) == 0:
            await inter.bot.config.DB.nsfw.insert_one({"_id": inter.guild.id, "channel": channel.id})
        else:
            await inter.bot.config.DB.nsfw.update_one({"_id": inter.guild.id}, {"$set": {"channel": channel.id}})

        await inter.send(
            embed=await inter.bot.embeds.simple(
                title='NSFW',
                description="Канал автопостинга NSFW был установлен, картинка отсылается каждые 30 секунд."
            )
        )
    
    @nsfw.sub_command(name='remove', description="Убирает авто-постинг в NSFW канал")
    @commands.is_nsfw()
    async def nsfw_remove(self, inter):
        if await inter.bot.config.DB.nsfw.count_documents({"_id": inter.guild.id}) == 0:
            raise CustomError('Ну... Сейчас нет каналов, куда я бы постила NSFW.')
        else:
            await inter.bot.config.DB.nsfw.delete_one({"_id": inter.guild.id})

        await inter.send(embed=await inter.bot.embeds.simple(title='Leyla settings **(posting)**', description="Канал автопостинга NSFW был убран."))
        
    @autoroles.sub_command(name="add-role", description="Настройка авторолей")
    async def add_autoroles(self, inter, role: disnake.Role):
        if role.is_integration():
            raise CustomError('Я не могу установить роль интеграции, как роль на авто-выдачу!')
        elif role >= inter.me.top_role:
            raise CustomError('Эта роль выше моей!')
        else:
            if await inter.bot.config.DB.autoroles.count_documents({"guild": inter.guild.id}) == 0:
                await inter.bot.config.DB.autoroles.insert_one({"guild": inter.guild.id, "roles": [role.id]})
            else:
                if role.id in dict(await inter.bot.config.DB.autoroles.find_one({"guild": inter.guild.id}))['roles']:
                    raise CustomError("Роль уже установлена")
                else:
                    await inter.bot.config.DB.autoroles.update_one({"guild": inter.guild.id}, {"$push": {"roles": role.id}})

            await inter.send(embed=await inter.bot.embeds.simple(
                    title='Leyla settings **(autoroles)**', 
                    description="Роль при входе на сервер установлена", 
                    footer={'text': f'Роль: {role.name}', 'icon_url': inter.guild.icon.url if inter.guild.icon else None}
                )
            )

    @autoroles.sub_command(name='remove-role', description='Удаляет роль с авторолей')
    async def remove_autorrole(self, inter, role: disnake.Role):
        if await inter.bot.config.DB.autoroles.count_documents({"guild": inter.guild.id}) == 0:
            raise CustomError('А где? Авторолей здесь нет ещё(')
        elif not role.id in dict(await inter.bot.config.DB.autoroles.find_one({"guild": inter.guild.id}))['roles']:
            raise CustomError("Эта роль не стоит в авторолях!")
        else:
            await inter.bot.config.DB.autoroles.update_one({"guild": inter.guild.id}, {"$pull": {"roles": role.id}})

        await inter.send(embed=await inter.bot.embeds.simple(
                title='Leyla settings **(autoroles)**', 
                description="Роль была убрана с авторолей!", 
                fields=[{'name': 'Роль', 'value': role.mention}]
            )
        )

    @logs.sub_command(name="moderation", description="Показ действий модераторов")
    async def logs_moderation(self, inter, mode: Literal['Включить', 'Выключить']):
        modes = {
            'Включить': True,
            'Выключить': False,
        }

        if await inter.bot.config.DB.logs.count_documents({"_id": inter.guild.id}) == 0:
            await inter.bot.config.DB.logs.insert_one({"_id": inter.guild.id, "moderation": modes[mode], 'channel': None})
        else:
            await inter.bot.config.DB.logs.update_one({"_id": inter.guild.id}, {"$set": {"moderation": modes[mode]}})

        await inter.send(
            embed=await inter.bot.embeds.simple(
                title='Leyla settings **(logs)**',
                description="Режим логирования модерации переключён!",
                fields=[{"name": "Режим", "value": mode}],
                footer={"text": "И да, у вас не указан канал логирования, не забудьте его тоже!", 'icon_url': inter.guild.icon.url if inter.guild.icon else inter.author.display_avatar.url} if dict(await inter.bot.config.DB.logs.find_one({"_id": inter.guild.id}))['channel'] else None
            )
        )

    @logs.sub_command(name="channel", description="Настройка кАнальчика для логов")
    async def logs_channel(self, inter, channel: disnake.TextChannel):
        if await inter.bot.config.DB.logs.count_documents({"guild": inter.guild.id}) == 0:
            await inter.bot.config.DB.logs.insert_one({"guild": inter.guild.id, "channel": channel.id})
        else:
            await inter.bot.config.DB.logs.update_one({"guild": inter.guild.id}, {"$set": {"channel": channel.id}})
        
        await inter.send(
            embed=await inter.bot.embeds.simple(
                title="Leyla settings **(logs)**", 
                description="Канал логов был установлен", 
                fields=[{"name": "Канал", "value": channel.mention}]
            )
        )

    @logs.sub_command(name="remove", description="Убирает кАнал логов")
    async def log_channel_remove(self, inter):
        if await inter.bot.config.DB.logs.count_documents({"guild": inter.guild.id}) == 0:
            raise CustomError("Канала логов на этом сервере и так нет :thinking:")
        else:
            await inter.bot.config.DB.logs.delete_one({"guild": inter.guild.id})
        
        await inter.send(embed=await inter.bot.embeds.simple(
                title="Leyla settings **(logs)**", 
                description="Канал логов был убран отседа u-u",
            )
        )

    @commands.slash_command(name="warn-limit", description="Указание наказания за достижение определённого количества предупреждений")
    async def warn_limit(
        self, inter, mode: Literal['Включить', 'Выключить'] = "Включить", 
        action: Literal['Кик', 'Мут', 'Бан'] = 'Мут', limit: int = 10,
        timeout_duration: int = None, timeout_unit: Literal['Секунды', 'Минуты', 'Часы', 'Дни'] = 'Секунды'
    ):
        actions = {
            'Мут': 'mute',
            'Бан': 'ban',
            'Кик': 'kick',
        }
        modes = {
            'Включить': True,
            'Выключить': False
        }

        if not None in (timeout_duration, timeout_unit):
            units = {
                'Секунды': timeout_duration,
                'Минуты': timeout_duration * 60,
                'Часы': timeout_duration * 60 * 60,
                'Дни': timeout_duration * 60 * 60 * 24
            }

        data = {"_id": inter.guild.id, "mode": modes[mode], "action": actions[action], "limit": limit}
        embed = await inter.bot.embeds.simple(
            title='**Automoderation (warn-limit))**',
            fields=[
                {"name": "Режим", "value": mode, "inline": True},
                {"name": "Действие", "value": action, "inline": True},
                {"name": "Лимит", "value": limit, "inline": True}
            ]
        )

        if await inter.bot.config.DB.warn_limit.count_documents({"_id": inter.guild.id}) == 0:
            match action:
                case 'Мут':
                    if not None in (timeout_duration, timeout_unit):
                        data.update({'timeout_duration': units[timeout_unit]})
                        await inter.bot.config.DB.warn_limit.insert_one(data)
                    else:
                        await inter.bot.config.DB.warn_limit.insert_one(data)
                case 'Бан':
                    await inter.bot.config.DB.warn_limit.insert_one(data)
                case 'Кик':
                    await inter.bot.config.DB.warn_limit.insert_one(data)
        else:
            match action:
                case 'Мут':
                    if not None in (timeout_duration, timeout_unit):
                        data.update({'timeout_duration': units[timeout_unit]})
                        await inter.bot.config.DB.warn_limit.update_one({"_id": inter.guild.id}, {"$set": data})
                    else:
                        await inter.bot.config.DB.warn_limit.update_one({"_id": inter.guild.id}, {"$set": data})
                case 'Бан':
                    await inter.bot.config.DB.warn_limit.update_one({"_id": inter.guild.id}, {"$set": data})
                case 'Кик':
                    await inter.bot.config.DB.warn_limit.update_one({"_id": inter.guild.id}, {"$set": data})

        await inter.send(embed=embed)

    @reaction_role.sub_command(name="set", description="Установка роли за реакцию на сообщение")
    async def reaction_role_set(self, inter, channel: disnake.TextChannel, message_id: str, role: disnake.Role, emoji):
        message = await channel.fetch_message(int(message_id))
        emoji_data = emoji if emoji in emj.UNICODE_EMOJI_ALIAS_ENGLISH else str(emoji)

        if await inter.bot.config.DB.emojirole.count_documents({"_id": int(message_id)}) == 0:
            await inter.bot.config.DB.emojirole.insert_one({"_id": message.id, "emojis": [{emoji_data: [role.id]}]})
        else:
            await inter.bot.config.DB.emojirole.update_one({"_id": message.id}, {"$push": {"emojis": {emoji_data: [role.id]}}})

        await inter.send(
            embed=await inter.bot.embeds.simple(
                title="Leyla settings **(reaction role)**", 
                description=f"Теперь при нажатии на реакцию, на том сообщение, что вы указали, будет выдаваться роль", 
                fields=[{"name": "Роль", "value": role, "inline": True}, {"name": "ID сообщения", "value": message_id, "inline": True}],
                thumbnail=inter.author.display_avatar.url
            ), ephemeral=True
        )
        await message.add_reaction(emoji)

    @reaction_role.sub_command(name="remove", description="Удаление ролей за реакцию на сообщении")
    async def reaction_role_remove(self, inter, message_id: Optional[disnake.Message]):
        if await inter.bot.config.DB.emojirole.count_documents({"_id": message_id.id}) == 0:
            raise CustomError("На этом сообщение нет ролей за реакцию")
        else:
            await inter.bot.config.DB.emojirole.delete_one({"_id": message_id.id})

        await inter.send(
            embed=await inter.bot.embeds.simple(
                title="Leyla settings **(reaction role)**", 
                description=f"Больше роли за реакцию на этом сообщении работать не будут!",
                thumbnail=inter.author.display_avatar.url
            ), ephemeral=True
        )

    @settings.sub_command(name="counter", description="Канал, который вы укажете, будет указывать количество участников")
    async def settings_counter(self, inter, channel_type: Literal['Текстовый', 'Голосовой']):
        permissions = {
            inter.guild.default_role: disnake.PermissionOverwrite(
                send_messages=False, 
                read_messages=False, 
                connect=False
            )
        }

        if channel_type == "Текстовый":
            channel = await inter.guild.create_text_channel(name=f"Участников: {len(inter.guild.members)}", overwrites=permissions)
        else:
            channel = await inter.guild.create_voice_channel(name=f"Участников: {len(inter.guild.members)}", overwrites=permissions)

        if await inter.bot.config.DB.counter.count_documents({"_id": inter.guild.id}) == 0:
            await inter.bot.config.DB.counter.insert_one({"_id": inter.guild.id, "channel": channel.id})
        else:
            await inter.bot.config.DB.counter.update_one({"_id": inter.guild.id}, {"$set": {"channel": channel.id}})

        await inter.send(
            embed=await inter.bot.embeds.simple(
                title="Leyla settings **(counter)**", 
                description="Всё, счётчик участников включен :)", 
                fields=[{"name": "Канал", "value": channel.mention}]
            )
        )

    @trigger.sub_command(name='set', description="Устанавливает триггер-слово/предложение")
    async def trigger_set(self, inter, message: str = commands.Param(default=None, name="сообщение"), response: str = commands.Param(default=None, name='ответ-на-сообщение')):
        if await inter.bot.config.DB.trigger.count_documents({"guild": inter.guild.id, "trigger_message": message}) == 0:
            await inter.bot.config.DB.trigger.insert_one({"guild": inter.guild.id, "trigger_message": message.lower(), "response": response, 'trigger_id': random.randint(10000, 99999)})
        else:
            raise CustomError("Триггер на такое сообщение уже существует")
        
        await inter.send(
            embed=await inter.bot.embeds.simple(
                title='Leyla settings **(trigger)**',
                description="Триггер-сообщение установлено!",
                fields=[
                    {"name": 'Сообщение', 'value': message},
                    {'name': 'Мой ответ на это', 'value': response}
                ]
            )
        )

    @trigger.sub_command(name='remove', description="Убирает триггер")
    async def trigger_remove(self, inter, trigger_id: int):
        if await inter.bot.config.DB.trigger.count_documents({"guild": inter.guild.id, "trigger_id": trigger_id}) > 0:
            await inter.bot.config.DB.trigger.delete_one({"guild": inter.guild.id, "trigger_id": trigger_id})
        else:
            raise CustomError("Триггер на такое сообщение не существует")
        
        await inter.send(
            embed=await inter.bot.embeds.simple(
                title='Leyla settings **(trigger)**',
                description="Триггер-сообщение убрано!"
            )
        )

    @trigger.sub_command(name='list', description="Список триггеров")
    async def trigger_list(self, inter, page: int = 1):
        data = [i async for i in inter.bot.config.DB.trigger.find({"guild": inter.guild.id})]
        items_per_page = 10
        pages = math.ceil(len(data) / items_per_page)
        start = (page - 1) * items_per_page
        end = start + items_per_page
        trigger = ''

        for i, j in enumerate(data[start:end], start=start):
            trigger += f'[{i+1}] **{j["trigger_id"]}** | {j["trigger_message"]} | {j["response"]}\n'

        embed = await inter.bot.embeds.simple(
            title=f"Количество триггеров — {len(data)}",
            description=trigger if data else "На сервере нет триггеров",
            footer={"text": f"Страница: {page}/{pages}", "icon_url": inter.author.display_avatar.url}
        )

        await inter.send(embed=embed)

def setup(bot):
    bot.add_cog(Settings(bot))
