import disnake
from disnake.ext import commands
from config import Color
import messages
import word
import punishments
import asyncio
import time
import cache
import typing
from word import ago
from disnake import ButtonStyle
from disnake.ui import Button, ActionRow

class ModCmd(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.cooldown(1, 30, commands.BucketType.guild)
    @commands.check(messages.check_perms)
    async def addroles(self, ctx, role: disnake.Role):
        if role >= ctx.author.top_role:
            await messages.err(ctx, "Данная роль находится не ниже вашей.", True)
        elif role.managed:
            await messages.err(ctx, "Данная роль является интеграцией. Она не может быть выдана или снята у участников.", True)
        elif role >= ctx.guild.get_member(self.bot.user.id).top_role:
            await messages.err(ctx, "Данная роль находится не ниже моей. Я не смогу её выдать.", True)
        elif role.permissions.administrator:
            await messages.err(ctx, "Данная роль имеет права администратора. В целях безопасности я её не выдам.", True)
        else:
            took = 0
            embed = disnake.Embed(title="⏳ | Подождите", description="Идёт выдача роли участникам.", color=Color.primary)
            msg = await ctx.send(embed=embed)
            for member in ctx.guild.members:
                if not member.bot and not role in member.roles:
                    try:
                        await member.add_roles(role)
                        took += 1
                    except:
                        pass
            if took == 0:
                embed = disnake.Embed(title="❌ | Не получилось", description="Данная роль не была выдана никому.", color=Color.danger)
            else:
                embed = disnake.Embed(title="✅ | Готово", description="Количество участников, получивших данную роль: **{}**.".format(took), color=Color.success)
            await msg.edit(embed=embed)

    @commands.command()
    @commands.cooldown(1, 30, commands.BucketType.guild)
    @commands.check(messages.check_perms)
    async def remroles(self, ctx, role: disnake.Role):
        if role >= ctx.author.top_role:
            await messages.err(ctx, "Данная роль находится не ниже вашей.", True)
        elif role.managed:
            await messages.err(ctx, "Данная роль является интеграцией. Она не может быть выдана или снята у участников.", True)
        elif role >= ctx.guild.get_member(self.bot.user.id).top_role:
            await messages.err(ctx, "Данная роль находится не ниже моей. Я не смогу её снять.", True)
        else:
            took = 0
            embed = disnake.Embed(title="⏳ | Подождите", description="Идёт снятие роли у участников.", color=Color.primary)
            msg = await ctx.send(embed=embed)
            for member in ctx.guild.members:
                if not member.bot and role in member.roles:
                    try:
                        await member.remove_roles(role)
                        took += 1
                    except:
                        pass
            if took == 0:
                embed = disnake.Embed(title="❌ | Не получилось", description="Данная роль не была ни у кого снята.", color=Color.danger)
            else:
                embed = disnake.Embed(title="✅ | Готово", description="Количество участников, у которых была снята роль: **{}**.".format(took), color=Color.success)
            await msg.edit(embed=embed)

    @commands.command()
    @commands.cooldown(1, 20, commands.BucketType.guild)
    @commands.check(messages.check_perms)
    async def kick(self, ctx, user: disnake.Member, *, reason = None):
        if user == ctx.author:
            await messages.err(ctx, "Кикать себя? Серьёзно?! Это не очень целесообразно.", True)
        elif user.top_role >= ctx.author.top_role:
            await messages.err(ctx, "Роль данного участника находится не ниже вашей.", True)
        elif user.id == self.bot.user.id:
            await messages.err(ctx, "Кикать меня? Серьёзно?! Это не очень целесообразно.", True)
        elif user.top_role >= ctx.guild.get_member(self.bot.user.id).top_role:
            await messages.err(ctx, "Роль данного участника находится не выше моей, я не смогу его кикнуть.", True)
        else:
            if reason is None:
                reason1 = 'Не указана'
                reason2 = 'Причина не указана'
            else:
                reason1, reason2 = reason, reason
            embed = disnake.Embed()
            try:
                await user.kick(reason=f'{ctx.author}: {reason2}')
                embed.color = Color.primary
                embed.title = '👢 | Кик'
                embed.description = f'''
**Пользователь:** {user} ({user.mention})
**Модератор:** {ctx.author} ({ctx.author.mention})
**Причина:** {reason1}
                '''
            except:
                embed.color = Color.danger
                embed.title = '❌ | Что-то пошло не так'
                embed.description = 'Я не смог кикнуть этого участника.'
            await ctx.send(embed=embed)

    @commands.command()
    @commands.cooldown(1, 20, commands.BucketType.guild)
    @commands.check(messages.check_perms)
    async def warn(self, ctx, user: disnake.Member, *, reason = None):
        if user == ctx.author:
            await messages.err(ctx, "Предупреждать себя? Серьёзно?! Это не очень целесообразно.", True)
        elif user.bot:
            await messages.err(ctx, "Вы не можете предупредить администратора.", True)
        elif user.top_role >= ctx.author.top_role:
            await messages.err(ctx, "Роль данного участника находится не ниже вашей.", True)
        elif user.id == self.bot.user.id:
            await messages.err(ctx, "Предупреждать меня? Серьёзно?! Это не очень целесообразно.", True)
        elif user.top_role >= ctx.guild.get_member(self.bot.user.id).top_role:
            await messages.err(ctx, "Роль данного участника находится не выше моей, я не смогу его предупредить.", True)
        else:
            if reason is None:
                reason = 'Не указана'
            w = await punishments.warn(ctx, user, reason=reason)
            embed = disnake.Embed()
            embed.color = Color.primary
            embed.title = f"⚠ | Предупреждение **#{w[1]}**"
            embed.description = f'''
**Пользователь:** {user} ({user.mention})
**Модератор:** {ctx.author} ({ctx.author.mention})
**Причина:** {reason}
                    '''
            await ctx.send(embed=embed)

    @commands.command(aliases=['uw'])
    @commands.cooldown(1, 20, commands.BucketType.guild)
    @commands.check(messages.check_perms)
    async def unwarn(self, ctx, user: disnake.Member, amount: int = 1):
        if user == ctx.author:
            await messages.err(ctx, "Снимать предупреждения у себя? Серьёзно?! Это не очень целесообразно.", True)
        elif user.bot:
            await messages.err(ctx, "Вы не можете снять предупреждения у администратора.", True)
        elif user.top_role >= ctx.author.top_role:
            await messages.err(ctx, "Роль данного участника находится не ниже вашей.", True)
        elif user.id == self.bot.user.id:
            await messages.err(ctx, "Снимать предупреждения у меня? Серьёзно?! Это не очень целесообразно.", True)
        elif user.top_role >= ctx.guild.get_member(self.bot.user.id).top_role:
            await messages.err(ctx, "Роль данного участника находится не выше моей, я не смогу снять предупреждения.", True)
        else:
            w = await punishments.unwarn(ctx, user, amount)
            if isinstance(w, int):
                embed = disnake.Embed()
                embed.color = Color.primary
                embed.title = f"⚠ | Снято {w} {word.word_correct(w, 'предупреждение', 'предупреждения', 'предупреждений')}"
                embed.description = f'''
    **Пользователь:** {user} ({user.mention})
    **Модератор:** {ctx.author} ({ctx.author.mention})
                        '''
                await ctx.send(embed=embed)
            else:
                await messages.err(ctx, 'Не получилось снять предупреждения.')

    @commands.command(aliases=['b'])
    @commands.cooldown(1, 20, commands.BucketType.guild)
    @commands.check(messages.check_perms)
    async def ban(self, ctx, user: disnake.User, time1: typing.Optional[str] = '0s', *, reason = None):
        if user == ctx.author:
            return await messages.err(ctx, "Банить себя? Серьёзно?! Это не очень целесообразно.", True)
        elif user.id == self.bot.user.id:
            return await messages.err(ctx, "Банить меня? Серьёзно?! Это не очень целесообразно.", True)
        if ctx.guild.get_member(user.id):
            user = ctx.guild.get_member(user.id)
            if user.top_role >= ctx.author.top_role:
                return await messages.err(ctx, "Роль данного участника находится не ниже вашей.", True)
            elif user.top_role >= ctx.guild.get_member(self.bot.user.id).top_role:
                return await messages.err(ctx, "Роль данного участника находится не выше моей, я не смогу его забанить.", True)
        if word.ishs(time1):
            tc = word.string_to_seconds(time1)
        else:
            tc = 0
            if reason is not None:
                reason = time1 + ' ' + reason
            else:
                reason = time1

        if reason is None:
            reason1 = 'Не указана'
            reason2 = 'Причина не указана'
        else:
            reason1, reason2 = reason, reason

        embed = disnake.Embed()
        try:
            embed.color = Color.danger
            if tc == 0:
                embed.title = '🔨 | Бан'
                embed.description = f'''
**Пользователь:** {user} ({user.mention})
**Модератор:** {ctx.author} ({ctx.author.mention})
**Причина:** {reason1}
                '''
                await ctx.guild.ban(user, reason=f'{ctx.author}: {reason2}')
                tc = 228133722
                await punishments.tempban(ctx, user, tc, reason1)
            else:
                embed.title = '🔨 | Временный бан'
                embed.description = f'''
**Пользователь:** {user} ({user.mention})
**Модератор:** {ctx.author} ({ctx.author.mention})
**Длительность:** {word.hms(float(tc))}
**Причина:** {reason1}
**Дата разбана:** <t:{int(time.time()) + tc}>
                '''
                await ctx.guild.ban(user, reason=f'{ctx.author}: {reason2} | {word.hms(float(tc))}')
                await punishments.tempban(ctx, user, tc, reason1)
            
        except:
            embed.color = Color.danger
            embed.title = '❌ | Что-то пошло не так'
            embed.description = 'Я не смог забанить этого участника.'
        await ctx.send(embed=embed)

    @commands.command(aliases=['mb', 'massban', 'mass-ban'])
    @commands.cooldown(1, 150, commands.BucketType.guild)
    @commands.check(messages.check_perms)
    async def mass_ban(self, ctx, users: commands.Greedy[disnake.User], time1: typing.Optional[str] = '0s', *, reason = None):
        def check(ctx, member):
            if ctx.guild.get_member(member.id):
                member = ctx.guild.get_member(member.id)
                return member != ctx.author and member.top_role < ctx.author.top_role and member.id != self.bot.user.id and member.top_role < ctx.guild.get_member(self.bot.user.id).top_role
            else:
                return member != ctx.author and member.id != self.bot.user.id
        if len(users) > 50:
            await messages.err(ctx, "Вы можете забанить за раз не более 50 пользователей.", True)
        else:
            if word.ishs(time1):
                tc = word.string_to_seconds(time1)
            else:
                tc = 0
                if reason is not None:
                    reason = time1 + ' ' + reason
                else:
                    reason = time1

            if reason is None:
                reason1 = 'Не указана'
                reason2 = 'Причина не указана'
            else:
                reason1, reason2 = reason, reason

            embed = disnake.Embed()
            embed.color = Color.danger
            banned = 0
            await ctx.send('⏳')
            if tc == 0:
                embed.title = f"🔨 | "
                tc = 228133722
            for user in users:
                if check(ctx, user):
                    try:
                        if tc != 228133722:
                            await ctx.guild.ban(user, reason=f'Массовый бан от {ctx.author}: {reason2} | {word.hms(tc)}')
                            await punishments.tempban(ctx, user, tc, reason1)
                        else:
                            await ctx.guild.ban(user, reason=f'Массовый бан от {ctx.author}: {reason2}')
                            await punishments.tempban(ctx, user, tc, reason1)
                        banned += 1
                        await asyncio.sleep(2)
                    except:
                        pass
            
            if banned > 0:
                if tc == 228133722:
                    embed.title = f"🔨 | {banned} {word.word_correct(banned, 'пользователь был забанен', 'пользователя были забанены', 'пользователей были забанены')}"
                    embed.description = f'''
**Модератор:** {ctx.author} ({ctx.author.mention})
**Причина:** {reason1}
                    '''
                else:
                    embed.title = f"🔨 | {banned} {word.word_correct(banned, 'пользователь был временно забанен', 'пользователя были временно забанены', 'пользователей были временно забанены')}"
                    embed.description = f'''
**Модератор:** {ctx.author} ({ctx.author.mention})
**Длительность:** {word.hms(float(tc))}
**Причина:** {reason1}
**Дата разбана:** <t:{int(time.time()) + tc}>
                    '''
            else:
                embed.title = "❌ | Никто не был забанен"
                embed.description = f'**Модератор:** {ctx.author} ({ctx.author.mention})'
            
            await ctx.send(embed=embed)

    @commands.command(aliases=['ub'])
    @commands.cooldown(1, 10, commands.BucketType.guild)
    @commands.check(messages.check_perms)
    async def unban(self, ctx, user: disnake.User):
        if user.id == ctx.author.id:
            await messages.err(ctx, "Разбанивать себя? Серьёзно?! Это не очень целесообразно.", True)
        elif user.id == self.bot.user.id:
            await messages.err(ctx, "Разбанивать меня? Серьёзно?! Это не очень целесообразно.", True)
        else:
            try:
                await ctx.guild.unban(user)
                embed = disnake.Embed(color=Color.success)
                embed.title = "🔓 | Разбан"
                embed.description = f'''
**Пользователь:** {user}
**Модератор:** {ctx.author} ({ctx.author.mention})
                '''
                await ctx.send(embed=embed)
            except:
                await messages.err(ctx, "Не удалось разбанить пользователя.", True)
            try:
                bans = cache.automoderation_data[ctx.guild.id]["bans"]
                del bans[str(user.id)]
                cache.automoderation.add(ctx.guild.id, {"bans": bans})
            except:
                pass

    @commands.command(aliases=['m'])
    @commands.cooldown(1, 20, commands.BucketType.guild)
    @commands.check(messages.check_perms)
    async def mute(self, ctx, user: disnake.Member, time1: typing.Optional[str] = '0s', *, reason = None):
        try:
            muted = cache.mutes_data[ctx.guild.id][str(user.id)]
            muted = True
        except:
            muted = False
        if user == ctx.author:
            await messages.err(ctx, "Мьютить себя? Серьёзно?! Это не очень целесообразно.", True)
        elif user.top_role >= ctx.author.top_role:
            await messages.err(ctx, "Роль данного участника находится не ниже вашей.", True)
        elif user.id == self.bot.user.id:
            await messages.err(ctx, "Мьютить меня? Серьёзно?! Это не очень целесообразно.", True)
        elif user.top_role >= ctx.guild.get_member(self.bot.user.id).top_role:
            await messages.err(ctx, "Роль данного участника находится не выше моей, я не смогу его замьютить.", True)
        elif user.guild_permissions.administrator:
            await messages.err(ctx, "Данный участник является администратором.", True)
        elif muted:
            await messages.err(ctx, "Данный участник уже замьючен.", True)
        else:
            
            if word.ishs(time1):
                tc = word.string_to_seconds(time1)
            else:
                tc = 0
                if reason is not None:
                    reason = time1 + ' ' + reason
                else:
                    reason = time1

            if reason is None:
                reason1 = 'Не указана'
            else:
                reason1 = reason

            embed = disnake.Embed()
            with ctx.channel.typing():
                try:
                    embed.color = Color.primary
                    if tc == 0:
                        embed.title = '🔇 | Мьют'
                        embed.description = f'''
    **Пользователь:** {user} ({user.mention})
    **Модератор:** {ctx.author} ({ctx.author.mention})
    **Причина:** {reason1}
                        '''
                        tc = 228133722
                    else:
                        embed.title = '🔇 | Временный мьют'
                        embed.description = f'''
    **Пользователь:** {user} ({user.mention})
    **Модератор:** {ctx.author} ({ctx.author.mention})
    **Длительность:** {word.hms(float(tc))}
    **Причина:** {reason1}
    **Дата размьюта:** <t:{int(time.time()) + tc}>
                        '''
                    
                    await punishments.tempmute(ctx, user, tc, reason1)
                    
                except:
                    embed.color = Color.danger
                    embed.title = '❌ | Что-то пошло не так'
                    embed.description = 'Я не смог замьютить этого участника.'
                await ctx.send(embed=embed)

    @commands.command(aliases=['lockbot', 'lock-bot', 'lb'])
    @commands.cooldown(1, 20, commands.BucketType.guild)
    @commands.check(messages.check_perms)
    async def lock_bot(self, ctx, user: disnake.Member, time1: typing.Optional[str] = '0s', *, reason = None):
        try:
            muted = cache.locks_data[ctx.guild.id][str(user.id)]
            muted = True
        except:
            muted = False
        if user == ctx.author:
            await messages.err(ctx, "Блокировать себя? Серьёзно?! Это не очень целесообразно.", True)
        elif not user.bot:
            await messages.err(ctx, "Вы не можете заблокировать пользователя.", True)
        elif user.top_role >= ctx.author.top_role:
            await messages.err(ctx, "Роль данного бота находится не ниже вашей.", True)
        elif user.id == self.bot.user.id:
            await messages.err(ctx, "Блокировать меня? Серьёзно?! Это не очень целесообразно.", True)
        elif user.top_role >= ctx.guild.get_member(self.bot.user.id).top_role:
            await messages.err(ctx, "Роль данного бота находится не выше моей, я не смогу его заблокировать.", True)
        elif muted:
            await messages.err(ctx, "Данный бот уже заблокирован.", True)
        else:
            
            if word.ishs(time1):
                tc = word.string_to_seconds(time1)
            else:
                tc = 0
                if reason is not None:
                    reason = time1 + ' ' + reason
                else:
                    reason = time1

            if reason is None:
                reason1 = 'Не указана'
            else:
                reason1 = reason

            embed = disnake.Embed()
            with ctx.channel.typing():
                try:
                    embed.color = Color.primary
                    if tc == 0:
                        embed.title = '🔒 | Бот заблокирован'
                        embed.description = f'''
    **Бот:** {user} ({user.mention})
    **Модератор:** {ctx.author} ({ctx.author.mention})
    **Причина:** {reason1}
                        '''
                        tc = 228133722
                    else:
                        embed.title = '🔒 | Бот временно заблокирован'
                        embed.description = f'''
    **Бот:** {user} ({user.mention})
    **Модератор:** {ctx.author} ({ctx.author.mention})
    **Длительность:** {word.hms(float(tc))}
    **Причина:** {reason1}
    **Дата разблокировки:** <t:{int(time.time()) + tc}>
                        '''
                    
                    await punishments.lockbot(ctx, user, tc)
                    
                except:
                    embed.color = Color.danger
                    embed.title = '❌ | Что-то пошло не так'
                    embed.description = 'Я не смог заблокировать этого бота.'
                await ctx.send(embed=embed)

    @commands.command(aliases=['unlockbot', 'unlock-bot', 'ulb'])
    @commands.cooldown(1, 20, commands.BucketType.guild)
    @commands.check(messages.check_perms)
    async def unlock_bot(self, ctx, user: disnake.Member):
        try:
            muted = cache.locks_data[ctx.guild.id][str(user.id)]
            muted = True
        except:
            muted = False
        if user == ctx.author:
            await messages.err(ctx, "Разблокировать себя? Серьёзно?! Это не очень целесообразно.", True)
        elif not user.bot:
            await messages.err(ctx, "Вы не можете разблокировать пользователя.", True)
        elif user.top_role >= ctx.author.top_role:
            await messages.err(ctx, "Роль данного бота находится не ниже вашей.", True)
        elif user.id == self.bot.user.id:
            await messages.err(ctx, "Разблокировать меня? Серьёзно?! Это не очень целесообразно.", True)
        elif user.top_role >= ctx.guild.get_member(self.bot.user.id).top_role:
            await messages.err(ctx, "Роль данного бота находится не выше моей, я не смогу его разблокировать.", True)
        elif not muted:
            await messages.err(ctx, "Данный бот уже разблокирован.", True)
        else:

            embed = disnake.Embed()
            with ctx.channel.typing():
                try:
                    embed.color = Color.primary
                    embed.title = '🔓 | Бот разблокирован'
                    embed.description = f'''
**Бот:** {user} ({user.mention})
**Модератор:** {ctx.author} ({ctx.author.mention})
                    '''
                    
                    await punishments.unlockbot(ctx, user)
                    
                except:
                    embed.color = Color.danger
                    embed.title = '❌ | Что-то пошло не так'
                    embed.description = 'Я не смог разблокировать этого бота.'
                await ctx.send(embed=embed)

    @commands.command(aliases=['clear'])
    @commands.cooldown(1, 20, commands.BucketType.guild)
    @commands.check(messages.check_perms)
    async def purge(self, ctx, user: typing.Optional[disnake.Member] = None, amount: int = 100):
        def check(msg):
            return msg.author == user
        if amount > 1000:
            await messages.err(ctx, "Вы не можете удалить больше 1000 сообщений.", True)
        else:
            embed = disnake.Embed(color=Color.primary)
            embed.title = "♻ | Очистка сообщений"
            if user is None:
                deleted = len(await ctx.channel.purge(limit=amount))
                embed.description = f'Удалено {deleted} {word.word_correct(deleted, "сообщение", "сообщения", "сообщений")}.'
            else:
                deleted = len(await ctx.channel.purge(limit=amount, check=check))
                embed.description = f'Удалено {deleted} {word.word_correct(deleted, "сообщение", "сообщения", "сообщений")} от {user.mention}.'
            await ctx.send(embed=embed, delete_after=60)

    @commands.command(aliases=['um'])
    @commands.cooldown(1, 20, commands.BucketType.guild)
    @commands.check(messages.check_perms)
    async def unmute(self, ctx, user: disnake.Member):
        try:
            muted = cache.mutes_data[ctx.guild.id][str(user.id)]
            muted = True
        except:
            muted = False
        if user == ctx.author:
            await messages.err(ctx, "Размьючивать себя? Серьёзно?! Это не очень целесообразно.", True)
        elif user.top_role >= ctx.author.top_role:
            await messages.err(ctx, "Роль данного участника находится не ниже вашей.", True)
        elif user.id == self.bot.user.id:
            await messages.err(ctx, "Размьючивать меня? Серьёзно?! Это не очень целесообразно.", True)
        elif user.top_role >= ctx.guild.get_member(self.bot.user.id).top_role:
            await messages.err(ctx, "Роль данного участника находится не выше моей, я не смогу его размьютить.", True)
        elif user.guild_permissions.administrator:
            await messages.err(ctx, "Данный участник является администратором.", True)
        elif not muted:
            await messages.err(ctx, "Данный участник не замьючен.", True)
        else:
            embed = disnake.Embed()
            with ctx.channel.typing():
                try:
                    await punishments.unmute(ctx, user)
                    embed.color = Color.success
                    embed.title = "🔊 | Размьют"
                    embed.description = f'''
**Пользователь:** {user} ({user.mention})
**Модератор:** {ctx.author} ({ctx.author.mention})
                    '''
                except:
                    embed.color = Color.danger
                    embed.title = '❌ | Что-то пошло не так'
                    embed.description = 'Я не смог размьютить этого участника.'
                await ctx.send(embed=embed)

    @commands.command()
    @commands.check(messages.check_perms)
    @commands.cooldown(1, 10, commands.BucketType.guild)
    async def lock(self, ctx, channel: disnake.TextChannel = None):
        if channel is None:
            channel = ctx.channel
        await channel.set_permissions(ctx.guild.default_role, send_messages=False, add_reactions=False)
        await ctx.message.add_reaction('🔒')

    @commands.command()
    @commands.check(messages.check_perms)
    @commands.cooldown(1, 10, commands.BucketType.guild)
    async def unlock(self, ctx, channel: disnake.TextChannel = None):
        if channel is None:
            channel = ctx.channel
        await channel.set_permissions(ctx.guild.default_role, send_messages=None, add_reactions=None)
        await ctx.message.add_reaction('🔓')

    @commands.command(aliases=['say'])
    @commands.check(messages.check_perms)
    @commands.cooldown(1, 10, commands.BucketType.guild)
    async def echo(self, ctx, *, msg):
        await ctx.send(msg)
        await ctx.message.delete()

    @commands.command()
    @commands.cooldown(1, 5, commands.BucketType.guild)
    async def warns(self, ctx, member: disnake.Member = None):
        if member is None:
            member = ctx.author
        if member.bot:
            await messages.err(ctx, 'Вы не можете просмотреть предупреждения бота.', True)
        else:
            try:
                w = cache.warns_data[ctx.guild.id]['members'][str(member.id)]
            except:
                w = 0
            if member == ctx.author:
                name = 'вас'
            else:
                name = f'**{member}**'
            await ctx.send(f"У {name} {w} {word.word_correct(w, 'предупреждение', 'предупреждения', 'предупреждений')}.")

    @commands.command(aliases=['serverbans', 'server-bans', 'sb'])
    @commands.cooldown(1, 5, commands.BucketType.guild)
    @commands.check(messages.check_perms)
    async def bans(self, ctx):
        pages = [{}]
        total = 0
        index = 0

        if ctx.guild.id in cache.bans_data:
            bd = cache.bans_data[ctx.guild.id]
            if "_id" in bd: del bd['_id']
        else:
            bd = {}

        for ban in bd:
            user = self.bot.get_user(int(ban))
            member = ctx.guild.get_member(int(ban))
            if user and not member:
                if len(list(pages[-1])) >= 10:
                    pages.append({})
                pages[-1][str(user)] = bd[ban]
                total += 1

        embed = disnake.Embed(title = "🔨 | Действующие баны", color = Color.primary)
        embed.set_footer(text=ctx.author, icon_url=ctx.author.display_avatar)
        if not total:
            embed.description = "Наказаний нет :)"
            return await ctx.send(embed=embed)

        embed.title += f" ({total})"

        def refresh_buttons():
            if len(pages) > 1:
                buttons = [
                    ActionRow(
                        Button(
                            style=ButtonStyle.blurple,
                            custom_id="back",
                            emoji="<:back2:1071709332758073355>",
                            disabled=index==0
                        ),
                        Button(
                            style=ButtonStyle.blurple,
                            custom_id="forward",
                            emoji="<:forward2:1071709543840624660>",
                            disabled=index==len(pages) - 1
                        ),
                        Button(
                            style=ButtonStyle.red,
                            custom_id="close",
                            emoji="<:close2:1071709845436244018>"
                        )
                    )
                ]
            else:
                    buttons = [
                    ActionRow(
                        Button(
                            style=ButtonStyle.red,
                            custom_id="close",
                            emoji="<:close2:1071709845436244018>"
                        )
                    )
                ]
            return buttons

        def refresh_embed():
            embed.clear_fields()
            embed.set_footer(text=f"{ctx.author} | Страница {index+1} из {len(pages)}", icon_url=ctx.author.display_avatar)
            for user in pages[index]:
                timestamp = pages[index][user]
                if timestamp > time.time():
                    if timestamp > 1800000000: t = "Никогда"
                    else: t = f"<t:{timestamp}:f> (<t:{timestamp}:R>)"
                    embed.add_field(name=user, value="> Дата разбана: " + t, inline=False)

        refresh_embed()
        msg = await ctx.send(embed = embed, components=refresh_buttons())
        async def refresh_all():
            refresh_embed()
            await msg.edit(embed=embed, components=refresh_buttons())

        def check(inter):
            return inter.message.id == msg.id

        while time.time() < time.time() + 600:
            inter = await self.bot.wait_for('interaction', check=check)
            if inter.author != ctx.author:
                await inter.reply("403 Forbidden", ephemeral=True)
            else:
                if inter.component.custom_id == "begin":
                    index = 0
                    await refresh_all()
                elif inter.component.custom_id == "back":
                    index -= 1
                    await refresh_all()
                if inter.component.custom_id == "forward":
                    index += 1
                    await refresh_all()
                if inter.component.custom_id == "end":
                    index = len(pages) - 1
                    await refresh_all()
                if inter.component.custom_id == "close":
                    break

        await msg.delete()

    @commands.command(aliases=['serversmutes', 'server-mutes', 'sm'])
    @commands.cooldown(1, 5, commands.BucketType.guild)
    @commands.check(messages.check_perms)
    async def mutes(self, ctx):
        pages = [{}]
        total = 0
        index = 0

        if ctx.guild.id in cache.mutes_data:
            bd = cache.mutes_data[ctx.guild.id]
            if "_id" in bd: del bd['_id']
        else:
            bd = {}

        for mute in bd:
            user = self.bot.get_user(int(mute))
            member = ctx.guild.get_member(int(mute))
            if user and member:
                if len(list(pages[-1])) >= 10:
                    pages.append({})
                pages[-1][str(user)] = bd[mute]
                total += 1

        embed = disnake.Embed(title = "🔇 | Действующие мьюты", color = Color.primary)
        embed.set_footer(text=ctx.author, icon_url=ctx.author.display_avatar)
        if not total:
            embed.description = "Наказаний нет :)"
            return await ctx.send(embed=embed)

        embed.title += f" ({total})"

        def refresh_buttons():
            if len(pages) > 1:
                buttons = [
                    ActionRow(
                        Button(
                            style=ButtonStyle.blurple,
                            custom_id="back",
                            emoji="<:back2:1071709332758073355>",
                            disabled=index==0
                        ),
                        Button(
                            style=ButtonStyle.blurple,
                            custom_id="forward",
                            emoji="<:forward2:1071709543840624660>",
                            disabled=index==len(pages) - 1
                        ),
                        Button(
                            style=ButtonStyle.red,
                            custom_id="close",
                            emoji="<:close2:1071709845436244018>"
                        )
                    )
                ]
            else:
                    buttons = [
                    ActionRow(
                        Button(
                            style=ButtonStyle.red,
                            custom_id="close",
                            emoji="<:close2:1071709845436244018>"
                        )
                    )
                ]
            return buttons

        def refresh_embed():
            embed.clear_fields()
            embed.set_footer(text=f"{ctx.author} | Страница {index+1} из {len(pages)}", icon_url=ctx.author.display_avatar)
            for user in pages[index]:
                timestamp = pages[index][user]
                if timestamp > 1800000000: t = "Никогда"
                else: t = f"<t:{timestamp}:f> (<t:{timestamp}:R>)"
                embed.add_field(name=user, value="> Дата размьюта: " + t, inline=False)

        refresh_embed()
        msg = await ctx.send(embed = embed, components=refresh_buttons())
        async def refresh_all():
            refresh_embed()
            await msg.edit(embed=embed, components=refresh_buttons())

        def check(inter):
            return inter.message.id == msg.id

        while time.time() < time.time() + 600:
            inter = await self.bot.wait_for('interaction', check=check)
            if inter.author != ctx.author:
                await inter.reply("403 Forbidden", ephemeral=True)
            else:
                if inter.component.custom_id == "begin":
                    index = 0
                    await refresh_all()
                elif inter.component.custom_id == "back":
                    index -= 1
                    await refresh_all()
                if inter.component.custom_id == "forward":
                    index += 1
                    await refresh_all()
                if inter.component.custom_id == "end":
                    index = len(pages) - 1
                    await refresh_all()
                if inter.component.custom_id == "close":
                    break

        await msg.delete()


def setup(bot):
    bot.add_cog(ModCmd(bot))
