#!python
import numpy as np
import itertools
import time, math
import matplotlib.pyplot as plt

masterlist=[1256193, 2997505, 2661633, 4574465, 1207553, 636673, 738561, 758529, 3001089, 4454401, 261889, 415745, 1522689, 197633, 359937, 2905857, 1041153, 315393, 4343041, 3930881, 897537, 424961, 975873, 1837825, 2730497, 3834113, 2672641, 2906881, 173057, 3060993, 884737, 112129, 5215745, 3513601, 2061825, 387841, 2524673, 2889473, 3050241, 784129, 633601, 3924993, 895745, 134657, 2760193, 325121, 41729, 49409, 54273, 1510401, 1214721, 2763265, 348929, 341249, 2747905, 364545, 1270529, 377857, 2863105, 4632577, 2939649, 2977281, 4451329, 779521, 511233, 1195009, 177665, 3039233, 340481, 356865, 381697, 492033, 1076225, 593665, 2752769]

#masterlist=[6401, 1837825, 2863105, 2949633, 4574465, 3699201, 3764993, 744705, 1239809, 2760193, 593665, 697857, 3513601, 625153, 3060993, 2524673, 3812865, 1723649, 2661633, 3721473, 3695361, 3870465, 3491073, 194561, 3789569, 584449, 692481, 894209]
#symbolname=['ADANIENT', 'SYNDIBANK', 'IDFCBANK', 'NIITLTD', 'JSWENERGY', 'IBREALEST', 'TIMETECHNO', 'RICOAUTO', 'SNOWMAN', 'ALBK', 'NCC', 'PRICOL', 'DCBBANK', 'NOCIL', 'IDFC', 'ANDHRABANK', 'CENTRALBK', 'JINDALSTEL', 'JISLJALEQS', 'DISHTV', 'JKTYRE', 'EDELWEISS', 'JMFINANCIL', 'CROMPGREAV', 'HDIL', 'MRPL', 'PRAJIND', 'TINPLATE']
#symbollist=[6401, 1837825, 2863105, 2949633, 4574465, 3699201, 3764993, 744705, 1239809, 2760193, 593665, 697857, 3513601, 625153, 3060993, 2524673, 3812865, 1723649, 2661633, 3721473, 3695361, 3870465, 3491073, 194561, 3789569, 584449, 692481, 894209]
#symbolname=[1]
#symbollist=[3789569]
#symbolname=['ENGINERSIN', 'JETAIRWAYS', 'JISLJALEQS', 'JSWENERGY', 'GAIL', 'ORIENTBANK', 'RELIANCE', 'SAIL', 'JSWSTEEL', 'NHPC', 'FEDERALBNK', 'IOC', 'SOUTHBANK', 'DABUR', 'HINDPETRO', 'PETRONET', 'MARICO', 'GRASIM', 'TATAMTRDVR', 'RECLTD', 'TITAN', 'ITC', 'ZEEL', 'SYNDIBANK', 'PNB', 'POWERGRID', 'LUPIN', 'PTC', 'EXIDEIND', 'IDFC', 'TATAMOTORS', 'BHEL', 'COALINDIA', 'DCBBANK', 'KTKBANK', 'INDIACEM', 'ANDHRABANK', 'UPL', 'YESBANK', 'VEDL', 'ONGC', 'NMDC', 'TATASTEEL', 'BPCL', 'ALBK', 'AMBUJACEM', 'APOLLOTYRE', 'ARVIND', 'ASHOKLEY', 'AXISBANK', 'BANKINDIA', 'CANBK', 'HINDALCO', 'HDFCBANK', 'HEXAWARE', 'HINDZINC', 'ICICIBANK', 'IDBI', 'IDFCBANK', 'JUBLFOOD', 'LT', 'NTPC', 'ADANIPOWER', 'SBIN', 'LICHSGFIN', 'BANKBARODA', 'CIPLA', 'GRANULES', 'HDFC', 'HINDUNILVR', 'IFCI', 'KOTAKBANK', 'MOTHERSUMI', 'NCC', 'UNIONBANK']
#symbollist=[1256193, 2997505, 2661633, 4574465, 1207553, 636673, 738561, 758529, 3001089, 4454401, 261889, 415745, 1522689, 197633, 359937, 2905857, 1041153, 315393, 4343041, 3930881, 897537, 424961, 975873, 1837825, 2730497, 3834113, 2672641, 2906881, 173057, 3060993, 884737, 112129, 5215745, 3513601, 2061825, 387841, 2524673, 2889473, 3050241, 784129, 633601, 3924993, 895745, 134657, 2760193, 325121, 41729, 49409, 54273, 1510401, 1214721, 2763265, 348929, 341249, 2747905, 364545, 1270529, 377857, 2863105, 4632577, 2939649, 2977281, 4451329, 779521, 511233, 1195009, 177665, 3039233, 340481, 356865, 381697, 492033, 1076225, 593665, 2752769]
symbolname=['ORIENTBANK', 'PNB', 'INDIACEM', 'APOLLOTYRE', 'BANKINDIA', 'UNIONBANK','ITC', 'VEDL'] #['FEDERALBNK', 'ITC', 'VEDL', 'ICICIBANK', 'SBIN']
symbollist=[636673, 2730497, 387841, 41729, 1214721, 2752769, 424961, 784129]#[261889, 424961, 784129, 1270529, 779521]

