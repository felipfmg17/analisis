import matplotlib.pyplot as plt
import math
import random

class EMA:
	def __init__(self,a):
		self.a=a
		self.s=None

	def next(self,v):
		s,a = self.s, self.a
		self.s = v if s==None else a*v +(1-a)*s
		return self.s

class SMA:
	def __init__(self,vals):
		self.n = len(vals)
		self.vals = vals[:]
		self.ind = 0
		self.s = sum(vals)/len(vals)

	def next(self,v):
		vals,n,ind = self.vals,self.n,self.ind
		self.s = self.s - vals[ind]/n + v/n
		vals[ind] = v
		self.ind = (ind+1)%n
		return self.s

class Ratio:
	def __init__(self,vals):
		self.n = len(vals)
		self.vals = vals[:]
		self.ind = 0

	def next(self,v):
		vals,n,ind = self.vals,self.n,self.ind
		s = (v-vals[ind])/vals[ind]
		vals[ind] = v
		self.ind = (ind+1)%n
		return s

def calcSMA(vals,n):
	series = []
	s = 0
	for i in range(n):
		s += vals[i]
	s /= n
	series.append(s)
	for i in range(n,len(vals)):
		s -= vals[i-n]/n
		s += vals[i]/n
		series.append(s)
	return series

def calcEMA(vals,a):
	series = [vals[0]]
	for i in range(1,len(vals)):
		s = series[-1]*(1-a) + vals[i]*a
		series.append(s)
	return series
	

def simu(prices, usd, alpha, minutes, limbuy, limsell, fee):
    ema = EMA(alpha)
    por = Ratio( [0]*minutes )

    fiat = usd
    crypto = 0
    trans = 0
    fees = 0

    for p in prices:
        e = ema.next(p)
        d = por.next(e)
        if d>limbuy :
            if fiat>0 :
                fiat *= 1-fee
                fees += fiat*fee
                crypto += fiat/p
                fiat = 0
                trans += 1
        elif d<limsell :
            if crypto>0 :
                fiat = crypto*p
                crypto = 0
                fees += fiat*fee
                fiat *= 1-fee
                trans += 1





def test():
	x = [ 100*math.sin( (2*t/100-1)*math.pi )  + 10*math.sin( (8*t/100-4)*math.pi )  +  10*math.sin( (16*t/100-8)*math.pi ) for t in range(100) ]
	y = [ random.randint(-15,15)+t+200 for t in x ]

	ema = EMA(0.3)

	z = []
	for t in y:
		z.append(ema.next(t))


	rat = Ratio(z[:10])
	ema_rat = []

	for t in z[10:]:
		ema_rat.append(rat.next(t)*100)


	print(ema_rat)

	plt.plot(y)
	plt.plot(z)
	plt.plot(ema_rat)
	


	# Show the plot
	plt.show()

def test2():
	y = [ 100*math.sin( (2*t/100-1)*math.pi )  + 10*math.sin( (8*t/100-4)*math.pi )  +  10*math.sin( (16*t/100-8)*math.pi ) for t in range(100) ]
	x = [ random.randint(-15,15)+t for t in y ]

	sma = SMA(x[:5])
	sma_sig = []
	for t in x:
		sma_sig.append(t)


	rat = Ratio(sma_sig[:10])
	sma_rat = []
	for t in sma_sig[10:]:
		sma_rat.append(rat.next(t)*100)


	plt.plot(x)
	plt.plot(sma_sig)
	plt.plot(sma_rat)
	

	# Add a legend
	plt.legend()

	# Show the plot
	plt.show()

test()