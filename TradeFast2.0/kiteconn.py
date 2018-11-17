#!python
# This two-part program automates the following processes so that I don't have to wake up early in the morning to login to
# my brokerage website:
#- Open the selenium browser to access the login page. 
#- Confirm the identity of the page
#- enter user_id, password and asnwer 2fa questions to get the request token.
#- Once request token is received, get access token and public token.
#- Save all tokens in "accessticket.txt". This will be used to read the token in case of connection failure.
# 
# The program also makes the decision of how many stocks the main algo will buy per 'x' minutes to cost average the purchase.
# Depending on the cash left and stock price, if one or more stocks can be bought per min, the main algo does so.
# Otherwise it buys one stock every x minutes.

from xxxxx import xxxxx
from xxxxx import WebSocket
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import os
import datetime
import time

symbolname=['ORIENTBANK', 'PNB', 'INDIACEM', 'APOLLOTYRE', 'BANKINDIA', 'UNIONBANK','ITC', 'VEDL'] #['FEDERALBNK', 'ITC', 'VEDL', 'ICICIBANK', 'SBIN']

accessstartepoch=int(datetime.datetime(int(str(datetime.datetime.now().date()).split('-')[0]), int(str(datetime.datetime.now().date()).split('-')[1]), int(str(datetime.datetime.now().date()).split('-')[2]), 9, 0, 0, 0).strftime('%s'))
epochnow=int(time.time())
while epochnow<accessstartepoch:
	epochnow=int(time.time())
	time.sleep(10)

#####-------------------OPEN A BROWSER AND GET REQUEST TOKEN---###########
driver = webdriver.Firefox()
driver.get("https://xxxx.yyyy/connect/login?api_key=tttttt")
assert "xxxx" in driver.title
time.sleep(1)
demo_link =driver.find_element_by_name('user_id').send_keys("xxxx")
time.sleep(1)
demo_link =driver.find_element_by_name('password').send_keys("xxxxxx")
time.sleep(1)
demo_link =driver.find_element_by_name('login').click()
time.sleep(1)
demo_link =driver.find_element_by_name('answer1').send_keys("xxxx")
time.sleep(1)
demo_link =driver.find_element_by_name('answer2').send_keys("xxxx")
time.sleep(1)
try:
	demo_link =driver.find_element_by_name('twofa').click()
except Exception as e:
	requesttokenurl=driver.current_url
	requesttoken=str(requesttokenurl.split('request_token=')[1])
	print "Request Token is:",requesttoken
driver.get("https://xxxx.xxxx.com/")
assert "xxxx" in driver.title
#driver.close()
time.sleep(1)
#####################------START HERE-----######################################
api_key = "xxxx"
api_secret = "yyyy"

# Initialise.
xxxx = xxxxConnect(api_key=api_key)

#---------------------------TO GET THE ACCESS TOKEN AND PUBLIC TOKEN-----------------------------
try:
	user = xxxx.request_access_token(request_token=requesttoken, secret=api_secret)
	xxxx.set_access_token(user["access_token"])
except Exception as e:
	print("Authentication failed", str(e))
	raise
############---GET CASH DETAILS-----------------
prices=[]
for name in symbolname:
	prices.append((xxxx.quote(exchange="NSE", tradingsymbol=name))['last_price'])
margindaystart=xxxx.margins("equity")
totalcash=float(margindaystart['available']['cash'])
cashtotrade=totalcash-1000
leverage=10
profittarget=1
stockprice=max(prices)
tradingtime=365 #minutes from trade open to square off
numberofstocks=cashtotrade*leverage/stockprice
expectedprofit=float(profittarget)/100*cashtotrade
reqminpricechange=(float(profittarget)/float(leverage))/100*float(stockprice)
reqminpercentchange=reqminpricechange/stockprice*100
stockspermin=numberofstocks/tradingtime
if stockspermin<1:
	for i in range(1,61):
		if int(i*stockspermin)>=1:
			stocks=int(i*stockspermin)
			timedelta=int(i)
			break
	print "cash",cashtotrade, "profittarget", profittarget, "stockprice", stockprice, "numberofstocks", numberofstocks, "expectedprofit", expectedprofit, "reqminpricechange", reqminpricechange, "reqminpercentchange", reqminpercentchange, stocks, "stocksper", i, "min"

if stockspermin>=1:
	print "cashtotrade",cashtotrade, "profittarget", profittarget, "stockprice", stockprice, "numberofstocks", numberofstocks, "expectedprofit", expectedprofit, "reqminpricechange", reqminpricechange, "reqminpercentchange", reqminpercentchange, "stockspermin", stockspermin
	stocks=int(stockspermin)
	timedelta=1


ticket=open("accessticket.txt",'w')
ticket.write(str(user["user_id"])+'\n'+str(user["access_token"])+'\n'+str(user["public_token"])+'\n'+str(totalcash)+'\n'+str(cashtotrade)+'\n'+str(stocks)+'\n'+str(timedelta))
ticket.close()
print(str(user["user_id"]), "has logged in with ",str(user["access_token"]),"access token and", str(user["public_token"]), "as public token")
print "CHANGE TIME ZONE TO INDIAN TIME"
print "Now run python squareoff.py"
print "Run python3 start-mainalgo.py"
print "Run python checkheartbeat.py"



