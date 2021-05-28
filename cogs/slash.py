import discord
from discord.ext import commands
from discord_slash import cog_ext, SlashContext
import time

class Slash(commands.Cog):
    """ Slash Commands """
    def __init__(self,osi):
        self.osi = osi

    # ping command
    @cog_ext.cog_slash(name='ping',description='Shows the latency of the bot')
    async def ping(self,ctx: SlashContext):
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
    @cog_ext.cog_slash(name='invite', description='Gives bot invite')
    async def invite(self, ctx: SlashContext):
        em=discord.Embed(
            title='Osi Links',
            description='Invite Osi: [Invite me](https://dsc.gg/osi)\n━━━\nGet help: [Join now](https://discord.gg/gWCF89bggc)',
            color=discord.Color.purple()
            )
        em.set_thumbnail(url=self.osi.user.avatar_url)
        em.set_footer(text= 'Invite me!')
        await ctx.send(embed=em, hidden=True)


def setup(client):
    client.add_cog(Slash(client))