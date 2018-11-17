# THIS VERSION IS FOR PYTHON 2 #
import urllib2
import time
import datetime
import numpy as np
import pylab
import time
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import matplotlib.dates as mdates
from matplotlib.finance import candlestick
import matplotlib.animation as animation
import matplotlib
import requests
import csv

#------------------------------------------Fetch data from Tradable security list and save it as NSE.csv----------------
api_key="xxxx"
foNSE= open('NSE.csv', 'w')
url= "https://api.xxxx.xxxx/instruments/NSE?api_key="+api_key
data = urllib2.urlopen(url).read()
foNSE.write(data)
foNSE.close()

#----------------------------------------- Open the csv file and make necessary lists-------------------
fo =open('NSE.csv')
reader= csv.reader(fo)
data=list(reader)


eachStock=[]
selected_stocks=[]
instrument_token=[]
selected_instrument_token=[]
exchange_token=[]
selected_exchange_token=[]
for i in data:
	if 'instrument_token' not in i[0] and "-" not in i[2] and  i[10] == "NSE":
		eachStock.append(str(i[2])+".ns")
		instrument_token.append(str(i[0]))
		exchange_token.append(str(i[1]))




blacklisted=['ARSINFRA.ns','ANANTRAJ.ns','MANAPPURAM.ns', 'APTECHT.ns','UGARSUGAR.ns','UJAAS.ns', 'MOREPENLAB.ns', 'PIPAVAVDOC.ns', 
	     'JAICORPLTD.ns', 'MARKSANS.ns', 'SHARONBIO.ns', 'MANINFRA.ns', 'MIC.ns','SREINFRA.ns','GENUSPOWER.ns','TRIVENI.ns',
	     'DCW.ns', 'MERCATOR.ns']


fo = open("stockscreener.txt", "a")
fo.write('Stock'+'\t'+'AveragePrice'+'\t'+'LTP'+'\t'+'AverageATR'+'\t'+'AverageATRPercent'+'\t'+'AverageVolume'+'\t'+'\n')
timeframedata= '2m'
timewidth=float(.0005)
SqueezePeriod=180
if timeframedata[-1]=='y':
	strpdate2numformat='%Y%m%d'
	i=86400
elif timeframedata[-1]=='d':
	strpdate2numformat= '%Y-%m-%d %H:%M:%S'
	i=60
elif timeframedata[-1]=='m':
	strpdate2numformat= '%Y%m%d'
	i=86400
print "hello"

# --------------------------------------Defining RSI------- Set 'n'------------ 
def rsiFunc(prices, n=14):
    deltas = np.diff(prices)
    seed = deltas[:n+1]
    
    up = seed[seed>=0].sum()/n
    down = -seed[seed<0].sum()/n
    rs = up/down
    rsi = np.zeros_like(prices)
    
    rsi[:n] = 100. - 100./(1.+rs)
    
	
    for i in range(n, len(prices)):
        delta = deltas[i-1] # cause the diff is 1 shorter

        if delta>0:
            upval = delta
            downval = 0.
        else:
            upval = 0.
            downval = -delta

        up = (up*(n-1) + upval)/n
        down = (down*(n-1) + downval)/n

        rs = up/down
        rsi[i] = 100. - 100./(1.+rs)

    return rsi
#------------------------------------- Defining Simple MOVING AVERAGE----------------------------
def movingaverage(values,window):
    weigths = np.repeat(1.0, window)/window
    smas = np.convolve(values, weigths, 'valid')
    return smas # as a numpy array
    
#-----------------------------------------------Defining Exponential Moving Average------------------
def ExpMovingAverage(values, window):
    weights = np.exp(np.linspace(-1., 0., window))
    weights /= weights.sum()
    a =  np.convolve(values, weights, mode='full')[window-1:-window+1] #[:len(values)]
    
    
    a[:window] = a[window]
    
    return a
   