cumulativetrades=[]
cumulativeprofit=[]
cumulativewinloss=[]

for instrumenttoken in symbollist:
	LTPlist=[]
	bid=[]
	ask=[]
	bidask=[]
	#bandwidth=[]
	bidquantity=[]
	askquantity=[]
	buy=[]
	short=[]
	totaltrades=[0]
	longtrades=[]
	shorttrades=[]
	longexit=[]
	shortexit=[]
	pnl=[]
	winner=[]
	losser=[]
	trl=[]
	trs=[]
	n=1000
	m=500
	dev=3
	ticksize= 0.05
	risk=0.5
	reward=0.1
				
	if instrumenttoken in masterlist:

		fr= open('./data/'+str(instrumenttoken)+".txt", 'r')

           #lineList = fr.readlines()


		for line in fr:
			if 'Timestamp' not in line:
				LTPlist.append(float(line.split()[2]))
				bid.append(float(line.split()[3]))
				ask.append(float(line.split()[5]))
				bidask.append((float(line.split()[3])+float(line.split()[5]))/2)
				#bandwidth.append(float(line.split()[10]))
				bidquantity.append(float(line.split()[4]))
				askquantity.append(float(line.split()[6]))
		       #buy.append(line.split()[11])
		       #short.append(line.split()[12])

		LTParray=np.array(LTPlist)
			
		for index, value in enumerate(LTPlist):
			trlong= float(value-(risk/100*value))
			trshort=float(value+(risk/100*value))

			if len(trl)==0 and len(trs)==0:
				trl.append(trlong)
				trs.append(trshort)
				colorlong='green'
				colorshort='red'
			elif len(trl)>0 and len(trs)>0:
				maxtrl=max(trlong, trl[-1])
				mintrs=min(trshort, trs[-1])
				
				if mintrs>value>maxtrl:
					trl.append(maxtrl)
					trs.append(mintrs)
					colorlong='green'
					colorshort='red'					
				elif value>=mintrs:
					trl.append(maxtrl)
					trs.append(maxtrl)
					colorlong='green'
					colorshort='green'
				elif value<=maxtrl:
					trl.append(mintrs)
					trs.append(mintrs)
					colorlong='red'
					colorshort='red'
		print trl, trs
		stocks=round(1000/LTPlist[-1])
			#stocks=10
		def round_nearest(x, a):
			return round(x / a) * a
		def round_down(x, a):
			return math.floor(x / a) * a

		def movingaverage(values,window):
			weigths = np.repeat(1.0, window)/window
			smas = np.convolve(values, weigths, 'valid')
			return smas # as a numpy array

		def ExpMovingAverage(values, window):
			weights = np.exp(np.linspace(-1., 0., window))
			weights /= weights.sum()
			a =  np.convolve(values, weights, mode='full')[window-1:-window+1] #[:len(values)]
			a[:window] = a[window]
			return a

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

		#def bollinger_bands(mult1,mult2, tff):
		def bollinger_bands(mult1, tff):
			#bdate=[]
			topBand=[]
			botBand=[]
			midBand=[]
			#topBand2=[]
			#botBand2=[]


			x=tff
			while x<len(LTParray)+1:
				curSMA= round(float((movingaverage(LTParray[x-tff:x], tff)[-1])), 3)
				#curSMA= round(float((movingaverage(LTParray[x-tff:x], tff)[-1])), 3)
				curSD= standard_deviation(tff, LTParray[x-tff:x])
				curSD=curSD[-1]

				TB= round(round_nearest(float(curSMA+(curSD*mult1)), ticksize), 2)
				#TB2= curSMA+(curSD*mult2)
				BB= round(round_down(float(curSMA-(curSD*mult1)), ticksize), 2)
				#BB2= curSMA-(curSD*mult2)
				#D= date[x-1]

				#bdate.append(D)
				topBand.append(TB)
				botBand.append(BB)
				midBand.append(curSMA)
				#topBand2.append(TB2)
				#botBand2.append(BB2)

				x+=1


			return topBand, botBand, midBand, tff


		tb, bb, mb, tfb= bollinger_bands(dev,n)
		tbsmall, bbsmall, mbsmall, tfsmall=bollinger_bands(dev,m)
		imp=[]
		print len(trl), len(trs), len(LTPlist)	

		xaxis=[]

		bandwidth= list((np.array(tb) - np.array(bb))/np.array(mb)*100)
		for i in range(len(bb[:-1])):
			xaxis.append(i)
		LTPlist.append(0)
		#print len(xaxis),len(LTPlist), len(bb[:-1]), len(LTPlist[n:-1]), len(bid[n-1:-1])
		print len(mb[:-1]), len(xaxis), len(mbsmall[m:-1]), len(trl[n-1:-1]), len(trs[n-1:-1])
		print symbolname[symbollist.index(instrumenttoken)]
		
		plt.scatter( xaxis,LTPlist[n:-1],marker='o', s=10, c='blue')
		plt.plot(xaxis,LTPlist[n:-1],c='blue')
		
		#for trailing stops

		plt.plot(xaxis,trl[n-1:-1],c=colorlong)
		plt.plot(xaxis,trs[n-1:-1],c=colorshort)
				
		#plt.scatter( xaxis,bid[n-1:-1],marker='o', s=0.2,c='green' )
		#plt.plot(xaxis,bid[n-1:-1],c='green')

		#plt.scatter( xaxis,ask[n-1:-1],marker='o', s=0.2,c='red')
		#plt.plot(xaxis,ask[n-1:-1],c='red')								 

		plt.scatter( xaxis,mb[:-1],marker='o', s=0.2,c='orange')
		plt.plot(xaxis,mb[:-1],c='orange')
		plt.plot(xaxis,mbsmall[n-m:-1],c='black')
		#plt.scatter( xaxis,tbsmall[n-m:-1],marker='o', s=0.2,c='black')
		#plt.plot(xaxis,tbsmall[n-m:-1],c='black')  				 

		#plt.scatter( xaxis,bbsmall[n-m:-1],marker='o', s=0.2,c='brown')
		#plt.plot(xaxis,bbsmall[n-m:-1],c='brown')  				 
			# Creates 3 Rectangles
		p1 = plt.Rectangle((0, 0), 0.1, 0.1, fc='blue')
		p2 = plt.Rectangle((0, 0), 0.1, 0.1, fc='green')
		p3 = plt.Rectangle((0, 0), 0.1, 0.1, fc='red')
		p4 = plt.Rectangle((0, 0), 0.1, 0.1, fc='black')
		p5 = plt.Rectangle((0, 0), 0.1, 0.1, fc='brown')
		p6 = plt.Rectangle((0, 0), 0.1, 0.1, fc='orange')
		p7= plt.Rectangle((0, 0), 0.1, 0.1, fc='orange')
			# Adds the legend into plot
		plt.legend((p1, p2, p3, p4, p5, p6, p7), ('LTP', 'BID', 'ASK', 'TB', 'BB', 'MB', str(symbolname[symbollist.index(instrumenttoken)])), loc='best')
		'''for j in range(len(xaxis)):
					# Code for LONG ENTRY
					#if bb[j]==bid[n-1:-1][j] and bandwidth[j]>0.15 and round(ask[n-1:-1][j]-bid[n-1:-1][j], 2)>=0.05 and bid[n-1:-1][j]!=bid[n-1:-1][totaltrades[-1]] and bid[n-1:-1][j]==LTPlist[n:-1][j]:
						if bid[n-1:-1][j]<100 and bid[n-1:-1][j]>mb[-1]  and bid[n-1:-1][j]==LTPlist[n:-1][j]:  	 
 	 totaltrades.append(j)
 			 longtrades.append(j)
 			 plt.annotate(str('BUY'+str(askquantity[n-1:-1][j])), xy=(xaxis[j], bid[n-1:-1][j]), xytext=(-20,20), 
 				 textcoords='offset points',size=10, ha='center', va='bottom',
 					 bbox=dict(boxstyle='round,pad=0.2', fc='green', alpha=1),
 					 arrowprops=dict(arrowstyle='->', connectionstyle='arc3,rad=0.5', 
 								 color='green'))
 		 #Code for SHORT ENTRY
 		 #if ask[n-1:-1][j]==tb[j] and bandwidth[j]>0.15 and round(ask[n-1:-1][j]-bid[n-1:-1][j], 2)>=0.05 and ask[n-1:-1][j]!=ask[n-1:-1][totaltrades[-1]] and ask[n-1:-1][j]==LTPlist[n:-1][j]:
 		 if ask[n-1:-1][j]<100 and ask[n-1:-1][j]<mb[-1]  and ask[n-1:-1][j]==LTPlist[n:-1][j]:
 					
 	 totaltrades.append(j)
 			 shorttrades.append(j)
 			 plt.annotate(str('SHORT'+str(bidquantity[n-1:-1][j])), xy=(xaxis[j], ask[n-1:-1][j]), xytext=(-20,20), 
 				 textcoords='offset points',size=10, ha='center', va='bottom',
 					 bbox=dict(boxstyle='round,pad=0.2', fc='red', alpha=1),
 					 arrowprops=dict(arrowstyle='->', connectionstyle='arc3,rad=0.5', 
 								 color='green'))
 					 
 		 #CODE for LONG EXIT
 		 for entries in longtrades:
 			 profit=round(round_nearest((reward/100*bid[n-1:-1][entries])+bid[n-1:-1][entries], ticksize), 2)
 			 loss=round(round_down(bid[n-1:-1][entries]-(risk/100*bid[n-1:-1][entries]), ticksize), 2)
 			 if j>entries and entries not in longexit and ask[n-1:-1][j]>=profit and ask[n-1:-1][j]==LTPlist[n:-1][j]:
 				 longexit.append(entries)
 				 winner.append(entries)
 				 pnl.append(stocks*round((ask[n-1:-1][j]-bid[n-1:-1][entries]), 2))
 				 print "Profit for long entry at",bid[n-1:-1][entries],"and exit at",ask[n-1:-1][j]
 			 elif j>entries and entries not in longexit and loss>=ask[n-1:-1][j] and ask[n-1:-1][j]==LTPlist[n:-1][j]:
 				 longexit.append(entries)
 				 losser.append(entries)
 				 pnl.append(stocks*round((ask[n-1:-1][j]-bid[n-1:-1][entries]), 2))
 				 print "Loss for long entry at",bid[n-1:-1][entries],"and exit at",ask[n-1:-1][j]
 		 

 		 #CODE for SHORT EXIT
 		 for entries in shorttrades:
 			 profit=round(round_down(ask[n-1:-1][entries]-(reward/100*ask[n-1:-1][entries]), ticksize), 2)
 			 loss=round(round_nearest(ask[n-1:-1][entries]+(risk/100*ask[n-1:-1][entries]), ticksize), 2)
 			 if j>entries and entries not in shortexit and profit>=bid[n-1:-1][j] and bid[n-1:-1][j]==LTPlist[n:-1][j]:
 				 shortexit.append(entries)
 				 winner.append(entries)
 				 pnl.append(stocks*round((ask[n-1:-1][entries]-bid[n-1:-1][j]), 2))
 				 print "Profit for short entry at",ask[n-1:-1][entries],"and exit at",bid[n-1:-1][j]
 			 elif j>entries and entries not in shortexit and bid[n-1:-1][j]>=loss and bid[n-1:-1][j]==LTPlist[n:-1][j]:
 				 shortexit.append(entries)
 				 losser.append(entries)
 				 pnl.append(stocks*round((ask[n-1:-1][entries]-bid[n-1:-1][j]), 2))
 				 print "Loss for short entry at",ask[n-1:-1][entries],"and exit at",bid[n-1:-1][j]  					 
 		 


 print("TOTAL PROFIT:",pnl, round(sum(pnl), 2))
 if len(losser) !=0:
 		 print("Win:Loss ratio:", round((float(len(winner))/float(len(losser))), 2))
 		 cumulativewinloss.append(round((float(len(winner))/float(len(losser))), 2))					 
 print("Opportunities in",instrumenttoken,len(totaltrades)-1)

 cumulativeprofit.append(round(sum(pnl), 2))
 cumulativetrades.append(len(totaltrades)-1)

 print"--------------------------------------"
 print("Total Opportunities:",sum(cumulativetrades))
 print("Total Profit:",sum(cumulativeprofit))
 if len(cumulativewinloss) !=0:
 		 print("Average win/loss ratio:", sum(cumulativewinloss)/len(cumulativewinloss)) 
 print"--------------------------------------"'''
		try:
			plt.axis([0, len(xaxis), min(bb), max(tb)])
			plt.show()
		except Exception as e:
			print "Exception"
	else:
		continue
