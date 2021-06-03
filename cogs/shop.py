import discord
from discord.ext import commands

items = [
    'pepe', 
    'youtube',
    'shield', 
    'trash',
    'clock',
    'pizza',
    'spinner'
        ]

class Shop(commands.Cog):
    """ Shop """
    def __init__(self, osi):
        self.osi = osi

    # ==== SHOP COMMAND =====
    @commands.command()
    async def shop(self, ctx, item=None):

        if item is None:
            em = discord.Embed(
                title='Osi Shop',
                description=f'<:fun:815015395030859796> Pepe: {self.osi.emote} 10,000\n\n<:ytbot:818586162540707860> YouTube: {self.osi.emote} 35,000\n\n<:moderation:847248846526087239> Shield: {self.osi.emote} 50,000\n\n<:dsc_trash:835184769691156520> Trash: {self.osi.emote} 25,000\n\n<:spinner:848866446766899271> Spinner: {self.osi.emote} 55,000\n\n🍕 Pizza: {self.osi.emote} 19,000',
                color=discord.Color.random()
            )
            await ctx.send(embed=em)
        
        elif 'pepe' in item.lower():
            em = discord.Embed(
                title='Pepe',
                description=f'Price: {self.osi.emote} 10,000',
                color=discord.Color.random()
            )
            em.set_thumbnail(url='https://cdn.discordapp.com/emojis/815015395030859796.png?v=1')
            await ctx.send(embed=em)
        
        elif 'youtube' in item.lower():
            em = discord.Embed(
                title='YouTube',
                description=f'Price: {self.osi.emote} 35,000',
                color=discord.Color.random()
            )
            em.set_thumbnail(url='https://cdn.discordapp.com/emojis/818586162540707860.png?v=1')
            await ctx.send(embed=em)

        elif 'shield' in item.lower():
            em = discord.Embed(
                title='Shield',
                description=f'Price: {self.osi.emote} 50,000',
                color=discord.Color.random()
            )
            em.set_thumbnail(url='https://cdn.discordapp.com/emojis/847248846526087239.png?v=1')
            await ctx.send(embed=em)

        elif 'trash' in item.lower():
            em = discord.Embed(
                title='Trash',
                description=f'Price: {self.osi.emote} 25,000',
                color=discord.Color.random()
            )
            em.set_thumbnail(url='https://cdn.discordapp.com/emojis/835184769691156520.png?v=1')
            await ctx.send(embed=em)
        
        elif 'spinner' in item.lower():
            em = discord.Embed(
                title='Spinner',
                description=f'Price: {self.osi.emote} 55,000',
                color=discord.Color.random()
            )
            em.set_thumbnail(url='https://cdn.discordapp.com/emojis/804837332439400488.png?v=1')
            await ctx.send(embed=em)

        elif 'pizza' in item.lower():
            em = discord.Embed(
                title='Pizza',
                description=f'Price: {self.osi.emote} 19,000',
                color=discord.Color.random()
            )
            em.set_thumbnail(url='https://media.discordapp.net/attachments/693517202879414312/788070266579189790/pizza-export2.png')
            await ctx.send(embed=em)
        
        elif item not in items:
            await ctx.send('That item is not in the shop.')


    # ====== BUY COMMAND =======
    @commands.command()
    async def buy(self, ctx, item=None):
        
        if item is None:
            await ctx.send('Item not provided.')
        
        elif item not in items:
            await ctx.send('Item cannot be bought/not found')

def setup(osi):
    osi.add_cog(Shop(osi))