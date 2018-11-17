#!python
# This program checks the "heartbeat.txt" for the last time
# packets came from websockets data stream. If the last packet was received between 6-20 seconds ago,
# it will restart the program by sending a signal to "signal-heartbeat.txt" which will be read by the main algo.
# If the last packet was received more than 20 seconds ago, 
# it will check if there is an internet connection by pinging to google. 
# If there is internet, that means the program had frozen and needs a brute force start
# by pressing "ctrl+c". If there is no internet, it wont do "ctrl+c" because that will kill
# the complete program. So it will wait untill there is internet and do a brute force again. 


import os
import time
import datetime
import pyautogui
pyautogui.FAILSAFE = True

tradestartepoch=int(datetime.datetime(int(str(datetime.datetime.now().date()).split('-')[0]), int(str(datetime.datetime.now().date()).split('-')[1]), int(str(datetime.datetime.now().date()).split('-')[2]), 9, 15, 5, 0).strftime('%s'))
tradeendepoch=int(datetime.datetime(int(str(datetime.datetime.now().date()).split('-')[0]), int(str(datetime.datetime.now().date()).split('-')[1]), int(str(datetime.datetime.now().date()).split('-')[2]), 15, 18, 0, 0).strftime('%s'))
epochnow=int(time.time())

while epochnow<=tradestartepoch:
	epochnow=int(time.time())
	time.sleep(0.5)
while epochnow<=tradeendepoch:
	epochnow=int(time.time())
	try:
		fo =open("heartbeat.txt", "r")
		line=fo.readline()
		fo.close()
		if len(line)>1:
			lastbeat=int(str(line))
			if 20>epochnow-lastbeat>=6:
				#print("HEARTBEAT RESTARTED"+str(datetime.datetime.now().time()).split()[0][0:5])
				fr =open("signal-heartbeat.txt", "w")
				fr.write("restart")
				fr.close()
			elif epochnow-lastbeat>=20:
				response=os.system('ping -c 1 www.google.com')
				if response==0:
					print("BRUTEFORCE APPLIED"+str(datetime.datetime.now().time()).split()[0][0:5])
					pyautogui.click(x=368, y=506) 
					pyautogui.hotkey('ctrl', 'c',)
					time.sleep(10)
					pyautogui.click(x=368, y=506)
					pyautogui.press('up')
					pyautogui.press('enter')
					time.sleep(10)
				else:
					print("NO INTERNET, BRUTEFORCE WONT BE APPLIED")
		else:
			continue
	except Exception as e:
		#print("Error",str(e))
		time.sleep(0.001)
	time.sleep(0.1)



