#!python
# Closes all open positions after 15:17 to avoid auto-squareoff from the broker. 


import os
import time
import datetime
from xxxx import xxxx


tradeendepoch=int(datetime.datetime(int(str(datetime.datetime.now().date()).split('-')[0]), int(str(datetime.datetime.now().date()).split('-')[1]), int(str(datetime.datetime.now().date()).split('-')[2]), 15, 18, 0, 0).strftime('%s'))
squareoffepoch=int(datetime.datetime(int(str(datetime.datetime.now().date()).split('-')[0]), int(str(datetime.datetime.now().date()).split('-')[1]), int(str(datetime.datetime.now().date()).split('-')[2]), 15, 20, 0, 0).strftime('%s'))
epochnow=int(time.time())
while epochnow<tradeendepoch:
	epochnow=int(time.time())
	time.sleep(5)



ticket=open("accessticket.txt").read().splitlines()
api_key= 'xxxx'
user_id=str(ticket[0])
access_token=str(ticket[1])
public_token= str(ticket[2])
xxxx = xxxx(api_key=api_key)
xxxx.set_access_token(access_token)



#-------IF the time is after 15:17, close all open positions
while epochnow<=squareoffepoch:
	print("Trading time up for the day!! Now Closing all positions")
	epochnow=int(time.time())
	try:
		positionlist=xxxx.positions()
		positions=positionlist['net']
		if len(positions)>0:
			for openpositions in positions:
				symbol=str(openpositions['tradingsymbol'])
				InstrumentToken=int(openpositions['instrument_token'])
				openquantity=int(openpositions['quantity'])
				print(symbol,InstrumentToken,openquantity)
				if 	openquantity<0:
					try:
						buy= xxxx.order_place('NSE', symbol, 'BUY',quantity=abs(openquantity), price=None, product='MIS', order_type='MARKET', validity='DAY', disclosed_quantity=abs(openquantity), trigger_price=None, squareoff_value=None, stoploss_value=None, trailing_stoploss=None, variety='regular')
						#buy=999
						print("Closing SELL Positions", InstrumentToken,symbol, "at",str(str(datetime.datetime.now().time()).split()[0][0:5]),"OrderID", buy)
					except Exception as f:	
						buy= xxxx.order_place('NSE', symbol, 'BUY',quantity=abs(openquantity), price=None, product='MIS', order_type='MARKET', validity='DAY', disclosed_quantity=abs(openquantity), trigger_price=None, squareoff_value=None, stoploss_value=None, trailing_stoploss=None, variety='regular')
						#buy=999
						print("Closing SELL Positions", InstrumentToken,symbol, "at",str(str(datetime.datetime.now().time()).split()[0][0:5]),"OrderID", buy)
				elif 	openquantity>0:
					try:
						sell= xxxx.order_place('NSE', symbol, 'SELL',quantity=abs(openquantity), price=None, product='MIS', order_type='MARKET', validity='DAY', disclosed_quantity=abs(openquantity), trigger_price=None, squareoff_value=None, stoploss_value=None, trailing_stoploss=None, variety='regular')
						#sell=999
						print("Closing BUY Positions", InstrumentToken,symbol, "at",str(str(datetime.datetime.now().time()).split()[0][0:5]),"OrderID", sell)
					except Exception as f:
						sell= xxxx.order_place('NSE', symbol, 'SELL',quantity=abs(openquantity), price=None, product='MIS', order_type='MARKET', validity='DAY', disclosed_quantity=abs(openquantity), trigger_price=None, squareoff_value=None, stoploss_value=None, trailing_stoploss=None, variety='regular')
						#sell=999
						print("Closing BUY Positions", InstrumentToken,symbol, "at",str(str(datetime.datetime.now().time()).split()[0][0:5]),"OrderID", sell)
				else:
					continue
			time.sleep(10)
	except Exception as e:
		print(str(e))
