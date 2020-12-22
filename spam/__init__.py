import logging
import os
import sys
import time
import yaml
import logging
from pathlib import Path

from pyrogram import Client, errors

StartTime = time.time()
logging.basicConfig(level=logging.INFO)
log = logging.getLogger()
clients = []

# if version < 3.6, stop bot.
if sys.version_info[0] < 3 or sys.version_info[1] < 6:
    logging.error("You MUST have a python version of at least 3.6! Multiple features depend on this. Bot quitting...")
    quit(1)

try:
    with open('config.yaml') as c:
        config = yaml.safe_load(c)
except FileNotFoundError:
    logging.error("You must create a config.yaml file, edit the example yaml file and rename it to config.yaml")
    quit(1)

# Check if the sessions directory exists and create it if it does not.
with Path('sessions') as p:
    if not p.exists():
        p.mkdir()
    elif not p.is_dir():
        logging.error(f"{p.resolve()} must be a directory.")
        quit(1)
    
for sessh in config['config']['sessions']:
    client = Client(sessh, api_id=config['telegram']['api_id'], api_hash=config['telegram']['api_hash'], plugins={'root': os.path.join(__package__, 'modules')}, workdir='sessions')
    clients.append(client)
