import html
from datetime import datetime
from asyncio import sleep

from pyrogram import filters, Client
from pyrogram.types import User, Chat
from pyrogram.raw import functions
from pyrogram.errors import PeerIdInvalid

from spam import config, utilities, session, spb
from spam.utilities import get_entity

__MODULE__ = "Whois"
__HELP__ = """-> `whois` @username
-> `whois` (reply to a text)
To find information about a person.
"""

async def _get_flags(spbinfo):
    # Check for statuses.
    text = ""
    if spbinfo:

        entity = "user"
        if spbinfo.entity_type == "supergroup":
            entity = "group"
        if spbinfo.entity_type == "supergroup":
            entity = "channel"

        needline = False
        if spbinfo.attributes.intellivoid_accounts_verified:
            text += "\N{WHITE HEAVY CHECK MARK} This user's Telegram account is verified by Intellivoid Accounts\n"
            needline = True
        if spbinfo.attributes.is_official:
            text += f"\N{WHITE HEAVY CHECK MARK} This {entity} is verified by Intellivoid Technologies\n"
            needline = True
        if spbinfo.attributes.is_potential_spammer:
            text += f"\N{warning sign} This {entity} may be an active spammer!\n"
            needline = True
        if spbinfo.attributes.is_blacklisted:
            text += f"\N{warning sign} This {entity} is blacklisted!\n"
            needline = True
        if spbinfo.attributes.is_agent:
            text += "\N{police officer} This user is an agent who actively reports spam automatic\n"
            needline = True
        if spbinfo.attributes.is_operator:
            text += "\N{police officer} This user is an operator who can blacklist users\n"
            needline = True

        if needline:
            text += "\n"
    return text

async def _get_info(spbinfo):
    text = ""
    if spbinfo:
        text += f"<b>Trust Prediction:</b> <code>{spbinfo.spam_prediction.ham_prediction}/{spbinfo.spam_prediction.spam_prediction}</code>\n"
        text += f"<b>Language Prediction:</b> <code>{spbinfo.language_prediction.language}</code> (<code>{spbinfo.language_prediction.probability}</code>)\n"
        if spbinfo.attributes.is_whitelisted:
            text += f"<b>Whitelisted:</b> <code>True</code>\n"
        if spbinfo.attributes.is_operator:
            text += f"<b>Operator:</b> <code>True</code>\n"
        if spbinfo.attributes.is_agent:
            text += f"<b>Spam Detection Agent:</b> <code>True</code>\n"
        if spbinfo.attributes.is_potential_spammer:
            text += f"<b>Active Spammer:</b> <code>True</code>\n"
        if spbinfo.attributes.is_blacklisted:
            text += f"<b>Blacklisted:</b> <code>True</code>\n"
            text += f"<b>Blacklist Reason:</b> <code>{spbinfo.attributes.blacklist_reason}</code>\n"
        if spbinfo.attributes.original_private_id:
            text += f"<b>Original Private ID:</b> <code>{spbinfo.attributes.original_private_id}</code>\n"
    return text


def LastOnline(user: User):
    if user.is_bot:
        return ""
    elif user.status == 'recently':
        return "Recently"
    elif user.status == 'within_week':
        return "Within the last week"
    elif user.status == 'within_month':
        return "Within the last month"
    elif user.status == 'long_time_ago':
        return "A long time ago :("
    elif user.status == 'online':
        return "Currently Online"
    elif user.status == 'offline':
        return datetime.fromtimestamp(user.status.date).strftime("%a, %d %b %Y, %H:%M:%S")

async def GetCommon(client, get_user):
    common = await client.send(
        functions.messages.GetCommonChats(
            user_id=await client.resolve_peer(get_user),
            max_id=0,
            limit=0))
    return common

@Client.on_message(filters.me & filters.command(["whois"], prefixes=config['config']['prefixes']))
async def whois(client, message):
    cmd = message.command
    if not message.reply_to_message and len(cmd) == 1:
        get_user = message.from_user.id
    elif message.reply_to_message and len(cmd) == 1:
        get_user = message.reply_to_message.from_user.id
    elif len(cmd) > 1:
        get_user = cmd[1]
        try:
            get_user = int(cmd[1])
        except ValueError:
            pass
    try:
        user, uclient = await get_entity(client, get_user)
    except:
        await message.reply(f"Unable to resolve the query '{get_user}'!")
        return
        
    desc = await client.get_chat(get_user)
    if desc.bio:
        desc = desc.bio
    else:
        desc = desc.description
    spbinfo = await spb.lookup(user.id)

    # discard the lookup.
    if spbinfo:
        if not spbinfo.success:
            spbinfo = None

    text = "<b>User Information</b>\n\n"
    thingtype = "User"
    if spbinfo:
        if spbinfo.entity_type == "supergroup":
            thingtype = "Chat"
            text = "<b>Chat Information</b>\n\n"
        if spbinfo.entity_type == "channel":
            thingtype = "Channel"
            text = "<b>Channel Information</b>\n\n"
    else:
        if user.id < 0:
            thingtype = "Chat"
            text = "<b>Chat Information</b>\n\n"

    text += await _get_flags(spbinfo)

    if spbinfo:
        text += f"<b>Private ID:</b> <code>{spbinfo.private_telegram_id}</code>\n"

    text += f"<b>{thingtype} ID:</b> <code>{user.id}</code>\n"
    if isinstance(user, User):
        if user.first_name:
            text += f"<b>First Name:</b> <code>{user.first_name}</code>\n"
        if user.last_name:
            text += f"<b>Last Name:</b> <code>{user.last_name}</code>\n"
    else:
        if user.title:
            text += f"<b>Title:</b> <code>{user.title}</code>\n"
    if user.username:
        text += f"<b>Username:</b> <code>{user.username}</code> (@{user.username})\n"
    if not isinstance(user, Chat):
        common = await GetCommon(client, user.id)
        text += f"<b>Last Online:</b> {LastOnline(user)}\n"
        if len(common.chats) > 0:
            text += f"<b>Common Chats:</b> {len(common.chats)}\n"

    text += await _get_info(spbinfo)

    if isinstance(user, User):
        text += f'<b>{thingtype} Link:</b> <a href="tg://user?id={user.id}">tg://user?id={user.id}</a>\n'
    if desc:
        text += f"<b>Description:</b> {desc}"
    await message.reply(text)
