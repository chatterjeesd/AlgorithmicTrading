#!python
# Starts the main algo and write the signal in "signal-mainalgo.txt" file.
# It will keep checking the signal file and if it finds out that the main algo has stopped
#(CLOSED) written in signal file, it will restart the main algo.

import os
import time
import datetime


tradestartepoch=int(datetime.datetime(int(str(datetime.datetime.now().date()).split('-')[0]), int(str(datetime.datetime.now().date()).split('-')[1]), int(str(datetime.datetime.now().date()).split('-')[2]), 9, 15, 0, 0).strftime('%s'))
tradeendepoch=int(datetime.datetime(int(str(datetime.datetime.now().date()).split('-')[0]), int(str(datetime.datetime.now().date()).split('-')[1]), int(str(datetime.datetime.now().date()).split('-')[2]), 15, 17, 0, 0).strftime('%s'))
epochnow=int(time.time())

while epochnow<=tradestartepoch:
	epochnow=int(time.time())
	time.sleep(0.5)
os.system("python3 mainalgo.py")
while epochnow<=tradeendepoch:
	epochnow=int(time.time())
	time.sleep(0.5)
	fo =open("signal-mainalgo.txt", "r")
	for line in fo:
		if "CLOSED" in line:
			print("RESTARTED"+str(datetime.datetime.now().time()).split()[0][0:5])
			fr =open("signal-mainalgo.txt", "w")
			fr.write("")
			fr.close()			
			os.system("python3 mainalgo.py")
	fo.close()

