import time
import datetime
def time4logs():
    return f'[{datetime.datetime.now().strftime("%d.%m.%Y %H:%M:%S")}]'
print(time4logs(), 'Начало запуска бота')
start = time.time()
import disnake
from disnake.ext import commands
import os
import pymongo
import asyncio
from disnake.utils import get
from config import *
import word
import cache
from profilactic import measures
from messages import send_graph
import oauth
from pyqiwip2p import QiwiP2P
from disnake import ButtonStyle
from disnake.ui import Button, ActionRow
print(time4logs(), 'Библиотеки импортированы')

mongo = pymongo.MongoClient('mongodb+srv://admin0001:llWW6Pw4FjmRtzNA@bot.ggs2v.mongodb.net/main?retryWrites=true&w=majorityы')
print(time4logs(), 'MongoDB подключена')

release = oauth.release
if release:
    token = Auth.discord_auth["release"]
else:
    token = Auth.discord_auth["debug"]

db = mongo.cp
default_prefixes = ['cp!', 'Cp!', 'CP!', 'cP!']

begin = time.time()

async def determine_prefix(bot, message):
    guild = message.guild
    if guild:
        try:
            return cache.configs_data[guild.id]["prefix"]
        except:
            return default_prefixes

class Botik(commands.AutoShardedBot):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.remove_command(help)

intents = disnake.Intents.all()
bot = Botik(command_prefix = determine_prefix, intents = intents, shard_count = Other.shard_count, activity = disnake.Activity(type = disnake.ActivityType.watching, name="за тобой, чтобы ты не кикнул бота"))
bot.remove_command('help')
p2p = QiwiP2P(Auth.qiwi_auth)
Other.p2p = p2p


for file in os.listdir('./cogs'):
    if file.endswith('.py') and not file in ["config.py", "mongo.py", "messages.py"]:
        bot.load_extension(f'cogs.{file[:-3]}')
        print(time4logs(), 'Кога', file[:-3], 'загружена')

print(time4logs(), 'Подключение шардов')

@bot.event
async def on_ready():
    print(f'{time4logs()} Бот загружен за {word.hms2(time.time() - start)}')
    await bot.change_presence(status = disnake.Status.online, activity = disnake.Activity(type=disnake.ActivityType.streaming, name=f"https://crashprotect.ru | Серверов: {word.unit(len(bot.guilds))}", url="https://www.youtube.com/watch?v=o-YBDTqX_ZU"))

@bot.event
async def on_shard_connect(shard_id):
    print(f'{time4logs()} Шард {shard_id} готов к работе ;)')
    if int(shard_id) == len(bot.shards) - 1:
    	Other.uptime = int(time.time())

