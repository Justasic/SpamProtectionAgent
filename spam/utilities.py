import asyncio
from pyrogram.types import Chat, User, Message
from pyrogram.errors.exceptions.bad_request_400 import PeerIdInvalid, ChannelInvalid
from spam import clients

async def self_destruct(message, text):
    await message.edit(text)
    await asyncio.sleep(2)
    await message.delete()

async def get_entity(client, entity):
	entity_client = client
	if not isinstance(entity, Chat):
		try:
			entity = int(entity)
		except ValueError:
			pass
		except TypeError:
			entity = entity.id
		try:
			entity = await client.get_chat(entity)
		except (PeerIdInvalid, ChannelInvalid):
			for app in clients:
				if app != client:
					try:
						entity = await app.get_chat(entity)
					except (PeerIdInvalid, ChannelInvalid):
						pass
					else:
						entity_client = app
						break
	return entity, entity_client