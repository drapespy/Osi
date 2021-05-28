import discord
from discord.ext import commands

class Shop(commands.Cog):
    """ Shop """
    def __init__(self, osi):
        self.osi = osi

    # shop command
    @commands.command()
    async def shop(self, ctx):
        em = discord.Embed(
            title='Osi Shop',
            description=f'<:fun:815015395030859796> Pepe: {self.osi.emote} 10,000\n\n<:ytbot:818586162540707860> YouTube: {self.osi.emote} 35,000\n\n<:moderation:847248846526087239> Shield: {self.osi.emote} 50,000\n\n<:dsc_trash:835184769691156520> Trash: {self.osi.emote} 25,000\n\n⏰ Alarm clock: {self.osi.emote} 100\n\n🍕 Pizza: {self.osi.emote} 1,000',
            color=discord.Color.random()
        )
        await ctx.send(embed=em)

def setup(osi):
    osi.add_cog(Shop(osi))