@bot.event
async def on_guild_join(guild):
    def first(guild):
        for i in guild.text_channels:
            if i.permissions_for(guild.me).send_messages and i.permissions_for(guild.me).read_messages and i.permissions_for(guild.me).embed_links:
                return i
    if not guild.owner.id in cache.bl_data:
        async for entry in guild.audit_logs(limit = 1, action = disnake.AuditLogAction.bot_add):
            embed = disnake.Embed()
            embed.color = Color.primary
            embed.title = "👋 | Привет!"
            embed.description = "Спасибо, что добавил меня сюда, ведь теперь этот сервер под защитой.\n"
            try: prefix = cache.configs_data[guild.id]['prefix']
            except: prefix = "cp!"
            embed.description += f"Мой префикс – `{prefix}`. Для получения списка команд введи `{prefix}help`."
            embed.add_field(inline=False, name="Пожалуйста, сделай следующие действия:", value="""
`1.` Передвинь мою роль как можно выше, чтобы наказывать нарушителей;
`2.` Убедись, что у меня есть права администратора для работы.
            """)
            row = ActionRow(
                Button(
                    style=ButtonStyle.link,
                    label="Поддержка",
                    emoji="❔",
                    url="https://discord.gg/VtJuw3P7qE"
                ),
                Button(
                    style=ButtonStyle.link,
                    label="Документация",
                    emoji="📚",
                    url="https://docs.crashprotect.ru"
                )
            )
            await first(guild).send(embed=embed, components=[row])
            lb = disnake.Embed(title="🤖 | Бот был добавлен на сервер")
            lb.color = Color.success
            lb.description = f'''
**Название сервера:** {guild.name}
**Владелец:** {guild.owner}
**Количество участников:** {guild.member_count}
**Кто добавил:** {entry.user}
**ID:** {guild.id}
            '''
            try:
                lb.set_thumbnail(url=guild.icon.url)
            except:pass
            await bot.get_channel(1069491759920468018).send(embed=lb)
    else:
        embed = disnake.Embed(color = Color.danger)
        embed.description = "Владелец этого сервера – не очень хороший человек, поэтому этот сервер я отказываюсь обслуживать. Поддержка также не будет осуществляться."
        embed.add_field(name="Причина", value=cache.bl_data[guild.owner.id]["reason"])
        embed.set_footer(text="Ну что встал-то? Иди лавана ставь.")
        for g in bot.guilds:
            if g.owner.id == guild.owner.id:
                try: 
                    await first(g).send(embed=embed)
                    await g.leave()
                    lb = disnake.Embed(title="😡 | Сервер в черном списке!")
                    lb.color = Color.danger
                    lb.description = f'''
**Название сервера:** {g.name}
**Владелец:** {g.owner}
**Количество участников:** {g.member_count}
**ID:** {g.id}
                    '''
                    try:
                        lb.set_thumbnail(url=guild.icon.url)
                    except:pass
                    await bot.get_channel(1069491759920468018).send(embed=lb)
                except:
                    pass


@bot.event
async def on_guild_remove(guild):
    lb = disnake.Embed(title="😢 | К сожалению, этому серверу бот не понравился")
    lb.color = Color.danger
    lb.description = f'''
**Название сервера:** {guild.name}
**Владелец:** {guild.owner}
**Количество участников:** {guild.member_count}
**ID:** {guild.id}
    '''
    try:
        lb.set_thumbnail(url=guild.icon.url)
    except:pass
    await bot.get_channel(1069491759920468018).send(embed=lb)

async def checkbans():
    while True:
        for dictionary in cache.bans_data:
            try:
                guild = bot.get_guild(dictionary)
                for member in cache.bans_data[dictionary]:
                    if cache.bans_data[dictionary][member] <= int(time.time()):
                        user = bot.get_user(int(member))
                        await guild.unban(user)
                        #del cache.bans_data[dictionary][member]
                        cache.bans.delete(dictionary, {member: True})
            except:
                pass
        await asyncio.sleep(60)

async def checkmutes():
    while True:
        for dictionary in cache.mutes_data:
            try:
                guild = bot.get_guild(dictionary)
                if 'muterole' in cache.configs_data[dictionary]:
                    muterole = guild.get_role(cache.configs_data[dictionary]['muterole'])
                    for member in cache.mutes_data[dictionary]:
                        if cache.mutes_data[dictionary][member] <= int(time.time()):
                            user = guild.get_member(int(member))
                            if user is not None:
                                await user.remove_roles(muterole)
                            cache.mutes.delete(dictionary, {member: True})
            except:
                pass
        await asyncio.sleep(60)

async def checklocks():
    while True:
        for dictionary in cache.locks_data:
            try:
                guild = bot.get_guild(dictionary)
                for member in cache.locks_data[dictionary]:
                    if cache.locks_data[dictionary][member]['locked'] <= int(time.time()):
                        user = guild.get_member(int(member))
                        for role in cache.locks_data[dictionary][member]['roles']:
                            try:
                                await user.add_roles(guild.get_role(int(role)))
                            except:
                                pass
                        mngd = [r for r in user.roles if r.managed]
                        await mngd[0].edit(permissions=disnake.Permissions(permissions=cache.locks_data[dictionary][member]['managed']['perms']))
                        cache.locks.delete(dictionary, {member: True})
            except:
                pass
        await asyncio.sleep(60)

