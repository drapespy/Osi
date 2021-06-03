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

_extensions = [
    'cogs.eco',
    'cogs.error_handler',
    'cogs.fun',
    'cogs.info',
    'cogs.misc',
    'cogs.shop',
    'cogs.slash'
]

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

@osi.command()
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

if __name__ == '__main__':
    for ext in _extensions:
        osi.load_extension(ext)


# token and others 
keep_alive()
osi.run(os.environ['TOKEN'])