#-----------------------------------------------Defining MACD---------------------------------------
def computeMACD(x, slow=26, fast=12):
    """
    compute the MACD (Moving Average Convergence/Divergence) using a fast and slow exponential moving avg'
    return value is emaslow, emafast, macd (emafast - emaslow) which are len(x) arrays
   MACD LINE= 12EMA- 26EMA
   Signal LIne= 9EMA of the MACD LINE
   Histogram= MACD LINE-SIGNAL Line
   
    """
    emaslow = ExpMovingAverage(x, slow)
    emafast = ExpMovingAverage(x, fast)
    #print len(emaslow), len(emafast), len(emafast[slow-fast:] - emaslow)
    
    return emaslow, emafast, emafast[slow-fast:]-emaslow #


		
#--------------------Start of the Pulling Data live from API--------------------
#def graphData(stock,MA0,MA1,MA2):
    #fig.clf()
for stock in eachStock:
    '''
        Use this to dynamically pull a stock:
		q - Stock symbol
		x - Stock exchange symbol on which stock is traded (ex: NASD)
		i - Interval size in seconds (86400 = 1 day intervals)
		p - Period. (A number followed by a "d" or "Y", eg. Days or years. Ex: 40Y = 40 years.)
		f - What data do you want? d (date - timestamp/interval, c - close, v - volume, etc...) Note: Column order may not match what you specify here
		df - ??
		auto - ??
		ei - ??
		ts - Starting timestamp (Unix format). If blank, it uses today.
    '''
    try:
        #print 'Currently Pulling',stock
        #print str(datetime.datetime.fromtimestamp(int(time.time())).strftime('%Y-%m-%d %H:%M:%S'))
        urlToVisit = 'https://www.google.com/finance/getprices?q='+stock+'&x=NSE&i='+i+'&p='+timeframe+'&f=d,c,h,l,o'
		#https://www.google.com/finance/getprices?q=.NSEI&x=NSE&i=60&p=5d&f=d,c,o,h,l&df=cpct&auto=1&ts=1266701290218
		
		#urlToVisit = 'http://chartapi.finance.yahoo.com/instrument/1.0/'+stock+'/chartdata;type=quote;range='+timeframedata+'/csv'
		#http://chartapi.finance.yahoo.com/instrument/1.0/tsla/chartdata;type=quote;range=1d/csv
        stockFile =[]
        try:
            sourceCode = urllib2.urlopen(urlToVisit).read()
            splitSource = sourceCode.split('\n')
            for eachLine in splitSource:
                splitLine = eachLine.split(',')
		if timeframedata[-1]=='y':
			if len(splitLine)==6:
                    		if 'values' not in eachLine and 'labels' not in eachLine:
                        		stockFile.append(eachLine)
		elif timeframedata[-1]=='d':
			fixMe= splitLine[0]
              		if len(splitLine)==6:
                   		if 'values' not in eachLine and 'labels' not in eachLine:
		    			fixed= eachLine.replace(fixMe, str(datetime.datetime.fromtimestamp(int(fixMe)).strftime(strpdate2numformat)))
                       			stockFile.append(fixed)
			
		elif timeframedata[-1]=='m':
			fixMe= splitLine[0]
              		if len(splitLine)==6:
                   		if 'values' not in eachLine and 'labels' not in eachLine:
		    			fixed= eachLine.replace(fixMe, str(datetime.datetime.fromtimestamp(int(fixMe)).strftime(strpdate2numformat)))
                       			stockFile.append(fixed)			
        except Exception, e:
            print str(e), 'failed to organize pulled data.'
    except Exception,e:
        print str(e), 'failed to pull pricing data'
	
#----------------------------------END of pulling Data----------------------------------
    try:   
        date, closep, highp, lowp, openp, volume = np.loadtxt(stockFile,delimiter=',', unpack=True,
                                                              converters={ 0: mdates.strpdate2num(strpdate2numformat)})
        x = 0
        y = len(date)
        newAr = []
        while x < y:
            appendLine = date[x],openp[x],closep[x],highp[x],lowp[x],volume[x]
	    
            newAr.append(appendLine)
            x+=1
	   
	
