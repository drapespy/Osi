import discord
from discord.ext import commands
import math

class ErrorHandler(commands.Cog):
    def __init__(self,osi):
        self.osi = osi

    @commands.Cog.listener()
    async def on_message(self, msg):
        if msg.author == self.osi.user:
            return
        if msg.content in {f'<@{self.osi.user.id}>', f'<@!{self.osi.user.id}>'}:
            await msg.channel.send('My prefix is `osi` and `o!`')

    @commands.Cog.listener()
    async def on_command_error(self,ctx,error):
        if isinstance(error, commands.CommandNotFound):
            return
        if isinstance(error, commands.CommandOnCooldown):
            embed=discord.Embed(title='Slow down...', description=f'Please wait **{math.ceil(error.retry_after)} seconds** before using that command again!\n\n**__Cooldown__**\nNormal: `{error.cooldown.rate}` use(s) every `{error.cooldown.per}` seconds\nPremium: Not available', color=discord.Color.dark_theme())
            await ctx.send(embed=embed)

        else:
            original_error = getattr(error, 'original', error)
            await ctx.send(f"{original_error}")


def setup(osi):
    osi.add_cog(ErrorHandler(osi))