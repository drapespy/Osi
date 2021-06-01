import discord
from discord.ext import commands, tasks
from discord_slash import SlashCommand
import os
from keep_alive import keep_alive
from better_help import Help

helpcommand = Help(sort_commands=True, code_block=False, colour=discord.Colour.purple(), timeout_remove_controls=True)
osi = commands.Bot(command_prefix=commands.when_mentioned_or('osi ', 'Osi ', 'OSi ', 'OSI ', 'OsI ', "oSI ", 'oSi ', 'osI ', 'o!', 'O!'), intents=discord.Intents.all(), case_insensitive=True, help_command=helpcommand, description='An economy bot made in discord.py')
osi.emote = '<a:osi:832657362912542790>' 
osi.load_extension("jishaku")
osi.emote = '<a:osi:832657362912542790>'
os.environ["JISHAKU_HIDE"] = "True"
os.environ["JISHAKU_NO_UNDERSCORE"] = "True"
os.environ["JISHAKU_NO_DM_TRACEBACK"] = "True"
slash = SlashCommand(osi, override_type = True, sync_commands = True)

@osi.event
async def on_ready():
    print('Osi is ready')
    cp.start()


# CP 😳
@tasks.loop(minutes=5)
async def cp():
    await osi.change_presence(activity=discord.Game(name='osi help'))


@osi.command(hidden=True, aliases=['l'])
@commands.is_owner()
async def load(ctx, extension):
    try:
        osi.unload_extension(extension)
        await ctx.send(f':inbox_tray: `{extension}`')
    except Exception as e:
        await ctx.send(f'```\n{e}\n```')

@osi.command(hidden=True, aliases=['ul'])
@commands.is_owner()
async def unload(ctx, extension):
    try:
        osi.unload_extension(extension)
        await ctx.send(f':outbox_tray:`{extension}`')
    except Exception as e:
        await ctx.send(f'```\n{e}\n```')

@osi.command(hidden=True, aliases=['rl'])
@commands.is_owner()
async def reload(ctx, extension):
    try:
        osi.unload_extension(extension)
        osi.load_extension(extension)
        await ctx.send(f':repeat: `{extension}`')
    except Exception as e:
        await ctx.send(f'```\n{e}\n```')

for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        osi.load_extension(f"cogs.{filename[:-3]}")


# token and others 
keep_alive()
osi.run(os.environ['TOKEN'])