#---------------------------------Calculation for Simple Moving Average----graphData(stock,10,50) has 
#-----------------------------------the two values for MA1, MA2-------------------           
	
        
	Av1 = movingaverage(closep, 5)
	Av2 = movingaverage(closep, 100)
	

        



	
#--------------------------BOLLINGER BANDS-----------

	def standard_deviation(tf, prices):
		sd=[]
		sddate=[]
		x=tf
		while x<= len(prices):
			array2consider= prices[x-tf:x]
			standev= array2consider.std()
			sd.append(standev)
			sddate.append(date[x])
			x+=1
		return sddate, sd
		
	def bollinger_bands(mult1,mult2, tff):
		bdate=[]
		topBand=[]
		botBand=[]
		midBand=[]
		topBand2=[]
		botBand2=[]
		
	
		x=tff
		while x<len(date)+1:
			curSMA= movingaverage(closep[x-tff:x], tff)[-1]
			d, curSD= standard_deviation(tff, closep[x-tff:x])
			
			curSD=curSD[-1]
			
			TB= curSMA+(curSD*mult1)
			TB2= curSMA+(curSD*mult2)
			BB= curSMA-(curSD*mult1)
			BB2= curSMA-(curSD*mult2)
			D= date[x-1]
			
			bdate.append(D)
			topBand.append(TB)
			botBand.append(BB)
			midBand.append(curSMA)
			topBand2.append(TB2)
			botBand2.append(BB2)
			
			x+=1
		
		return bdate, topBand, botBand, midBand,topBand2, botBand2, tff
		
	d, tb, bb, mb, tb2, bb2, tfb= bollinger_bands(2,1,20)
	
	

#----------------------------CHAIKIN MONEY FLOW:----------------------

	def CHMoF(d,c,h,l,o,v,tfff):
		CHMF=[]
		MFMs=[]
		MFVs=[]
		x=0
	
		while x<len(d):
			#PeriodVolume=0
			#volRange=v[x-tfff:x]
			
			#for eachVol in volRange:
				#PeriodVolume += eachVol
			
			MFM= ((c[x]-l[x])-(h[x]-c[x]))/(h[x]-l[x]) if (h[x]-l[x]) !=0 else 0.00
			PeriodVolumes=v[x]
			MFV= MFM*(v[x])
			MFMs.append(MFM)
			MFVs.append(MFV)
			
			
			x+=1
			
		y= tfff
		while y<len(MFVs)+1:
			PeriodVolume=0
			volRange=v[y-tfff:y]
			
			for eachVol in volRange:
				PeriodVolume += eachVol
			consider= MFVs[y-tfff:y]
			tfffsMFV= 0
		
			for eachMFV in consider:
				tfffsMFV += eachMFV
			tfffsCMF= tfffsMFV/PeriodVolume
			CHMF.append(tfffsCMF)
			#print PeriodVolume
			y+=1
		
		return date[tfff-1:], CHMF
	cmfDate, cmfY=CHMoF(date, closep, highp, lowp, openp, volume, 20)

	
		

#----------------------------------Calculation for RSI---------------------------------
        rsi = rsiFunc(closep)

#------------------------------------------Calculation for EMA--------------
	
        #nslow = 26
        #nfast = 12
        #nema = 9
        #emaslow, emafast, macd = computeMACD(closep)
        #ema9 = ExpMovingAverage(macd, nema)
	

	
	
