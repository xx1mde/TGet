import colorama, sys, asyncio, os
from pyrogram.enums import ChatType
from objects import FlagsObject, TGetObjects, _DumpObjects

class CommandObserver(object):
	def __init__(self,  *args, **kwargs):
		self._commands = {
			"chats": (self.getChats, "List chats with their id"),
			"help": (self.helper, "Description of available commands"),
			"dump": (self.dumper, f"[{colorama.Fore.MAGENTA}dump <chat_id/channel_id>{colorama.Fore.RESET}] Get a list of file extensions in a dialog/channel"),
			"load": (self.loader, f"[{colorama.Fore.MAGENTA}load <extension>/all{colorama.Fore.RESET}] Upload files with the selected extension from the last {colorama.Fore.MAGENTA}dump{colorama.Fore.RESET} command. The new {colorama.Fore.MAGENTA}dump{colorama.Fore.RESET} command will create a new set of files."),
			"exit": (self.__exit, "Exit")
		}

	async def __exit(self): sys.exit(1)

	async def dumper(self, *args):
		if len(args) != 1:
			print(f"{colorama.Fore.RED}Incorrect number of arguments.{colorama.Fore.RESET} Usage: {colorama.Fore.MAGENTA}dump <chat_id/channel_id>{colorama.Fore.RESET}. Example: {colorama.Fore.MAGENTA}dump 7700006611{colorama.Fore.RESET}")
			return
		else:
			_DumpObjects.LastChatDump.clear()
			async for message in TGetObjects.ClientObject.get_chat_history(int(args[0])):
				if message.document:
					_extension = message.document.file_name.split(".")[-1].lower()
					if _extension in _DumpObjects.LastChatDump.keys(): _DumpObjects.LastChatDump[_extension].add(message.id)
					else:
						_DumpObjects.LastChatDump[_extension] = set()
						_DumpObjects.LastChatDump[_extension].add(message.id)

			_DumpObjects._chatID = int(args[0])
			for _ext, _ids in _DumpObjects.LastChatDump.items(): print(f"{colorama.Fore.MAGENTA}{_ext}:{colorama.Fore.RESET} {len(_ids)} quantity")

	async def _backendFileDownload(self, _messageObject: object, path: str):
		if _messageObject.document:
			try:
				await _messageObject.download(file_name=os.path.abspath(path))
			except Exception as e: pass
			print(f"The {colorama.Fore.MAGENTA}{_messageObject.document.file_name}{colorama.Fore.RESET} has been downloaded.")

	async def loader(self, *args):
		if len(args) != 1:
			print(f"{colorama.Fore.RED}Incorrect number of arguments.{colorama.Fore.RESET} Usage: {colorama.Fore.MAGENTA}load <extension>/all{colorama.Fore.RESET}. Example: {colorama.Fore.MAGENTA}load all; load pdf{colorama.Fore.RESET}")
			return
		if not args[0] in _DumpObjects.LastChatDump.keys():
			print(f"{colorama.Fore.RED}Incorrect argument.{colorama.Fore.RESET} The latest dump contains the following extensions: {list(_DumpObjects.LastChatDump.keys())}")
			return

		_normalDir = os.path.abspath(f"{TGetObjects.PathDownload}/{args[0]}")
		os.makedirs(_normalDir, exist_ok=True)
		_localIDs = list(_DumpObjects.LastChatDump[args[0]])

		print(f"\n{colorama.Fore.GREEN}PathDownload: {colorama.Fore.RESET}{_normalDir}")
		while len(_localIDs) != 0:
			_media = await TGetObjects.ClientObject.get_messages(chat_id=_DumpObjects._chatID, message_ids=_localIDs[:5])
			print(f"\nLoad next {colorama.Fore.MAGENTA}{len(_media)}{colorama.Fore.RESET} {args[0]}")
			_localIDs = _localIDs[5:]
			_tasks = [asyncio.create_task(self._backendFileDownload(_message, f"{TGetObjects.PathDownload}/{args[0]}/{_message.document.file_name}")) for _message in _media]
			await asyncio.gather(*_tasks)
			await asyncio.sleep(0.3)


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
				else: print("Unsupported command")
			except KeyboardInterrupt: sys.exit(1)
			except Exception: pass