async def unquarantine():
    while True:
        for dictionary in cache.quarantine_data:
            try:
                guild = bot.get_guild(dictionary)
                for member in cache.quarantine_data[dictionary]:
                    if member.isdigit():
                        if cache.quarantine_data[dictionary][member]['end'] <= int(time.time()):
                            cache.quarantine.delete(guild.id, {member: True})
                            try: role = guild.get_role(cache.quarantine_data[guild.id]['role'])
                            except: role = None
                            if guild.get_member(int(member)) and role:
                                await guild.get_member(int(member)).remove_roles(role)
            except:
                pass
        await asyncio.sleep(60)

guilds, ts = [], []
        
@bot.command(aliases = ['exec', 'e'])
async def _exec(ctx, *, arg):
    if ctx.author.id == 723328085662892042:
        begin = time.time()
        arg = arg.replace("```py", '')
        arg = arg.replace("```", '')
        exec(
            f'async def __ex(ctx): ' +
            ''.join(f'\n {l}' for l in arg.split('\n'))
        )

        try:
            a = await locals()['__ex'](ctx)
            embed = disnake.Embed(color=Color.success, description=f"```py\n{a}\n```")
            embed.add_field(name="Время выполнения кода", value=str(round(time.time() - begin, 3)) + " сек")
            await ctx.send(embed=embed)
        except Exception as e:
            embed = disnake.Embed(color=Color.danger, description=f"```\n{e}\n```")
            await ctx.send(embed=embed)

@bot.event
async def on_command_completion(ctx):
    try: cc = cache.botstats_data[bot.user.id]["commands_completed"]
    except KeyError: cc = 0
    cache.botstats.add(bot.user.id, {"commands_completed": cc + 1})

@bot.command()
async def servers(ctx):
    global ts, guilds
    if 0.06 in ts: ts.pop(ts.index(0.06))
    if 0.06 in guilds: guilds.pop(guilds.index(0.06))
    await send_graph(ctx, ts[8:], guilds[8:], "Рост серверов", ylabel="Количество", xfields=True, yfields=True)

bot.loop.create_task(checkbans())
bot.loop.create_task(checklocks())
bot.loop.create_task(checkmutes())
bot.loop.create_task(unquarantine())


async def check_bills():
    while True:
        invoices = cache.invoices_data
        for invoice in invoices:
            try:
                try:
                    message = await bot.get_channel(invoices[invoice]['message'][0]).fetch_message(invoices[invoice]['message'][1])
                except:
                    message = None
                if not invoices[invoice]['paid']:
                    if str(p2p.check(str(invoices[invoice]['bill_id'])).status) == "PAID":
                        cache.premium.add(invoice, {'active': True})
                        cache.invoices.add(invoice, {'paid': True})
                        embed = disnake.Embed()
                        embed.title = "✅ | Счёт оплачен"
                        embed.description = "Счёт был успешно оплачен. Приятного пользования :)"
                        embed.color = Color.success
                        if message:
                            await message.edit(embed=embed, components=[])
                elif int(time.time()) > invoices[invoice]['expires'] and not invoices[invoice]['paid']:
                    embed = disnake.Embed()
                    embed.title = "⌛ | Счёт просрочен"
                    embed.description = "Вы слишком долго не оплачивали счёт, поэтому он просрочился. Если вы хотите, то можете снова выставить счёт."
                    embed.color = Color.danger
                    if message:
                        await message.edit(embed=embed, components=[])
            except:
                pass
            await asyncio.sleep(.2)
        await asyncio.sleep(40)

bot.loop.create_task(check_bills())
bot.run(token)
