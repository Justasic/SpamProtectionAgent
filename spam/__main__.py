import asyncio
import importlib
import sys
import time
import traceback
import yaml
from pyrogram import idle
from spam import clients, log

from spam.modules import ALL_MODULES

BOT_RUNTIME = 0
HELP_COMMANDS = {}

loop = asyncio.get_event_loop()

async def get_runtime():
    return BOT_RUNTIME

async def reload_userbot():
    try:
        with open('config.yaml') as c:
            config = yaml.safe_load(c)
    except FileNotFoundError:
        log.error("You must create a config.yaml file, edit the example yaml file and rename it to config.yaml")

    await reinitial()

    for modul in ALL_MODULES:
        imported_module = importlib.import_module("spam.modules." + modul)
        importlib.reload(imported_module)

async def reinitial():
    await asyncio.gather(*(app.start() for app in clients))

async def start_bot():
    # sys.excepthook = except_hook
    print("----- Checking user and bot... -----")
    await reinitial()
    print("----------- Check done! ------------")
    for modul in ALL_MODULES:
        imported_module = importlib.import_module("spam.modules." + modul)
        if hasattr(imported_module, "__MODULE__") and imported_module.__MODULE__:
            imported_module.__MODULE__ = imported_module.__MODULE__
        if hasattr(imported_module, "__MODULE__") and imported_module.__MODULE__:
            if not imported_module.__MODULE__.lower() in HELP_COMMANDS:
                HELP_COMMANDS[imported_module.__MODULE__.lower()] = imported_module
            else:
                raise Exception("Can't have two modules with the same name! Please change one")
        if hasattr(imported_module, "__HELP__") and imported_module.__HELP__:
            HELP_COMMANDS[imported_module.__MODULE__.lower()] = imported_module
    print("-----------------------")
    print("SpamProtection modules: " + str(ALL_MODULES))
    print("-----------------------")
    print("Bot run successfully!")
    await idle()
    await asyncio.gather(*(app.stop() for app in clients))

if __name__ == '__main__':
    BOT_RUNTIME = int(time.time())
    loop.run_until_complete(start_bot())