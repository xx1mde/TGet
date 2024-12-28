import colorama, datetime, os, platform
colorama.init(autoreset=True)

class Logger(object):
	@staticmethod
	def log(logStr: str) -> None: print(f"{colorama.Fore.GREEN}[LOG][{datetime.datetime.now().strftime('%H:%M:%S')}]{colorama.Fore.RESET} - {logStr}")
	@staticmethod
	def stderr(errStr: str) -> None: print(f"{colorama.Fore.RED}[ERROR][{datetime.datetime.now().strftime('%H:%M:%S')}]{colorama.Fore.RESET} - {errStr}")
	@staticmethod
	def clear(): os.system("clear" if platform.system() == "Linux" else "cls")
	@staticmethod
	def hello():
		print(
f"""░░░░░░░░ ░░░░░░░░ ░░░░░░░░ ░░░░░░░░ 
   ▒▒    ▒▒       ▒▒          ▒▒    
   ▒▒    ▒▒   ▒▒▒ ▒▒▒▒▒       ▒▒    
   ▓▓    ▓▓    ▓▓ ▓▓          ▓▓    
   ██    ████████ ████████    ██    
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 
 {colorama.Fore.MAGENTA}Telegram Getter v0.1 stable{colorama.Fore.RESET}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━""")