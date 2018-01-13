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

def sim(pri, fiat, fee, a, mins, lbuy, lsell):
    ema = EMA(a)
    dev = Ratio( [pri[0]]*mins )
    ofiat, cryp, sells, buys, fees = fiat, 0, 0, 0, 0
    for p in pri:
        e = ema.next(p)
        d = dev.next(e)
        if d>lbuy and fiat>0 :
            fees += fiat*fee
            fiat -= fiat*fee
            cryp += fiat/p
            fiat = 0
            buys += 1
        elif d<lsell and cryp>0 :
            fiat = cryp*p
            cryp = 0
            fees += fiat*fee
            fiat -= fiat*fee
            sells += 1
    if cryp>0:
        fiat = cryp*pri[-1]
        cryp = 0
        fees += fiat*fee
        fiat -= fiat*fee
        sells += 1
    gain = (fiat-ofiat)/ofiat
    return gain

def simugraph(prices, usd, fee, alpha, minutes, limbuy, limsell):
    ema = EMA(alpha)
    ema_sig = []
    por = Ratio( [prices[0]]*minutes )
    fiat = usd
    crypto = 0
    sells = 0
    buys = 0
    fees = 0

    for p in prices:
        e = ema.next(p)
        ema_sig.append(e)
        d = por.next(e)
        if d>limbuy :
            if fiat>0 :
                fiat *= 1-fee
                fees += fiat*fee
                crypto += fiat/p
                fiat = 0
                buys += 1
        elif d<limsell :
            if crypto>0 :
                fiat = crypto*p
                crypto = 0
                fees += fiat*fee
                fiat *= 1-fee
                sells += 1

    if crypto>0:
        fiat = crypto * prices[-1]
        crypto = 0
        fees += fiat * fee
        fiat *= 1 - fee
        sells += 1

    gain = (fiat-usd)/usd

    rep = ''
    rep += 'original money: ' + str(usd) + '\n'
    rep += 'final money: ' + str(fiat) + '\n'
    rep += 'diference: '+ str(fiat-usd )+ '\n'
    rep += 'percentage gain: ' +  str((fiat-usd)/usd*100) + ' % \n'
    rep += 'buys: ' + str(buys) + '\n'
    rep += 'sells: ' + str(sells) + '\n'
    rep += 'fees: ' +str(fees) + '\n'
    rep += 'fees percentage ' + str( fees/fiat ) + '\n'

    print(rep)

    plt.plot(prices)
    plt.plot(ema_sig)
    plt.show()

    return gain


def born():
    gen = [0,0,0,0]
    gen[0] = random.random()
    gen[1] = random.randint(1,60*24)
    gen[2] = random.random()
    gen[3] = -random.random()
    return gen

def mutate(gen):
    gen = gen[:]
    for ale in range(len(gen)):
        mod = random.randint(0,1)
        if mod==0 :
            continue
        gen[ale] += gen[ale]/2 - random.randint(0,1)*gen[ale]
        nvo = born()
        if ale==0:
            if gen[ale]<0 or gen[ale]>1:
                gen[ale] = nvo[ale]
        elif ale==1:
            gen[ale] = int(gen[ale])
            if gen[ale]<0:
                gen[ale] = nvo[ale]
        elif ale==2:
            if gen[ale]<0 :
                gen[ale] = nvo[ale]
        elif ale==3:
            if gen[ale]>0 :
                gen[ale] = nvo[ale]
    return gen



    return gen

def reproduce(g1,g2):
    g = [0,0,0,0]
    for i in range( len(g) ):
        g[i] = g1[i] if random.randrange(2)==0 else g2[i] 
    return g

params = []

def fitness(gen):
    p = params + gen
    return sim(*p)

def evolution(pri, fiat, fee, n):
    global params
    params = [pri,fiat,fee]
    pop = [ born() for i in range(n) ]
    for i in range(500):
        for j in range(n//10):
            ind = random.randrange(n)
            pop.append( mutate(pop[ind]) )
            pop.append( born() )
            pop.append( born() )
            pop.append( born() )
            pop.append( born() )
            pop.append( born() )
            
            a = random.randrange(n)
            b = random.randrange(n)
            pop.append( reproduce(pop[a],pop[b]) )
        uniq = set()
        for e in pop:
            uniq.add( tuple(e) )
        pop = [ list(e) for e in uniq]
        pop = sorted(pop, key=fitness, reverse=True)
        if len(pop)>=n:
            pop = pop[:n]
        print(i, fitness(pop[0]) )
    return pop





def genprice():
    x = [100 * math.sin((4 * t / 1000 - 2) * math.pi) + 10 * math.sin((16 * t / 1000 - 8) * math.pi) for t in range(1000)]
    y = [random.randint(-30, 30) + t + 1000 for t in x]
    return y

def test3():
    x = [100 * math.sin((4 * t / 100 - 2) * math.pi) + 10 * math.sin((16 * t / 100 - 8) * math.pi) for t in range(100)]
    y = [random.randint(-15, 15) + t + 200 for t in x]

    y = genprice()
    simugraph(y,100,0.0001,0.3,80,0.05,-0.05)

def test():
	x = [ 100*math.sin( (4*t/100-2)*math.pi )   +  10*math.sin( (16*t/100-8)*math.pi ) for t in range(100) ]
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

def test4():
    prices = genprice()
    params = [prices, 100, 0.0001]
    pop_n = 500
    par = params + [pop_n]
    pop = evolution( *par )
    p = pop[0]
    print(p)
    par = params + p
    simugraph( *par )




test4()

