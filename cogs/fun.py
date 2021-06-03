import discord
from discord.ext import commands, flags
import asyncio
import random
import aiosqlite
import typing

class Fun(commands.Cog):
    """
    Fun Commands
    """
    def __init__(self, osi):
        self.osi = osi

    # fight command
    @commands.command()
    async def fight(self, ctx, member:discord.Member):
        await ctx.send(f"{ctx.author.mention} its your chance, what do you want to do?\n\n**Beat/Smack/Hit**")

        def check(arg):
            return arg.author == ctx.author and arg.channel == ctx.channel
        msg = await self.osi.wait_for('message', check=check, timeout=15.0)

        if 'beat' in msg.content.lower():
            await ctx.send(f"{ctx.author.name}, you started beating up {member.name}")
        
        if 'smack' in msg.content.lower():
            await ctx.send(f"{ctx.author.name}, smacked {member.name}")
        
        if 'hit' in msg.content.lower():
            await ctx.send(f"{ctx.author.name}, hit {member.name} in the head, K.O")

    # roll command
    @commands.command(aliases=['bet', 'gamble'])
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def roll(self, ctx, amount, rigged=None):
        """
        Take a shot at the gamble command. 
        Totally not rigged:tm: ||except if you use the \`--rig` flag||
        If ya wanna view the source visit [here](https://github.com/drapespy/Osi)
        """
        if rigged and rigged == '--rig' and ctx.author.id in {583745403598405632, 710247495334232164, 596481615253733408}:
            urolls = (6, 6)
            brolls = (1, 1)
            multi = 110
        else:
            urolls = (random.randint(1, 6), random.randint(1, 6))
            brolls = (random.randint(1, 6), random.randint(1, 6))
            multi = random.randint(30, 110)

        winner = sum(urolls) > sum(brolls)
        draw = sum(urolls) == sum(brolls)
        lose = sum(urolls) < sum(brolls)
        USER_ID = ctx.message.author.id
        async with aiosqlite.connect("data/BankAccounts.db") as db:
            cur = await db.cursor()
            await cur.execute('create table if not exists Accounts("Num" integer primary key autoincrement,"user_name" text, "user_id" integer not null, "balance" integer,"wallet" integer)')
            await cur.execute(f'select balance from Accounts where user_id="{USER_ID}"')
            result_userID = await cur.fetchone()
        if result_userID is None:
            await ctx.send(f'{ctx.message.author.mention} please create an account using the register command')
            return
        if result_userID:      
            wallet_balance = int(result_userID[0])
        if amount.isalpha():
            if amount == 'max' or amount == 'all' or amount == 'half':
                if amount == 'half':
                    ant = wallet_balance / 2
                else:
                    if wallet_balance == 0:
                        return await ctx.send('You do not have enough money to do that')
                    ant = wallet_balance
            else:
                await ctx.send('Please give me a valid amount')
                return
        if amount.isdigit():
            ant = amount
        if int(ant) > int(wallet_balance) or int(wallet_balance) == 0:
            await ctx.send('You do not have enough money to do that')
        if int(ant) <= int(wallet_balance):
            async with aiosqlite.connect("data/BankAccounts.db") as db:   
                msg = await ctx.send(embed=discord.Embed(description=':game_die: Rolling...', color=discord.Color.dark_theme()))
                mul = multi / 100
                amt = int(ant) * mul
                rounded = round(amt)
                stringy = str(rounded)
                if winner:
                    cur = await db.cursor()
                    await cur.execute(f'UPDATE Accounts SET balance = balance + {int(amt)} where user_id={USER_ID}')
                    await db.commit()  
                    await cur.execute(f'select balance from Accounts where user_id="{USER_ID}"')
                    walID = await cur.fetchone()
                    message = f'**You won {self.osi.emote} {stringy}!**\nYou now have {self.osi.emote} **{int(walID[0])}**'
                    foot = f'Multiplier: {multi}%'
                if draw:
                    message = f'**You tied!**\nYour balance is still {self.osi.emote} **{wallet_balance}**'
                    foot = 'Multipler: 0%'
                if lose:                
                    cur = await db.cursor()
                    await cur.execute(f'UPDATE Accounts SET balance = balance - {int(ant)} where user_id={USER_ID}')
                    await db.commit()  
                    await cur.execute(f'select balance from Accounts where user_id="{USER_ID}"')
                    walID = await cur.fetchone()
                    message = f'**You lost {self.osi.emote} {ant}!**\nYou now have {self.osi.emote} **{int(walID[0])}**'
                    foot = f'Multiplier: 0%'
                await asyncio.sleep(1.5)
                await msg.edit(embed=discord.Embed(description=f':game_die: Osi: `{sum(brolls)}`\n:game_die: {ctx.author.name}: `{sum(urolls)}`\n\n{message}', color=discord.Color.dark_theme()).set_footer(text=foot))  


    @commands.command(hidden=True)
    @commands.is_owner()
    async def freemoney(self, ctx, amt:int, user:discord.Member=None):
        user = user or ctx.author
        USER_ID = user.id
        async with aiosqlite.connect("data/BankAccounts.db") as db:
            cur = await db.cursor()
            await cur.execute('create table if not exists Accounts("Num" integer primary key autoincrement,"user_name" text, "user_id" integer not null, "balance" integer,"wallet" integer)')
            await cur.execute(f'select balance from Accounts where user_id="{USER_ID}"')
            result_userID = await cur.fetchone()
        if result_userID is None:
            await ctx.send('not registered xd')
        else:
            async with aiosqlite.connect("data/BankAccounts.db") as db:
                cur = await db.cursor()
                await cur.execute(f'UPDATE Accounts SET balance = balance + {amt} where user_id={USER_ID}')
                await db.commit()  
                await ctx.send(f'Gave {user} {self.osi.emote} {amt}')

    @commands.command(hidden=True)
    @commands.is_owner()
    async def loserxd(self, ctx, amt:int, user:discord.Member=None):
        user = user or ctx.author
        USER_ID = user.id
        async with aiosqlite.connect("data/BankAccounts.db") as db:
            cur = await db.cursor()
            await cur.execute('create table if not exists Accounts("Num" integer primary key autoincrement,"user_name" text, "user_id" integer not null, "balance" integer,"wallet" integer)')
            await cur.execute(f'select balance from Accounts where user_id="{USER_ID}"')
            result_userID = await cur.fetchone()
        if result_userID is None:
            await ctx.send('not registered xd')
        else:
            async with aiosqlite.connect("data/BankAccounts.db") as db:
                cur = await db.cursor()
                await cur.execute(f'UPDATE Accounts SET balance = balance - {amt} where user_id={USER_ID}')
                await db.commit()  
                await ctx.send(f'Took away {self.osi.emote} {amt} from {user}')

    @commands.command()
    @commands.is_owner()
    async def remove(self, ctx, user:discord.Member):
        USER_ID = user.id
        if ctx.author.id == 583745403598405632:
            async with aiosqlite.connect("data/BankAccounts.db") as db:
                cur = await db.cursor()
                await cur.execute('create table if not exists Accounts("Num" integer primary key autoincrement,"user_name" text, "user_id" integer not null, "balance" integer,"wallet" integer)')
                await cur.execute(f'select balance from Accounts where user_id="{USER_ID}"')
                await db.commit()
                result_userID = await cur.fetchone()
            if result_userID is None:
                await ctx.send('not registered xd')
            else:
                async with aiosqlite.connect("data/BankAccounts.db") as db:
                    cur = await db.cursor()
                    await cur.execute(f'delete from Accounts where user_id="{USER_ID}"')
                    await db.commit()
                    await ctx.send(f'Removed {user} from the database')
        else:
            await ctx.send('no u')

    @commands.command()
    async def spellout(self, ctx, *, msg:str):
        await ctx.send(" ".join(list(msg.upper())))


def setup(osi):
    osi.add_cog(Fun(osi))