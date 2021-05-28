import discord
from discord.ext import commands

class Info(commands.Cog):
    """
    Information about the bot, server etc.
    """
    def __init__(self, osi):
        self.osi = osi

    # info command
    @commands.command()
    async def info(self, ctx):

        server_count = len(self.osi.guilds)
        total_members = len(set(self.osi.get_all_members()))

        em = discord.Embed(
            color=discord.Color.purple()
        )
        em.add_field(name='__Bot Info__',value='<:Developer:808407479687053403> Developers: <@583745403598405632>, <@710247495334232164>', inline=False)
        em.add_field(name='__Bot Stats__',value=f'<:servercount:822526317663748106> Servers: `{server_count}`\n<:memberlist:811747305543434260> Members: `{total_members}`', inline=False)
        await ctx.send(embed=em)

def setup(osi):
    osi.add_cog(Info(osi))