#--------------------------------------------ADX-------------------
	def TR(d, c, h, l, o, yc):
		x = h-l
		y=abs(h-yc)
		z=abs(l-yc)
	
		if y <= x >=z:
			TR=x
		elif x <= y >= z:
			TR=y
		elif x <= z >=y:
			TR=z
		return d, TR	
	
	def DM(d, o, h, l, c, yo, yh, yl, yc):
		moveUp= h-yh
		moveDown= yl-l
	
		if 0<moveUp>moveDown:
			PDM=moveUp
		else:
			PDM=0
		if 0<moveDown>moveUp:
			NDM=moveDown
		else:
			NDM=0
		return d, PDM, NDM
	ADXlist=[]
	
	def CalcDIs():
		x= 1
		TRDates=[]
		TrueRanges=[]
		PosDMs=[]
		NegDMs=[]
	
		while x<len(date):
			
			TRDate,TrueRange= TR(date[x],closep[x],highp[x],lowp[x],openp[x],closep[x-1])
			TRDates.append(TRDate)
			TrueRanges.append(TrueRange)
		
			DMdate, PosDM, NegDM= DM(date[x],openp[x],highp[x],lowp[x],closep[x],openp[x-1],highp[x-1], lowp[x-1], closep[x-1])
			PosDMs.append(PosDM)
			NegDMs.append(NegDM)
			x+=1
		n=5
		expPosDM= ExpMovingAverage(PosDMs,n)
		expNegDM= ExpMovingAverage(NegDMs,n)
		ATR= ExpMovingAverage(TrueRanges,n)
		ATR=ATR.tolist()
		AverageATR=round((sum(ATR[n:])/len(ATR[n:])),2)
		
		AverageVolume= int(sum(volume)/len(volume))
		AveragePrice= int(sum(closep)/len(closep))
		AverageATRPercent= round((AverageATR/float(AveragePrice)*100),2)
		LTP= float(closep[-1:])
		highlowlist=[]
		for i, j in enumerate(closep):
			highlowlist.append(float((highp[i]-lowp[i])/openp[i]*100)/2)
		AverageRangePercent=sum(highlowlist)/len(highlowlist)
		
		if 50<AveragePrice<110 and AverageVolume>1000000 and 1.5<AverageRangePercent<100:
			if stock not in blacklisted:
				print stock[:-3], "Average Close Price: ", AveragePrice, "LTP: ", LTP
				print "Average ATR: ", AverageATR, 'AverageATRPercent: ', AverageATRPercent, "Average Volume: ", AverageVolume, "AverageRangePercent", AverageRangePercent
				fo.write(str(stock[:-3])+'\t\t'+str(AveragePrice)+'\t'+str(LTP)+'\t'+str(AverageATR)+'\t'+str(AverageATRPercent)+'\t'+str(AverageVolume)+'\t'+'\n')
				selected_stocks.append(stock[:-3])
				selected_instrument_token.append(instrument_token[eachStock.index(stock)])
				selected_exchange_token.append(exchange_token[eachStock.index(stock)])
		
		xx=0
		PDIs=[]
		NDIs=[]
		while xx< len(ATR):
			
			PDI=100*(expPosDM[xx]/ATR[xx])
			PDIs.append(PDI)
			NDI=100*(expNegDM[xx]/ATR[xx])
			NDIs.append(NDI)
			xx+=1
			
		return PDIs, NDIs
	
	def ADX(tr):
		PositiveDI,NegativeDI=CalcDIs()
		
		xxx=0
		DXs= []
		 
		while xxx<len(PositiveDI):
			
			DX=100*((abs(PositiveDI[xxx]-NegativeDI[xxx])/(PositiveDI[xxx]+NegativeDI[xxx])))
			
			DXs.append(DX)
			xxx+=1
		
		ADXX=ExpMovingAverage(DXs, tr)
		return ADXX
	ADT=ADX(14)
	


   	
    except Exception,e:
        print 'main loop',str(e)
		

#print len(eachStock), eachStock
print len(selected_stocks), selected_stocks
print len(selected_instrument_token), 
print('[%s]' % ', '.join(map(str, selected_instrument_token)))

