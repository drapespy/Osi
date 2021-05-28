import discord
from discord.ext import commands
import aiosqlite
import random
import asyncio
import typing

START_BALANCE = 2000
START_WALLET = 0

class Economy(commands.Cog):
    """ Economy Commands """
    def __init__(self, osi):
        self.osi = osi

    @commands.command(description='Register into the database')
    async def register(self,ctx):
        USER_ID = ctx.message.author.id
        USER_NAME = str(ctx.message.author)
        async with aiosqlite.connect("data/BankAccounts.db") as db:
            cur = await db.cursor()
            await cur.execute('create table if not exists Accounts("Num" integer primary key autoincrement,"user_name" text, "user_id" integer not null, "balance" integer,"wallet" integer)')
            await cur.execute(f'select user_id from Accounts where user_id="{USER_ID}"')
            result_userID = await cur.fetchone()

        if result_userID is None:
            async with aiosqlite.connect("data/BankAccounts.db") as db:
                cur = await db.cursor()
                await cur.execute('insert into Accounts(user_name, user_id, balance, wallet) values(?,?,?,?)', (USER_NAME, USER_ID, START_BALANCE, START_WALLET))
                await db.commit()
            await ctx.send('Welcome to **Osi Bot**! We gave you 2000 credits to start.\nCheck your balance using `osi bal`')
        else:
            await ctx.send('You are already registered')

    @commands.command(aliases=['bal'], description='Check your balance')
    async def balance(self,ctx,*,user:discord.Member=None):
        if not user:
            user = ctx.author
        USER_ID = user.id
        async with aiosqlite.connect("data/BankAccounts.db") as db:
            cur = await db.cursor()
            await cur.execute('create table if not exists Accounts("Num" integer primary key autoincrement,"user_name" text, "user_id" integer not null, "balance" integer,"wallet" integer)')
            await cur.execute(f'select user_id from Accounts where user_id="{USER_ID}"')
            result_userID = await cur.fetchone()

        if result_userID is None:
            if user is None:
                await ctx.send(f'{user.mention} please create an account using the register command')
            else:
                await ctx.send(f"{user} hasn't registered yet")
        else:   
            async with aiosqlite.connect("data/BankAccounts.db") as db:
                cur = await db.cursor()
                await cur.execute(f'select balance from Accounts where user_id="{USER_ID}"')
                #SQL.execute(f'select wallet from Accounts where user_id="{USER_ID}"')
                result_userbal = await cur.fetchone()
                await cur.execute(f'select wallet from Accounts where user_id="{USER_ID}"')
                result_userwallet = await cur.fetchone()
            emb = discord.Embed(title=f'__{user.name}\'s Balance__')
            emb.add_field(name='Wallet: ', value=f'{self.osi.emote} {result_userbal[0]}', inline=False)
            emb.add_field(name='Bank: ', value=f'{self.osi.emote} {result_userwallet[0]}', inline=False)
            await ctx.send(embed=emb)

    @commands.command(aliases=['dep'], description='Deposit credits into your bank')
    async def deposit(self,ctx, amount:typing.Union[int, str]):
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
        if isinstance(amount, str):
            if amount == 'max' or amount == 'all':
                amt = wallet_balance
            else:
                await ctx.send('Please give me a valid amount')
                return
        if isinstance(amount, int):
            amt = amount
        if int(amt) > int(wallet_balance):
            await ctx.send('You do not have enough money to do that')
        if int(amt) <= int(wallet_balance):
            async with aiosqlite.connect("data/BankAccounts.db") as db:     
                cur = await db.cursor()
                await cur.execute(f'UPDATE Accounts SET wallet = wallet + {int(amt)} where user_id={USER_ID}')
                await db.commit()
                await cur.execute(f'UPDATE Accounts SET balance = balance - {int(amt)} where user_id={USER_ID}')
                await db.commit()
            await ctx.send(f'Successfully transfered {self.osi.emote} {amt} to your bank')    
        else:
            await ctx.send(f"{ctx.message.author.mention} Please give a valid amount")    

    @commands.command(aliases=['with'], description='Withdraw credits from bank.')
    async def withdraw(self,ctx, amount:typing.Union[int, str]):
        USER_ID = ctx.message.author.id
        async with aiosqlite.connect("data/BankAccounts.db") as db:
            cur = await db.cursor()
            await cur.execute('create table if not exists Accounts("Num" integer primary key autoincrement,"user_name" text, "user_id" integer not null, "balance" integer,"wallet" integer)')
            await cur.execute(f'select wallet from Accounts where user_id="{USER_ID}"')
            result_userID = await cur.fetchone()
        if result_userID is None:
            await ctx.send(f'{ctx.message.author.mention} please create an account using the register command')
        else:
            bank_balance = int(result_userID[0])

        if isinstance(amount, str):
            if amount == 'max' or amount == 'all':
                amt = bank_balance
            else:
                await ctx.send('Please give me a valid amount')
                return
        if isinstance(amount, int):
            amt = amount
        if int(amt) > int(bank_balance):
            await ctx.send('You do not have enough money to do that')
        elif int(amt) <= int(bank_balance):
            async with aiosqlite.connect("data/BankAccounts.db") as db:
                cur = await db.cursor()
                await cur.execute(f'UPDATE Accounts SET wallet = wallet - {int(amt)} where user_id={USER_ID}')
                await db.commit()
                await cur.execute(f'UPDATE Accounts SET balance = balance + {int(amt)} where user_id={USER_ID}')
                await db.commit() 
            await ctx.send(f'You have successfully withdrawn {self.osi.emote} {int(amt)}')
        else:
            await ctx.send(f"{ctx.message.author.mention} Please give me a valid amount")

    @commands.command(description='Beg for some credits.')
    @commands.cooldown(1, 20, commands.BucketType.user)
    async def beg(self,ctx):
        USER_ID = ctx.message.author.id
        async with aiosqlite.connect("data/BankAccounts.db") as db:
            cur = await db.cursor()
            await cur.execute('create table if not exists Accounts("Num" integer primary key autoincrement,"user_name" text, "user_id" integer not null, "balance" integer,"wallet" integer)')
            await cur.execute(f'select user_id from Accounts where user_id="{USER_ID}"')
            result_userID =await cur.fetchone()

        if result_userID is None:
            await ctx.send(f'{ctx.message.author.mention} please create an account using the register command')
        else:
            #db.commit()
            random_amount = random.randint(0,100)
            random_resp = random.choice([f'Heres {self.osi.emote} {random_amount}', f'Take {self.osi.emote} {random_amount} and leave me alone', f'Ugh, fine, I\'ll give you {self.osi.emote} {random_amount}'])
            async with aiosqlite.connect("data/BankAccounts.db") as db:
                cur = await db.cursor()
                await cur.execute(f'UPDATE Accounts SET balance = balance + {random_amount} where user_id={USER_ID}')
                await db.commit()
            await ctx.send(f'**{random.choice(self.osi.users).name}**: {random_resp}')

    @commands.command()
    @commands.cooldown(1, 20, commands.BucketType.user)
    async def search(self,ctx):
        USER_ID = ctx.message.author.id
        async with aiosqlite.connect("data/BankAccounts.db") as db:
            cur = await db.cursor()
            await cur.execute(f'select balance from Accounts where user_id="{USER_ID}"')
            result_userID = await cur.fetchone()
        if result_userID is None:
            await ctx.send('Please register using the `register` command')    
        else:
            options = ['Church', 'Store', 'Toilet', 'TV', 'Lawn', 'Couch', 'Carpet', 'Sewer', '344 Cleveland St. Rapid City, SD']
            option1 = random.choice(options)
            options.remove(option1)
            option2 = random.choice(options)
            options.remove(option2)
            option3 = random.choice(options)

            await ctx.reply(f'**Available search options**\nRespind with where you want to search!\n\n`{option1}`, `{option2}`, `{option3}`')

            def msg_check(m):
                return m.author == ctx.message.author and m.channel == ctx.channel

            try:
                response = await self.osi.wait_for('message', check=msg_check, timeout=20.0)
                if str(response) == option1.lower() or option2.lower() or option3.lower():
                    random_money = random.randint(10,300)
                    async with aiosqlite.connect("data/BankAccounts.db") as db:
                        cur = await db.cursor()
                        await cur.execute(f'UPDATE Accounts SET balance = balance + {random_money} where user_id={USER_ID}')
                        await db.commit()
                    await ctx.send(f'You searched the {response.content} and found {self.osi.emote} {random_money}!')
                else:
                    await ctx.send('Bruh')    
            except asyncio.TimeoutError:
                await ctx.send(f'You ran out of time so you didn\'t earn any {self.osi.emote}')

def setup(osi):
    osi.add_cog(Economy(osi))