import discord
from discord.ext import commands
import time

class Misc(commands.Cog):
    """
    Miscellaneous commands
    """
    def __init__(self, osi):
        self.osi = osi

    # ping command
    @commands.command(description='Shows the bot latency')
    async def ping(self,ctx):

        start = time.perf_counter()
        pinging = await ctx.send('Pinging...')
        end = time.perf_counter()
        duration = round((end - start) * 1000)

        em=discord.Embed(
            title = '🏓  Pong!',
            description = f'Bot latency: {round(self.osi.latency*1000)} ms\nType latency: {duration} ms',
            color = discord.Color.dark_theme()
        )
        await pinging.edit(content=None,embed=em)

    # invite command
    @commands.command()
    async def invite(self, ctx):
        em=discord.Embed(
            title='Osi Links',
            description='Invite Osi: [Invite me](https://dsc.gg/osi)\n━━━\nGet help: [Join now](https://discord.gg/gWCF89bggc)',
            color=discord.Color.purple()
            )
        em.set_thumbnail(url=self.osi.user.avatar_url)
        em.set_footer(text= 'Invite me!')
        await ctx.send(embed=em)


def setup(osi):
    osi.add_cog(Misc(osi))