import html
from pyrogram import filters, Client
from spam import log, HELP_COMMANDS, config


def __list_all_modules():
    from os.path import dirname, basename, isfile
    import glob
    # This generates a list of modules in this folder for the * in __main__ to work.
    mod_paths = glob.glob(dirname(__file__) + "/*.py")
    all_modules = [basename(f)[:-3] for f in mod_paths if isfile(f)
                   and f.endswith(".py")
                   and not f.endswith('__init__.py')]
    return all_modules

@Client.on_message(filters.me & filters.command(["help"], prefixes=config['config']['prefixes']))
async def help(client, message):
    command = message.command
    command.pop(0)
    if command:
        if command[0].lower() in HELP_COMMANDS:
            await message.edit(HELP_COMMANDS[command[0].lower()].__HELP__)
        else:
            await message.edit(f"<code>{html.escape(command[0])}</code> is not a valid command")
    else:
        prefix = config['config']['prefixes'][0]
        reply = "Available Commands:\n\n"
        for key, value in HELP_COMMANDS.items():
            reply += f"- <code>{prefix}{key}</code>\n"
        reply += f"\nYou can use <code>{prefix}help &lt;command&gt;<code>"
        await message.edit(reply)

ALL_MODULES = sorted(__list_all_modules())
__all__ = ALL_MODULES + ["ALL_MODULES"]