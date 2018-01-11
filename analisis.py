


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
	



def test():
	x = [ 100*math.sin( (2*t/100-1)*math.pi )  + 10*math.sin( (8*t/100-4)*math.pi )  +  10*math.sin( (16*t/100-8)*math.pi ) for t in range(100) ]
	y = [ random.randint(-15,15)+t for t in x ]
	w = calcEMA(y,0.3)
	w = [ t+20 for t in w]

	ema = EMA(0.3)

	z = []
	for t in y:
		z.append(ema.next(t))

	plt.plot(y)
	plt.plot(z)
	plt.plot(w)

	# Add a legend
	plt.legend()

	# Show the plot
	plt.show()



def test2():
	x = [ 100*math.sin( (2*t/100-1)*math.pi )  + 10*math.sin( (8*t/100-4)*math.pi )  +  10*math.sin( (16*t/100-8)*math.pi ) for t in range(100) ]
	y = [ random.randint(-15,15)+t for t in x ]
	w = calcSMA(y,5)
	w = [ t+20 for t in w]

	sma = SMA(y[:5])

	z = []
	for t in y[5:] :
		z.append(sma.next(t))

	plt.plot(y)
	plt.plot(z)
	plt.plot(w)

	# Add a legend
	plt.legend()

	# Show the plot
	plt.show()


test()