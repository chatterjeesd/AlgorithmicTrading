#!python
import numpy as np
from xxxxxx import xxxxxxx
from xxxxxx import WebSocket
import requests
import logging
import json
import itertools
import time
import datetime
import math
#logging.basicConfig(level=logging.DEBUG)


ticket=open("accessticket.txt").read().splitlines()
api_key= 'xxxxxxxxxx'
user_id=str(ticket[0])
access_token=str(ticket[1])
public_token= str(ticket[2])
totalcash=float(ticket[3])
cashtotrade=totalcash-1000
leverage=10
profittarget=1
tradingtime=21720 #seconds till 15:17
expectedprofit=float(profittarget)/100*cashtotrade

xxxxxx = xxxxxx(api_key=api_key)
xxxxx.set_access_token(access_token)
#print(xxxx.positions())
#print(xxxx.quote(exchange="NSE", tradingsymbol="HDIL"))
# Initialise. api_key, public_token, user_id are correct just as obtained.
yyy = WebSocket(api_key, public_token, user_id)

# Callback for tick reception.
symbolname=['ORIENTBANK', 'PNB', 'INDIACEM', 'APOLLOTYRE', 'BANKINDIA', 'UNIONBANK','ITC', 'VEDL'] #['FEDERALBNK', 'ITC', 'VEDL', 'ICICIBANK', 'SBIN']
symbollist=[636673, 2730497, 387841, 41729, 1214721, 2752769, 424961, 784129]#[261889, 424961, 784129, 1270529, 779521]

print("Total Symbols:", len(symbollist), len(symbolname))
for symbols in symbollist:
		fo= open('./data/'+str(symbols)+".txt", 'a')
		fo.close()
		fr= open('./data/'+str(symbols)+".txt", 'r')	
		lineList = fr.readlines()
		if len(lineList)==0:
			fo= open('./data/'+str(symbols)+".txt", 'a')
			fo.write("Date"+'\t'+"Timestamp"+'\t'+"LastPrice"+'\t'+"Bid"+'\t'+"BidQuantity"+'\t'+"Ask"+'\t'+"AskQuantity"+'\t'+"Volume"+'\t'+"TRS"+'\t'+"MB"+'\t'+"MBsmall"+'\t'+"TRL"+'\t'+"BuyPrice"+'\t'+"BuyEntryOrderId"+'\t'+"BuyEntryQuantity"+'\t'+"BuyEntryTime"+'\t'+"BuyExitOrderID"+'\t'+"BuyExitQuantity"+'\t'+"SellPrice"+'\t'+"SellEntryOrderID"+'\t'+"SellEntryQuantity"+'\t'+"SellEntryTime"+'\t'+"SellExitOrderID"+'\t'+"SellExitQuantity"+'\t'+"BuyPnl"+'\t'+"SellPnl"+'\n')
			fo.close()			
		else:
			continue
		fr.close()



