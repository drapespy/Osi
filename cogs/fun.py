import discord
from discord.ext import commands
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
    async def roll(self, ctx, amount):
        """
        Take a shot at the gamble command. 
        Totally not rigged:tm:
        If ya wanna view the source visit [here](https://github.com/drapespy/Osi)
        """
        USER_ID = ctx.message.author.id
        async with aiosqlite.connect("data/BankAccounts.db") as db:
            cur = await db.cursor()
            await cur.execute('create table if not exists Accounts("Num" integer primary key autoincrement,"user_name" text, "user_id" integer not null, "balance" integer,"wallet" integer)')
            await cur.execute(f'select balance from Accounts where user_id="{USER_ID}"')
            result_userID = await cur.fetchone()
        if result_userID is None:
            await ctx.send(f'{ctx.message.author.mention} please create an account using the register command')
        if result_userID:      
            wallet_balance = int(result_userID[0])
        if amount.isalpha():
            if amount == 'max' or amount == 'all':
                ant = wallet_balance
            else:
                await ctx.send('Please give me a valid amount')
                return
        if amount.isdigit():
            ant = amount
        if int(ant) > int(wallet_balance):
            await ctx.send('You do not have enough money to do that')
        if int(ant) <= int(wallet_balance):
            async with aiosqlite.connect("data/BankAccounts.db") as db:   
                msg = await ctx.send(embed=discord.Embed(description=':game_die: Rolling...', color=discord.Color.dark_theme()))
                user = random.randint(2, 12)
                bot = random.randint(2, 12)
                multi = random.randint(60, 120)
                mul = multi / 100
                amt = int(ant) * mul
                rounded = round(amt)
                stringy = str(rounded)
                if bot > user:                
                    cur = await db.cursor()
                    message = f'**You lost {self.osi.emote} {ant}!**'
                    foot = f'Multiplier: 0%'
                    await cur.execute(f'UPDATE Accounts SET balance = balance - {int(ant)} where user_id={USER_ID}')
                    await db.commit()  
                if bot < user:
                    cur = await db.cursor()
                    message = f'**You won {self.osi.emote} {stringy}!**'
                    foot = f'Multiplier: {multi}%'
                    await cur.execute(f'UPDATE Accounts SET balance = balance + {int(amt)} where user_id={USER_ID}')
                    await db.commit()  
                if bot == user:
                    message = '**You tied!**'
                    foot = 'Multipler: 0%'
                await asyncio.sleep(1.5)
                await msg.edit(embed=discord.Embed(description=f':game_die: Osi: `{bot}`\n:game_die: {ctx.author.name}: `{user}`\n\n{message}', color=discord.Color.dark_theme()).set_footer(text=foot))  


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

    @commands.command()
    async def table(self, ctx):
        async with aiosqlite.connect('data/BankAccounts.db') as db:
            cur = await db.cursor()
            await cur.execute('SELECT * FROM Accounts')
            result = await cur.fetchall()
            for row in result:
                em =  discord.Embed(
                    description=row,
                    color=discord.Color.random()
                )
                await ctx.send(embed=em)
                # print(row)
                # print("\n")
            # await ctx.send('Printed result')


def setup(osi):
    osi.add_cog(Fun(osi))