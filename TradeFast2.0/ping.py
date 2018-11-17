#!python
#This one does a hard reset if there is a loss of internet
#while trades are firing.



import os
import time
while True:
	response=os.system('ping -c 1 www.google.com')
	#print response
	if response!=0:
		print "Internet gone, restarted"
		os.system('sudo restart network-manager')
	time.sleep(10)