start = time.time()
def on_tick(tick, ws):
	beatnows=0
	try:
		#print(len(tick))
		for i in tick:
			#print(i)
			#start = time.time()
			#print(i['instrument_token'],i['last_price'])
			d=json.dumps(i)
			e= json.loads(d)
			depth=e['depth']
			instrumenttoken=e['instrument_token']
			lastprice=float(e['last_price'])
			volumep=int(e['volume'])
			ohlcopen=float(e['ohlc']['open'])
			selldom=depth['sell']
			buydom=depth['buy']
			latestbuyline=buydom[0]
			latestsellline=selldom[0]
			latestbid= float(latestbuyline['price'])
			latestask= float(latestsellline['price'])
			latestbidquantity= int(latestbuyline['quantity'])
			latestaskquantity= int(latestsellline['quantity'])
			if instrumenttoken in symbollist:
				Datelist=[]
				Timelist=[]
				LTPlist=[]
				buyprice=[0]
				buyentryorderid=[0]
				BuyentryQuantity=[0]
				BuyEntryTime=[0]
				buyexitorderid=[0]
				BuyexitQuantity=[0]
				sellprice=[0]
				sellentryorderid=[0]
				SellentryQuantity=[0]
				SellEntryTime=[0]
				sellexitorderid=[0]
				SellexitQuantity=[0]
				BuyPnl=[0]
				SellPnl=[0]
				#mblist=[0]
				#mbsmalllist=[0]
				trs=[]
				trl=[]
				m=1000
				n=50
				dev=2
				ticksize= 0.05
				risk=0.2
				reward=4
				#timedelta=2
				#trailingstop=10/100*reward
				maxsuccessiveloss=1

				fr= open('./data/'+str(instrumenttoken)+".txt", 'r')
				
				lineList = fr.readlines()[-m:]
				
				if len(lineList)== 1:
					LTPlist.append(float(lastprice))
					
				elif len(lineList)> 1 :
					for line in lineList:
						if 'Timestamp' not in line:
							Datelist.append(str(line.split()[0]))
							Timelist.append(str(line.split()[1]))
							LTPlist.append(float(line.split()[2]))
							trs.append(float(line.split()[8]))
							#mblist.append(float(line.split()[9]))
							#mbsmalllist.append(float(line.split()[10]))
							trl.append(float(line.split()[11]))							
							buyprice.append(float(line.split()[12]))
							buyentryorderid.append(int(line.split()[13]))
							BuyentryQuantity.append(int(line.split()[14]))
							BuyEntryTime.append(int(line.split()[15]))
							buyexitorderid.append(int(line.split()[16]))
							BuyexitQuantity.append(int(line.split()[17]))
							sellprice.append(float(line.split()[18]))
							sellentryorderid.append(int(line.split()[19]))
							SellentryQuantity.append(int(line.split()[20]))
							SellEntryTime.append(int(line.split()[21]))							
							sellexitorderid.append(int(line.split()[22]))
							SellexitQuantity.append(int(line.split()[23]))
							BuyPnl.append(int(line.split()[24]))
							SellPnl.append(int(line.split()[25]))
					
						
					if int(lineList[-1].split()[7]) != int(volumep):
						LTPlist.append(float(lastprice))
				fr.close()
				#print(orderid)
				######-------------------------TIMER ZONE-------------------------############
				tradeendepoch=int(datetime.datetime(int(str(datetime.datetime.now().date()).split('-')[0]), int(str(datetime.datetime.now().date()).split('-')[1]), int(str(datetime.datetime.now().date()).split('-')[2]), 15, 18, 0, 0).strftime('%s'))
				squareoffepoch=int(datetime.datetime(int(str(datetime.datetime.now().date()).split('-')[0]), int(str(datetime.datetime.now().date()).split('-')[1]), int(str(datetime.datetime.now().date()).split('-')[2]), 15, 20, 0, 0).strftime('%s'))
				epochnow=int(time.time())
				
				#stocks=1
				LTParray=np.array(LTPlist)			 
				#------------------RULES----------------------------------------------------
				# Get the SMAs. One long and another short to just smooth the price fluctuation
				# Open price not taken in to consideration.
				# If small MA goes above Long MA, go long but with DCA. Reverse for short.
				# For exiting position,......
				# Also take note of the cash available before trading. 
				# 
				#  
				#---------------------------------------------------------------------------
				def round_nearest(x, a):
					return round(x / a) * a
				def round_down(x, a):
					return math.floor(x / a) * a			 
			
				def movingaverage(values,window):
					weigths = np.repeat(1.0, window)/window
					smas = np.convolve(values, weigths, 'valid')
					return smas # as a numpy array
				
				
				def standard_deviation(tf, prices):
					sd=[]
					#sddate=[]
					x=tf
					while x<= len(prices):
						array2consider= prices[x-tf:x]
						standev= array2consider.std()
						sd.append(standev)
						#sddate.append(date[x])
						x+=1
					#return sddate, sd
					return sd
	
				
				def bollinger_bands(mult1, tff):
					#bdate=[]
					topBand=[]
					botBand=[]
					midBand=[]
	

					x=tff
					while x<len(LTParray)+1:
						curSMA= round(float((movingaverage(LTParray[x-tff:x], tff)[-1])), 3)
						curSD= standard_deviation(tff, LTParray[x-tff:x])
						curSD=curSD[-1]
						TB=round(round_nearest(float(curSMA+(curSD*mult1)), ticksize), 2) 
						BB=round(round_down(float(curSMA-(curSD*mult1)), ticksize), 2)					

						#bdate.append(D)
						topBand.append(TB)
						botBand.append(BB)
						midBand.append(curSMA)
						x+=1
	
					#return bdate, topBand, botBand, midBand,topBand2, botBand2, tff
					return topBand, botBand, midBand, tff
				tb, bb, mb, tfb= bollinger_bands(dev,m)
				tbsmall, bbsmall, mbsmall, tfbsmall=bollinger_bands(dev,n)
				
				trlong= float(LTPlist[-1]-(risk/100*LTPlist[-1]))
				trshort=float(LTPlist[-1]+(risk/100*LTPlist[-1]))				
				if len(lineList)==1:
					fs= open('./data/'+str(instrumenttoken)+".txt", 'a')

					trl.append(trlong)
					trs.append(trshort)					
					
					fs.write(str(str(datetime.datetime.now().date()).split()[0])+'\t'+str(str(datetime.datetime.now().time()).split()[0][0:5])+'\t'+str(LTPlist[-1])+'\t'+str(latestbid)+'\t'+str(latestbidquantity)+'\t'+str(latestask)+'\t'+str(latestaskquantity)+'\t'+str(volumep)+'\t'+str(trs[-1])+'\t'+str(len(mb))+'\t'+str(len(mbsmall))+'\t'+str(trl[-1])+'\t'+str(buyprice[-1])+'\t'+str(buyentryorderid[-1])+'\t'+str(BuyentryQuantity[-1])+'\t'+str(BuyEntryTime[-1])+'\t'+str(buyexitorderid[-1])+'\t'+str(BuyexitQuantity[-1])+'\t'+str(sellprice[-1])+'\t'+str(sellentryorderid[-1])+'\t'+str(SellentryQuantity[-1])+'\t'+str(SellEntryTime[-1])+'\t'+str(sellexitorderid[-1])+'\t'+str(SellexitQuantity[-1])+'\t'+str(BuyPnl[-1])+'\t'+str(SellPnl[-1])+'\n')
					fs.close()
				
				if len(lineList)>1:
					maxtrl=max(trlong, trl[-1])
					mintrs=min(trshort, trs[-1])
					
					if mintrs>LTPlist[-1]>maxtrl:
						trl.append(maxtrl)
						trs.append(mintrs)
					
					elif LTPlist[-1]>=mintrs:
						trl.append(maxtrl)
						trs.append(maxtrl)

					elif LTPlist[-1]<=maxtrl:
						trl.append(mintrs)
						trs.append(mintrs)					
					
					fs= open('./data/'+str(instrumenttoken)+".txt", 'a')
					if int(lineList[-1].split()[7]) != int(volumep):
						if len(mb)==0:						
							
							fs.write(str(str(datetime.datetime.now().date()).split()[0])+'\t'+str(str(datetime.datetime.now().time()).split()[0][0:5])+'\t'+str(LTPlist[-1])+'\t'+str(latestbid)+'\t'+str(latestbidquantity)+'\t'+str(latestask)+'\t'+str(latestaskquantity)+'\t'+str(volumep)+'\t'+str(trs[-1])+'\t'+str('0')+'\t'+str('0')+'\t'+str(trl[-1])+'\t'+str(buyprice[-1])+'\t'+str(buyentryorderid[-1])+'\t'+str(BuyentryQuantity[-1])+'\t'+str(BuyEntryTime[-1])+'\t'+str(buyexitorderid[-1])+'\t'+str(BuyexitQuantity[-1])+'\t'+str(sellprice[-1])+'\t'+str(sellentryorderid[-1])+'\t'+str(SellentryQuantity[-1])+'\t'+str(SellEntryTime[-1])+'\t'+str(sellexitorderid[-1])+'\t'+str(SellexitQuantity[-1])+'\t'+str(BuyPnl[-1])+'\t'+str(SellPnl[-1])+'\n')
								
						else:							
							buyprofit=float((reward/100*float(buyprice[-1]))+float(buyprice[-1]))
							sellprofit=float(float(sellprice[-1])-(reward/100*float(sellprice[-1])))
							
							#-----CALCULATE STOCKS PER MIN AND TIME DELTA
							stockprice=LTPlist[-1]
							numberofstocks=cashtotrade*leverage/stockprice
							reqminpricechange=(float(profittarget)/float(leverage))/100*float(stockprice)
							reqminpercentchange=reqminpricechange/stockprice*100
							stockspersec=numberofstocks/tradingtime
							if stockspersec<1:
								for i in range(1,tradingtime+1):
									if int(i*stockspersec)>=1:
										stocks=int(i*stockspersec)
										timedelta=int(i)
										break
								#print("cash",cashtotrade, "profittarget", profittarget, "stockprice", stockprice, "numberofstocks", numberofstocks, "expectedprofit", expectedprofit, "reqminpricechange", reqminpricechange, "reqminpercentchange", reqminpercentchange, int(i*stockspersec), "stocksper", i, "min")

							if stockspersec>=1:
								#print("cashtotrade",cashtotrade, "profittarget", profittarget, "stockprice", stockprice, "numberofstocks", numberofstocks, "expectedprofit", expectedprofit, "reqminpricechange", reqminpricechange, "reqminpercentchange", reqminpercentchange, "stockspersec", stockspersec)
								stocks=int(stockspersec)
								timedelta=1

								
							#-----------LONG ENTRY REGULAR ORDER------------------------------------------
							if epochnow<=tradeendepoch and str(Datelist[-1])==str(str(datetime.datetime.now().date()).split()[0]) and int(buyentryorderid[-1])!=1 and float(mbsmall[-1])>float(mb[-1]) and (int(time.time())-int(BuyEntryTime[-1]))>=timedelta:
								#Get cash available
								try:
									margin=xxxx.margins("equity")
									cash=float(margin['net'])
									availablecash=cash+cashtotrade-totalcash
								except Exception as cs:
									print(str(cs))								
								if availablecash>LTPlist[-1]:
									try:
										buy= xxxx.order_place('NSE', symbolname[symbollist.index(instrumenttoken)], 'BUY',quantity=stocks, price=None, product='MIS', order_type='MARKET', validity='DAY', disclosed_quantity=stocks, trigger_price=None, squareoff_value=None, stoploss_value=None, trailing_stoploss=None, variety='regular')
										#buy=999
										buyprice.append(latestask)
										buyentryorderid.append(int(buy))
										BuyentryQuantity.append(BuyentryQuantity[-1]+int(stocks))
										BuyEntryTime.append(int(time.time()))
										buyexitorderid.append('0')
										BuyexitQuantity.append('0')
										sellprice.append('1')
										sellentryorderid.append('1')
										SellentryQuantity.append('0')
										sellexitorderid.append('1')
										SellexitQuantity.append('0')															
										print("BUY LONG", instrumenttoken,symbolname[symbollist.index(instrumenttoken)], "at", latestask,"at",str(str(datetime.datetime.now().time()).split()[0][0:5]), "OrderID", buy)
										fs.write(str(str(datetime.datetime.now().date()).split()[0])+'\t'+str(str(datetime.datetime.now().time()).split()[0][0:5])+'\t'+str(LTPlist[-1])+'\t'+str(latestbid)+'\t'+str(latestbidquantity)+'\t'+str(latestask)+'\t'+str(latestaskquantity)+'\t'+str(volumep)+'\t'+str(trs[-1])+'\t'+str(mb[-1])+'\t'+str(mbsmall[-1])+'\t'+str(trl[-1])+'\t'+str(buyprice[-1])+'\t'+str(buyentryorderid[-1])+'\t'+str(BuyentryQuantity[-1])+'\t'+str(BuyEntryTime[-1])+'\t'+str(buyexitorderid[-1])+'\t'+str(BuyexitQuantity[-1])+'\t'+str(sellprice[-1])+'\t'+str(sellentryorderid[-1])+'\t'+str(SellentryQuantity[-1])+'\t'+str(SellEntryTime[-1])+'\t'+str(sellexitorderid[-1])+'\t'+str(SellexitQuantity[-1])+'\t'+str(BuyPnl[-1])+'\t'+str(SellPnl[-1])+'\n')
									except Exception as f:
										buy= xxxx.order_place('NSE', symbolname[symbollist.index(instrumenttoken)], 'BUY',quantity=stocks, price=None, product='MIS', order_type='MARKET', validity='DAY', disclosed_quantity=stocks, trigger_price=None, squareoff_value=None, stoploss_value=None, trailing_stoploss=None, variety='regular')
										#buy=999
										print(str(f), 'ERROR in LONG BUY', symbolname[symbollist.index(instrumenttoken)])
										buyprice.append(latestask)
										buyentryorderid.append(int(99999))
										BuyentryQuantity.append(BuyentryQuantity[-1]+int(stocks))
										BuyEntryTime.append(int(time.time()))
										buyexitorderid.append('0')
										BuyexitQuantity.append('0')
										sellprice.append('1')
										sellentryorderid.append('1')
										SellentryQuantity.append('0')
										sellexitorderid.append('1')
										SellexitQuantity.append('0')							
										fs.write(str(str(datetime.datetime.now().date()).split()[0])+'\t'+str(str(datetime.datetime.now().time()).split()[0][0:5])+'\t'+str(LTPlist[-1])+'\t'+str(latestbid)+'\t'+str(latestbidquantity)+'\t'+str(latestask)+'\t'+str(latestaskquantity)+'\t'+str(volumep)+'\t'+str(trs[-1])+'\t'+str(mb[-1])+'\t'+str(mbsmall[-1])+'\t'+str(trl[-1])+'\t'+str(buyprice[-1])+'\t'+str(buyentryorderid[-1])+'\t'+str(BuyentryQuantity[-1])+'\t'+str(BuyEntryTime[-1])+'\t'+str(buyexitorderid[-1])+'\t'+str(BuyexitQuantity[-1])+'\t'+str(sellprice[-1])+'\t'+str(sellentryorderid[-1])+'\t'+str(SellentryQuantity[-1])+'\t'+str(SellEntryTime[-1])+'\t'+str(sellexitorderid[-1])+'\t'+str(SellexitQuantity[-1])+'\t'+str(BuyPnl[-1])+'\t'+str(SellPnl[-1])+'\n')								
								else:
									print("Not enough cash")
									fs.write(str(str(datetime.datetime.now().date()).split()[0])+'\t'+str(str(datetime.datetime.now().time()).split()[0][0:5])+'\t'+str(LTPlist[-1])+'\t'+str(latestbid)+'\t'+str(latestbidquantity)+'\t'+str(latestask)+'\t'+str(latestaskquantity)+'\t'+str(volumep)+'\t'+str(trs[-1])+'\t'+str(mb[-1])+'\t'+str(mbsmall[-1])+'\t'+str(trl[-1])+'\t'+str(buyprice[-1])+'\t'+str(buyentryorderid[-1])+'\t'+str(BuyentryQuantity[-1])+'\t'+str(BuyEntryTime[-1])+'\t'+str(buyexitorderid[-1])+'\t'+str(BuyexitQuantity[-1])+'\t'+str(sellprice[-1])+'\t'+str(sellentryorderid[-1])+'\t'+str(SellentryQuantity[-1])+'\t'+str(SellEntryTime[-1])+'\t'+str(sellexitorderid[-1])+'\t'+str(SellexitQuantity[-1])+'\t'+str(BuyPnl[-1])+'\t'+str(SellPnl[-1])+'\n')

							#-----------LONG EXIT REGULAR ORDER------------------------------------------
							elif epochnow<=tradeendepoch and str(Datelist[-1])==str(str(datetime.datetime.now().date()).split()[0]) and int(buyentryorderid[-1])!=0 and  float(mbsmall[-1])<=float(mb[-1]) and int(sellentryorderid[-1])==1:

								try:								
									sell= xxxx.order_place('NSE', symbolname[symbollist.index(instrumenttoken)], 'SELL',quantity=BuyentryQuantity[-1], price=None, product='MIS', order_type='MARKET', validity='DAY', disclosed_quantity=BuyentryQuantity[-1], trigger_price=None, squareoff_value=None, stoploss_value=None, trailing_stoploss=None, variety='regular')							
									#sell=999
									buyprice.append(latestbid)
									buyentryorderid.append('0')
									BuyentryQuantity.append('0')
									BuyEntryTime.append('0')
									buyexitorderid.append(int(sell))
									BuyexitQuantity.append(int(BuyentryQuantity[-1]))
									sellprice.append('0')
									sellentryorderid.append('0')
									SellentryQuantity.append('0')
									sellexitorderid.append('0')
									SellexitQuantity.append('0')
									BuyPnl.append(int(int(BuyPnl[-1])+1))											
									print("EXIT LONG", instrumenttoken,symbolname[symbollist.index(instrumenttoken)], "at", latestbid, "at",str(str(datetime.datetime.now().time()).split()[0][0:5]),"OrderID", buyexitorderid[-1])
									fs.write(str(str(datetime.datetime.now().date()).split()[0])+'\t'+str(str(datetime.datetime.now().time()).split()[0][0:5])+'\t'+str(LTPlist[-1])+'\t'+str(latestbid)+'\t'+str(latestbidquantity)+'\t'+str(latestask)+'\t'+str(latestaskquantity)+'\t'+str(volumep)+'\t'+str(trs[-1])+'\t'+str(mb[-1])+'\t'+str(mbsmall[-1])+'\t'+str(trl[-1])+'\t'+str(buyprice[-1])+'\t'+str(buyentryorderid[-1])+'\t'+str(BuyentryQuantity[-1])+'\t'+str(BuyEntryTime[-1])+'\t'+str(buyexitorderid[-1])+'\t'+str(BuyexitQuantity[-1])+'\t'+str(sellprice[-1])+'\t'+str(sellentryorderid[-1])+'\t'+str(SellentryQuantity[-1])+'\t'+str(SellEntryTime[-1])+'\t'+str(sellexitorderid[-1])+'\t'+str(SellexitQuantity[-1])+'\t'+str(BuyPnl[-1])+'\t'+str(SellPnl[-1])+'\n')
								except Exception as f:
									sell= xxxx.order_place('NSE', symbolname[symbollist.index(instrumenttoken)], 'SELL',quantity=BuyentryQuantity[-1], price=None, product='MIS', order_type='MARKET', validity='DAY', disclosed_quantity=BuyentryQuantity[-1], trigger_price=None, squareoff_value=None, stoploss_value=None, trailing_stoploss=None, variety='regular')							
									#sell=999
									print(str(f), 'ERROR in LONG Exit', symbolname[symbollist.index(instrumenttoken)])
									buyprice.append(latestbid)
									buyentryorderid.append('0')
									BuyentryQuantity.append('0')
									BuyEntryTime.append('0')
									buyexitorderid.append(int(99999))
									BuyexitQuantity.append(int(BuyentryQuantity[-1]))
									sellprice.append('0')
									sellentryorderid.append('0')
									SellentryQuantity.append('0')
									sellexitorderid.append('0')
									SellexitQuantity.append('0')
									BuyPnl.append(int(int(BuyPnl[-1])+1))
									fs.write(str(str(datetime.datetime.now().date()).split()[0])+'\t'+str(str(datetime.datetime.now().time()).split()[0][0:5])+'\t'+str(LTPlist[-1])+'\t'+str(latestbid)+'\t'+str(latestbidquantity)+'\t'+str(latestask)+'\t'+str(latestaskquantity)+'\t'+str(volumep)+'\t'+str(trs[-1])+'\t'+str(mb[-1])+'\t'+str(mbsmall[-1])+'\t'+str(trl[-1])+'\t'+str(buyprice[-1])+'\t'+str(buyentryorderid[-1])+'\t'+str(BuyentryQuantity[-1])+'\t'+str(BuyEntryTime[-1])+'\t'+str(buyexitorderid[-1])+'\t'+str(BuyexitQuantity[-1])+'\t'+str(sellprice[-1])+'\t'+str(sellentryorderid[-1])+'\t'+str(SellentryQuantity[-1])+'\t'+str(SellEntryTime[-1])+'\t'+str(sellexitorderid[-1])+'\t'+str(SellexitQuantity[-1])+'\t'+str(BuyPnl[-1])+'\t'+str(SellPnl[-1])+'\n')
							

							
							#-----------SHORT ENTRY REGULAR ORDER------------------------------------------
							elif epochnow<=tradeendepoch and str(Datelist[-1])==str(str(datetime.datetime.now().date()).split()[0]) and int(sellentryorderid[-1])!=1 and float(mbsmall[-1])<float(mb[-1]) and (int(time.time())-int(SellEntryTime[-1]))>=timedelta:
								#Get cash available
								try:
									margin=xxxx.margins("equity")
									cash=float(margin['net'])
									availablecash=cash+cashtotrade-totalcash
								except Exception as cs:
									print(str(cs))								
								if availablecash>LTPlist[-1]:								
									try:								
										sell= xxxx.order_place('NSE', symbolname[symbollist.index(instrumenttoken)], 'SELL',quantity=stocks, price=None, product='MIS', order_type='MARKET', validity='DAY', disclosed_quantity=stocks, trigger_price=None, squareoff_value=None, stoploss_value=None, trailing_stoploss=None, variety='regular')
										#sell=999
										buyprice.append('1')
										buyentryorderid.append('1')
										BuyentryQuantity.append('0')
										buyexitorderid.append('1')
										BuyexitQuantity.append('0')
										sellprice.append(latestbid)
										sellentryorderid.append(int(sell))
										SellentryQuantity.append(SellentryQuantity[-1]+int(stocks))
										SellEntryTime.append(int(time.time()))
										sellexitorderid.append('0')
										SellexitQuantity.append('0')								
										print("SHORT", instrumenttoken,symbolname[symbollist.index(instrumenttoken)], "at", latestbid, "at",str(str(datetime.datetime.now().time()).split()[0][0:5]),"OrderID", sell)		
										fs.write(str(str(datetime.datetime.now().date()).split()[0])+'\t'+str(str(datetime.datetime.now().time()).split()[0][0:5])+'\t'+str(LTPlist[-1])+'\t'+str(latestbid)+'\t'+str(latestbidquantity)+'\t'+str(latestask)+'\t'+str(latestaskquantity)+'\t'+str(volumep)+'\t'+str(trs[-1])+'\t'+str(mb[-1])+'\t'+str(mbsmall[-1])+'\t'+str(trl[-1])+'\t'+str(buyprice[-1])+'\t'+str(buyentryorderid[-1])+'\t'+str(BuyentryQuantity[-1])+'\t'+str(BuyEntryTime[-1])+'\t'+str(buyexitorderid[-1])+'\t'+str(BuyexitQuantity[-1])+'\t'+str(sellprice[-1])+'\t'+str(sellentryorderid[-1])+'\t'+str(SellentryQuantity[-1])+'\t'+str(SellEntryTime[-1])+'\t'+str(sellexitorderid[-1])+'\t'+str(SellexitQuantity[-1])+'\t'+str(BuyPnl[-1])+'\t'+str(SellPnl[-1])+'\n')
									except Exception as f:
										sell= xxxx.order_place('NSE', symbolname[symbollist.index(instrumenttoken)], 'SELL',quantity=stocks, price=None, product='MIS', order_type='MARKET', validity='DAY', disclosed_quantity=stocks, trigger_price=None, squareoff_value=None, stoploss_value=None, trailing_stoploss=None, variety='regular')
										#sell=999
										print(str(f), 'ERROR in SHORT ENTRY', symbolname[symbollist.index(instrumenttoken)])
										buyprice.append('1')
										buyentryorderid.append('1')
										BuyentryQuantity.append('0')
										buyexitorderid.append('1')
										BuyexitQuantity.append('0')
										sellprice.append(latestbid)
										sellentryorderid.append(int(99999))
										SellentryQuantity.append(SellentryQuantity[-1]+int(stocks))
										SellEntryTime.append(int(time.time()))
										sellexitorderid.append('0')
										SellexitQuantity.append('0')
										fs.write(str(str(datetime.datetime.now().date()).split()[0])+'\t'+str(str(datetime.datetime.now().time()).split()[0][0:5])+'\t'+str(LTPlist[-1])+'\t'+str(latestbid)+'\t'+str(latestbidquantity)+'\t'+str(latestask)+'\t'+str(latestaskquantity)+'\t'+str(volumep)+'\t'+str(trs[-1])+'\t'+str(mb[-1])+'\t'+str(mbsmall[-1])+'\t'+str(trl[-1])+'\t'+str(buyprice[-1])+'\t'+str(buyentryorderid[-1])+'\t'+str(BuyentryQuantity[-1])+'\t'+str(BuyEntryTime[-1])+'\t'+str(buyexitorderid[-1])+'\t'+str(BuyexitQuantity[-1])+'\t'+str(sellprice[-1])+'\t'+str(sellentryorderid[-1])+'\t'+str(SellentryQuantity[-1])+'\t'+str(SellEntryTime[-1])+'\t'+str(sellexitorderid[-1])+'\t'+str(SellexitQuantity[-1])+'\t'+str(BuyPnl[-1])+'\t'+str(SellPnl[-1])+'\n')
								else:
									print("Not enough cash")										
									fs.write(str(str(datetime.datetime.now().date()).split()[0])+'\t'+str(str(datetime.datetime.now().time()).split()[0][0:5])+'\t'+str(LTPlist[-1])+'\t'+str(latestbid)+'\t'+str(latestbidquantity)+'\t'+str(latestask)+'\t'+str(latestaskquantity)+'\t'+str(volumep)+'\t'+str(trs[-1])+'\t'+str(mb[-1])+'\t'+str(mbsmall[-1])+'\t'+str(trl[-1])+'\t'+str(buyprice[-1])+'\t'+str(buyentryorderid[-1])+'\t'+str(BuyentryQuantity[-1])+'\t'+str(BuyEntryTime[-1])+'\t'+str(buyexitorderid[-1])+'\t'+str(BuyexitQuantity[-1])+'\t'+str(sellprice[-1])+'\t'+str(sellentryorderid[-1])+'\t'+str(SellentryQuantity[-1])+'\t'+str(SellEntryTime[-1])+'\t'+str(sellexitorderid[-1])+'\t'+str(SellexitQuantity[-1])+'\t'+str(BuyPnl[-1])+'\t'+str(SellPnl[-1])+'\n')

																									
							#-----------SHORT EXIT REGULAR ORDER------------------------------------------
							elif epochnow<=tradeendepoch and str(Datelist[-1])==str(str(datetime.datetime.now().date()).split()[0]) and int(sellentryorderid[-1])!=0 and float(mbsmall[-1])>=float(mb[-1]) and int(buyentryorderid[-1])==1:
								try:
									buy= xxxx.order_place('NSE', symbolname[symbollist.index(instrumenttoken)], 'BUY',quantity=SellentryQuantity[-1], price=None, product='MIS', order_type='MARKET', validity='DAY', disclosed_quantity=SellentryQuantity[-1], trigger_price=None, squareoff_value=None, stoploss_value=None, trailing_stoploss=None, variety='regular')
									#buy=999
									buyprice.append('0')
									buyentryorderid.append('0')
									BuyentryQuantity.append('0')
									buyexitorderid.append('0')
									BuyexitQuantity.append('0')
									sellprice.append(latestask)
									sellentryorderid.append('0')
									SellentryQuantity.append('0')
									SellEntryTime.append('0')
									sellexitorderid.append(int(buy))
									SellexitQuantity.append(SellentryQuantity[-1])
									SellPnl.append(int(int(SellPnl[-1])+1))	
									print("EXIT SHORT", instrumenttoken,symbolname[symbollist.index(instrumenttoken)], "at", latestask, "at",str(str(datetime.datetime.now().time()).split()[0][0:5]),"OrderID", sellexitorderid[-1])		
									fs.write(str(str(datetime.datetime.now().date()).split()[0])+'\t'+str(str(datetime.datetime.now().time()).split()[0][0:5])+'\t'+str(LTPlist[-1])+'\t'+str(latestbid)+'\t'+str(latestbidquantity)+'\t'+str(latestask)+'\t'+str(latestaskquantity)+'\t'+str(volumep)+'\t'+str(trs[-1])+'\t'+str(mb[-1])+'\t'+str(mbsmall[-1])+'\t'+str(trl[-1])+'\t'+str(buyprice[-1])+'\t'+str(buyentryorderid[-1])+'\t'+str(BuyentryQuantity[-1])+'\t'+str(BuyEntryTime[-1])+'\t'+str(buyexitorderid[-1])+'\t'+str(BuyexitQuantity[-1])+'\t'+str(sellprice[-1])+'\t'+str(sellentryorderid[-1])+'\t'+str(SellentryQuantity[-1])+'\t'+str(SellEntryTime[-1])+'\t'+str(sellexitorderid[-1])+'\t'+str(SellexitQuantity[-1])+'\t'+str(BuyPnl[-1])+'\t'+str(SellPnl[-1])+'\n')
								except Exception as f:
									buy= xxxx.order_place('NSE', symbolname[symbollist.index(instrumenttoken)], 'BUY',quantity=SellentryQuantity[-1], price=None, product='MIS', order_type='MARKET', validity='DAY', disclosed_quantity=SellentryQuantity[-1], trigger_price=None, squareoff_value=None, stoploss_value=None, trailing_stoploss=None, variety='regular')
									#buy=999
									print(str(f), 'ERROR in SHORT Exit', symbolname[symbollist.index(instrumenttoken)])
									buyprice.append('0')
									buyentryorderid.append('0')
									BuyentryQuantity.append('0')
									buyexitorderid.append('0')
									BuyexitQuantity.append('0')
									sellprice.append(latestask)
									sellentryorderid.append('0')
									SellentryQuantity.append('0')
									SellEntryTime.append('0')
									sellexitorderid.append(int(99999))
									SellexitQuantity.append(SellentryQuantity[-1])
									SellPnl.append(int(int(SellPnl[-1])+1))		
									fs.write(str(str(datetime.datetime.now().date()).split()[0])+'\t'+str(str(datetime.datetime.now().time()).split()[0][0:5])+'\t'+str(LTPlist[-1])+'\t'+str(latestbid)+'\t'+str(latestbidquantity)+'\t'+str(latestask)+'\t'+str(latestaskquantity)+'\t'+str(volumep)+'\t'+str(trs[-1])+'\t'+str(mb[-1])+'\t'+str(mbsmall[-1])+'\t'+str(trl[-1])+'\t'+str(buyprice[-1])+'\t'+str(buyentryorderid[-1])+'\t'+str(BuyentryQuantity[-1])+'\t'+str(BuyEntryTime[-1])+'\t'+str(buyexitorderid[-1])+'\t'+str(BuyexitQuantity[-1])+'\t'+str(sellprice[-1])+'\t'+str(sellentryorderid[-1])+'\t'+str(SellentryQuantity[-1])+'\t'+str(SellEntryTime[-1])+'\t'+str(sellexitorderid[-1])+'\t'+str(SellexitQuantity[-1])+'\t'+str(BuyPnl[-1])+'\t'+str(SellPnl[-1])+'\n')
							
							#--------IF Today's Date is not the last recorded date, then erase all trading history-----
							elif str(Datelist[-1])!=str(str(datetime.datetime.now().date()).split()[0]):
								print(instrumenttoken,symbolname[symbollist.index(instrumenttoken)],"Erasing previous day's trading history. Good Luck for today!!")
								fs.write(str(str(datetime.datetime.now().date()).split()[0])+'\t'+str(str(datetime.datetime.now().time()).split()[0][0:5])+'\t'+str(LTPlist[-1])+'\t'+str(latestbid)+'\t'+str(latestbidquantity)+'\t'+str(latestask)+'\t'+str(latestaskquantity)+'\t'+str(volumep)+'\t'+str(trs[-1])+'\t'+str(mb[-1])+'\t'+str(mbsmall[-1])+'\t'+str(trl[-1])+'\t'+str('0')+'\t'+str('0')+'\t'+str('0')+'\t'+str('0')+'\t'+str('0')+'\t'+str('0')+'\t'+str('0')+'\t'+str('0')+'\t'+str('0')+'\t'+str('0')+'\t'+str('0')+'\t'+str('0')+'\t'+str('0')+'\t'+str('0')+'\n')

							else:
								fs.write(str(str(datetime.datetime.now().date()).split()[0])+'\t'+str(str(datetime.datetime.now().time()).split()[0][0:5])+'\t'+str(LTPlist[-1])+'\t'+str(latestbid)+'\t'+str(latestbidquantity)+'\t'+str(latestask)+'\t'+str(latestaskquantity)+'\t'+str(volumep)+'\t'+str(trs[-1])+'\t'+str(mb[-1])+'\t'+str(mbsmall[-1])+'\t'+str(trl[-1])+'\t'+str(buyprice[-1])+'\t'+str(buyentryorderid[-1])+'\t'+str(BuyentryQuantity[-1])+'\t'+str(BuyEntryTime[-1])+'\t'+str(buyexitorderid[-1])+'\t'+str(BuyexitQuantity[-1])+'\t'+str(sellprice[-1])+'\t'+str(sellentryorderid[-1])+'\t'+str(SellentryQuantity[-1])+'\t'+str(SellEntryTime[-1])+'\t'+str(sellexitorderid[-1])+'\t'+str(SellexitQuantity[-1])+'\t'+str(BuyPnl[-1])+'\t'+str(SellPnl[-1])+'\n')
								
								
					fs.close()
							
			#time.sleep(0.5)	
				
			
			#end = time.time()
			#print("TIME:",end - start)
					

	except Exception as e:
        	print(str(e), 'ERROR', symbolname[symbollist.index(instrumenttoken)])
