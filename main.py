import discord 
from discord.ext import commands, tasks
from discord_slash import SlashCommand
import os
from keep_alive import keep_alive
from better_help import Help
from jishaku.paginators import WrappedPaginator
import itertools
import traceback
from util.jsk import ExtensionConverter

desc = """
An economy bot made in discord.py
──────────────────────────────────────────
─██████████████─██████████████─██████████─
─██░░░░░░░░░░██─██░░░░░░░░░░██─██░░░░░░██─
─██░░██████░░██─██░░██████████─████░░████─
─██░░██──██░░██─██░░██───────────██░░██───
─██░░██──██░░██─██░░██████████───██░░██───
─██░░██──██░░██─██░░░░░░░░░░██───██░░██───
─██░░██──██░░██─██████████░░██───██░░██───
─██░░██──██░░██─────────██░░██───██░░██───
─██░░██████░░██─██████████░░██─████░░████─
─██░░░░░░░░░░██─██░░░░░░░░░░██─██░░░░░░██─
─██████████████─██████████████─██████████─
──────────────────────────────────────────
Now with spaghetti code:tm:
"""

helpcommand = Help(sort_commands=True, code_block=False, colour=discord.Colour.purple(), timeout_remove_controls=True)
osi = commands.Bot(command_prefix=commands.when_mentioned_or('osi ', 'Osi ', 'OSi ', 'OSI ', 'OsI ', "oSI ", 'oSi ', 'osI ', 'o!', 'O!'), intents=discord.Intents.all(), case_insensitive=True, help_command=helpcommand, description=desc)
osi.emote = '<a:osi:832657362912542790>' 
os.environ["JISHAKU_HIDE"] = "True"
os.environ["JISHAKU_NO_UNDERSCORE"] = "True"
os.environ["JISHAKU_NO_DM_TRACEBACK"] = "True"
slash = SlashCommand(osi, override_type = True, sync_commands = True)

EXTENSIONS = [
    'jishaku',
    'cogs.eco',
    'cogs.error_handler',
    'cogs.fun',
    'cogs.info',
    'cogs.misc',
    'cogs.shop',
    'cogs.slash'
    ]

@osi.event
async def on_ready():
    for ext in EXTENSIONS:
        try:
            osi.load_extension(ext)
            print(f"The {ext.replace('cogs.', '').replace('_', ' ').title()} cog has been loaded.")
        except Exception as e: 
            print(f"The {ext.replace('cogs.', '').replace('_', ' ').title()} cog has failed to load\n Error: {e}")
    print('Osi is now ready.')
    cp.start()


# CP 😳
@tasks.loop(minutes=5)
async def cp():
    await osi.change_presence(activity=discord.Game(name='osi help'))

@osi.command(hidden=True, aliases=['reload'])
@commands.is_owner()
async def load(ctx, *extensions: ExtensionConverter):
    paginator = WrappedPaginator(prefix='', suffix='')

    # 'jsk reload' on its own just reloads jishaku
    if ctx.invoked_with == 'reload' and not extensions:
        extensions = [['jishaku']]

    for extension in itertools.chain(*extensions):
        method, icon = (
            (osi.reload_extension, "\N{CLOCKWISE RIGHTWARDS AND LEFTWARDS OPEN CIRCLE ARROWS}")
            if extension in osi.extensions else
            (osi.load_extension, "\N{INBOX TRAY}")
        )

        try:
            method(extension)
        except Exception as exc:  # pylint: disable=broad-except
            traceback_data = ''.join(traceback.format_exception(type(exc), exc, exc.__traceback__, 1))

            paginator.add_line(
                f"{icon}\N{WARNING SIGN} `{extension}`\n```py\n{traceback_data}\n```",
                empty=True
            )
        else:
            paginator.add_line(f"{icon} `{extension}`", empty=True)

    for page in paginator.pages:
        await ctx.send(page)

@osi.command(hidden=True)
@commands.is_owner()
async def unload(ctx, *extensions: ExtensionConverter):

    paginator = WrappedPaginator(prefix='', suffix='')
    icon = "\N{OUTBOX TRAY}"

    for extension in itertools.chain(*extensions):
        try:
            osi.unload_extension(extension)
        except Exception as exc:  # pylint: disable=broad-except
            traceback_data = "".join(traceback.format_exception(type(exc), exc, exc.__traceback__, 1))

            paginator.add_line(
                f"{icon}\N{WARNING SIGN} `{extension}`\n```py\n{traceback_data}\n```",
                empty=True
            )
        else:
            paginator.add_line(f"{icon} `{extension}`", empty=True)

    for page in paginator.pages:
        await ctx.send(page)


# Starting the bot
if __name__ == '__main__':
    keep_alive()
    osi.run(os.environ['TOKEN'])

