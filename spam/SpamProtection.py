from spamprotection import SPBClient

class AccessException(Exception):
	pass

class SpamProtection:

	def __init__(self, token):
		self.token = token
		self.lookupclient = SPBClient()

	async def lookup(self, entity):
		try:
			return await self.lookupclient.check_blacklist(entity)
		except:
			return None

	async def queue_message(self, message):
		pass

	async def blacklist(self, entity, flag):
		pass

	async def log(self, entity, message):
		# Check if they're an operator first
		try:
			spbinfo = await self.lookup(message.from_user.id)
		except:
			raise AccessException("API is unavailable, please try again later.")
		if spbinfo.attributes.is_operator or spbinfo.attributes.is_agent:
			pass
		else:
			raise AccessException("You must be an operator to use this command")