# Callback for successful connection.
def on_connect(ws):
	# Subscribe to a list of instrument_tokens.
	ws.subscribe(symbollist)
	# Set symbols to tick in `full` mode.
	ws.set_mode(ws.MODE_FULL, symbollist)
	print("Connected!!")	

#Get Heartbeats
def on_data(beats, ws):
	#beatnows=str(str(datetime.datetime.now().time()).split()[0][0:8])
	#print("Heart beats",beatnows)
	try:
		heartbeat=open("heartbeat.txt", 'w')
		heartbeat.write(str(int(time.time())))
		heartbeat.close()
		signalbeat=open("signal-heartbeat.txt", "r")
		restartline=signalbeat.readline()
		signalbeat.close()
		if 'restart' in restartline:
			signalbeating=open("signal-heartbeat.txt", "w")
			signalbeating.write("")
			signalbeating.close()
			print("Pressing control C")
			yyyy.close()
	except Exception as heartbeaterror:
		print("Exception in heartbeat management", str(heartbeaterror))

def on_error(errors, ws):
	print("errors:",errors)
	#yyyy.close()

def on_close(ws):
	print("closed")
		
# Assign the callbacks.
yyyy.on_tick = on_tick
yyyy.on_connect = on_connect
yyyy.on_data= on_data
yyyy.on_error= on_error
yyyy.on_close = on_close

# Infinite loop on the main thread. Nothing after this will run.
yyyy.connect()
end = time.time()

print("TIME:",end - start)
signal= open("signal-mainalgo.txt", "w")
signal.write("CLOSED")

