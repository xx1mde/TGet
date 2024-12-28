import colorama, sys, asyncio, os, time
import pyrogram
from pyrogram.enums import ChatType
from objects import FlagsObject, TGetObjects, _DumpObjects

class CommandObserver(object):
	def __init__(self,  *args, **kwargs):

		self._Logger = args[0]

		self._commands = {
			"chats": (self.getChats, "List chats with their id"),
			"help": (self.helper, "Description of available commands"),
			"dump": (self.dumper, f"[{colorama.Fore.MAGENTA}dump <chat_id/channel_id>{colorama.Fore.RESET}] Get a list of file extensions in a dialog/channel"),
			"load": (self.loader, f"[{colorama.Fore.MAGENTA}load <extension>{colorama.Fore.RESET}] Upload files with the selected extension from the last {colorama.Fore.MAGENTA}dump{colorama.Fore.RESET} command. The new {colorama.Fore.MAGENTA}dump{colorama.Fore.RESET} command will create a new set of files."),
			"exit": (self.__exit, "Exit")
		}

	async def __exit(self, *args): sys.exit(1)

	async def dumper(self, *args):
		if len(args) != 1:
			self._Logger.stderr("Incorrect number of arguments. Usage: dump <chat_id/channel_id>. Example: dump 7700006611"); return
		else:
			_DumpObjects.LastChatDump.clear()
			async for message in TGetObjects.ClientObject.get_chat_history(int(args[0])):
				if message.document:
					_extensionFromArgument = message.document.file_name.split(".")[-1].lower()
					if _extensionFromArgument in _DumpObjects.LastChatDump.keys(): _DumpObjects.LastChatDump[_extensionFromArgument].add(message.id)
					else:
						_DumpObjects.LastChatDump[_extensionFromArgument] = set()
						_DumpObjects.LastChatDump[_extensionFromArgument].add(message.id)

			_DumpObjects._chatID = int(args[0])
			for _extension, _IDsByCurrentExtension in _DumpObjects.LastChatDump.items():
				print(f"{colorama.Fore.MAGENTA}{_extension}:{colorama.Fore.RESET} {len(_IDsByCurrentExtension)} quantity")

	async def _backendFileDownload(self, _messageObject: object, path: str):
		if _messageObject.document:
			try:
				await _messageObject.download(file_name=os.path.abspath(path))
				self._Logger.log(f"The {_messageObject.document.file_name} has been downloaded.")
			except Exception as e: pass

	async def loader(self, *args):
		if len(args) != 1:
			self._Logger.stderr("Incorrect number of arguments. Usage: load <extension>. Example: load pdf"); return
		if not args[0] in _DumpObjects.LastChatDump.keys():
			self._Logger.stderr(f"Incorrect argument. The latest dump contains the following extensions: {list(_DumpObjects.LastChatDump.keys())}"); return

		_absolutePathDownload = os.path.abspath(f"{TGetObjects.PathDownload}/{args[0]}")
		os.makedirs(_absolutePathDownload, exist_ok=True)
		_IDsByArgExtension = list(_DumpObjects.LastChatDump[args[0]])

		self._Logger.log(f"PathDownload: {_absolutePathDownload}\n")
		self._startLoad = time.time()
		while len(_IDsByArgExtension) != 0:
			try:
				_media = await TGetObjects.ClientObject.get_messages(chat_id=_DumpObjects._chatID, message_ids=_IDsByArgExtension[:5])
				_IDsByArgExtension = _IDsByArgExtension[5:]
				await asyncio.gather(
					*[asyncio.create_task(
						self._backendFileDownload(
							_message,
							f"{TGetObjects.PathDownload}/{args[0]}/{_message.document.file_name}"
						)) for _message in _media])
				await asyncio.sleep(0.3)
			except pyrogram.errors.FloodWait as _error:
				self._Logger.stderr("TG API FloodWait: {_error.value}s")
				await asyncio.sleep(_error.value)
			except Exception: pass
		print()
		self._Logger.log(f"Time: {round(time.time() - self._startLoad, 2)}s")


	async def getChats(self, *args):
		_setChannels = set()
		async for _chat in TGetObjects.ClientObject.get_dialogs():
			if _chat.chat.id in _setChannels: continue
			else:
				_setChannels.add(_chat.chat.id)
				print(
					f"{colorama.Fore.GREEN}{_chat.chat.id}{colorama.Fore.RESET} - "
					f"{colorama.Fore.MAGENTA}title: {colorama.Fore.RESET}{_chat.chat.title}, "
					f"{colorama.Fore.MAGENTA}username: {colorama.Fore.RESET}@{_chat.chat.username}"
				)

	async def helper(self, *args):
		for key, value in self._commands.items():
			print(f"{colorama.Fore.MAGENTA}{key}:{colorama.Fore.RESET} {value[-1]}")

	async def run(self):
		while FlagsObject.CycleFlag:
			try:
				self.command = input(f"\ncommand{colorama.Fore.GREEN} > {colorama.Fore.RESET}").lower().strip()
				self._copyCommandForVerify = [x for x in self.command.split(" ") if len(x) > 0]
				if self._copyCommandForVerify[0] in self._commands.keys(): await self._commands.get(self._copyCommandForVerify[0])[0](*self._copyCommandForVerify[1:])
				else: self._Logger.stderr(f"Unsupported command: {self._copyCommandForVerify[0]}")
			except KeyboardInterrupt: sys.exit(1)
			except Exception: pass