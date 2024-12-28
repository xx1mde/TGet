import pyrogram, json, platform, asyncio, sys, os, atexit, threading

from modules.logger import Logger
from modules.command import CommandObserver
from objects import TGetObjects, FlagsObject


if platform.system() == "Linux":
	import uvloop
	asyncio.set_event_loop_policy(uvloop.EventLoop())
	Logger.log("LibUV policy setted")
else: Logger.log("LibUV is not supported")

class TGetCore(object):
	def __init__(self, *args):

		atexit.register(self._exitEvent)

		try:
			with open("data/config.json", "r") as config:
				self._DeserealizedJSONConfig = json.loads(config.read())
				TGetObjects.PathDownload = self._DeserealizedJSONConfig["PathDownload"]
				self.initializeClient()
		except Exception:
			Logger.stderr("Error loading config. Create a new config via configure.exe")
			sys.exit(1)

	def initializeClient(self):
		if all([x != None for x in self._DeserealizedJSONConfig.values()]):
			try:
				TGetObjects.ClientObject = pyrogram.Client(
					"data/client",
					api_id=self._DeserealizedJSONConfig["API_ID"],
					api_hash=self._DeserealizedJSONConfig["API_HASH"],
					phone_number=self._DeserealizedJSONConfig["NumberPhone"])
			except Exception:
				Logger.stderr("Error connecting to account")
				sys.exit(1)
		else:
			Logger.stderr("Error loading config. Create a new config via configure.exe")
			sys.exit(1)

	async def runCore(self):
		async with TGetObjects.ClientObject:
			Logger.clear()
			Logger.hello()
			await CommandObserver(Logger).run()

	def startClient(self): TGetObjects.ClientObject.run(self.runCore())
	def _exitEvent(self):
		print()
		Logger.log("Close TGet")
		FlagsObject.CycleFlag = False

if __name__ == "__main__":
	TGetCore().startClient()