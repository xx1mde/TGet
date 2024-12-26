import json, os, colorama

colorama.init(autoreset=True)
os.makedirs("data/", exist_ok=True)

class Configurator(object):

	_EXISTS = False
	_elements = {"API_ID": None, "API_HASH": None, "NumberPhone": None, "PathDownload": None}
	_hints = {
		"API_ID": "",
		"API_HASH": "",
		"NumberPhone": f"{colorama.Fore.RED} (no spaces or extra characters!){colorama.Fore.RESET}",
		"PathDownload": ""
	}

	def __init__(self, *args): self._EXISTS = os.path.exists(os.path.abspath(f"{os.getcwd()}/data/config.json"))

	def create(self):

		for key, item in self._elements.items():
			__stdin = input(f"{colorama.Fore.GREEN}> {key}{colorama.Fore.RESET}{self._hints[key]} [now - {item}]: ")
			if len(__stdin) == 0: continue
			else:
				if key == "PathDownload": self._elements[key] = os.path.abspath(__stdin)
				else: self._elements[key] = __stdin

		with open("data/config.json", "w") as config: print(json.dumps(self._elements, indent=4), file=config)

	def parse(self, config_object: object):
		self._elements = config_object
		self.create()

	def run(self):
		if self._EXISTS:
			with open("data/config.json", "r") as config:
				try:
					self._configObject = json.loads(config.read())
					self.parse(self._configObject)
					return
				except Exception:
					print(f"{colorama.Fore.RED}Exception when reading config, please reconfigure the config.")
			os.remove("data/config.json")
		else: self.create()

if __name__ == "__main__": Configurator().run()