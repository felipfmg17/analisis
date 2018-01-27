

def simugraph(prices, usd, fee, alpha, minutes, limbuy):
    limsell = -limbuy
    ema = EMA(alpha)
    ema_sig = []
    por = Ratio( [prices[0]]*minutes )
    fiat = usd
    crypto = 0
    sells = 0
    buys = 0
    fees = 0

    for i in range(len(prices)):
        p = prices[i]
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
                print('Buying, price',p,i)
        elif d<limsell :
            if crypto>0 :
                fiat = crypto*p
                crypto = 0
                fees += fiat*fee
                fiat *= 1-fee
                sells += 1
                print('Selling, price', p, i)

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
    gen = [0,0,0]
    gen[0] = random.uniform(0.0,1)
    gen[1] = random.randint(1,10000)
    gen[2] = random.uniform(0.0,1)
    return gen

params = []

def fitness(gen):
    p = params + gen
    return sim(*p)

def valid(v,ale):
    b = born()
    if ale==0 and (v<0 or v>1):
        v = b[ale]
    elif ale==1 and (v<1 or v>10000):
        v = b[ale]
    elif ale==2 and v<1:
        v = b[ale]
    return v

#difs = [0.0005,0.001,0.002,0.004,0.008,0.016,0.032,0.064]
#difs = list(range(0.001,0.002,0.0001)) + list(range(0.01,0.02,0.001))
difs = [ v/1000 for v in range(10)] + [ v/100 for v in range(10) ]
idifs = [ v for v in range(10)] + [v for v in range(10,100,10) ]
difs += [-v for v in difs]
idifs += [-v for v in idifs]
def move(gen):
    bgen = gen[:]
    bper = fitness(bgen)
    for i in range(len(gen)):
        d = difs if i != 1 else idifs
        for v in d:
            cgen = gen[:]
            cgen[i] = valid(cgen[i]+v,i)
            cper = fitness(cgen)
            if  cper>bper:
                bgen = cgen
                bper = cper
    return bgen,bper

def evolve(pri, fiat, fee):
    global params
    params = [pri, fiat, fee]
    gen = born()
    per = fitness(gen)
    bgen,bper = gen,per
    for i in range(1000):
        cgen,cper = move(gen)
        if cper==per:
            if cper>bper:
                bgen = cgen
                bper = cper
            gen = born()
            per = fitness(gen)
        elif cper>per:
            gen,per = cgen,cper
        #print(i, bgen, bper)
    print(bper)
    return bgen

def train(ini,fin,sec):
    fiat, fee = 100, 0.0001
    cini = ini
    wprices = loadPrices(ini,fin)
    while cini<fin:
        prices = loadPrices(cini,cini+sec)
        cini += sec
        params = [prices,fiat,fee]
        gen = evolve(*params)
        params[0] = wprices
        par = params + gen
        gain = sim(*par)
        print(gen, gain)

def htrain(prices):
    fiat, fee = 100, 0.0001
    params = [prices, fiat, fee]
    p = evolve(*params)
    print(p)
    par = params + p
    simugraph(*par)

def loadPrices(d0,d1):
    db = pymysql.connect('localhost','root','root','crypto_prices')
    sql = """ SELECT  a.price as Price
FROM coin_price as a
JOIN currency_pair as b
ON a.currency_pair_id = b.id
JOIN exchange as c
ON a.exchange_id = c.id
WHERE c.name = \"bitso\"
AND b.name = \"xrp_mxn\" """
    sql += ' AND a.date_time_sec > '  + str(d0)
    sql += ' AND a.date_time_sec < '  + str(d1)
    cursor = db.cursor()
    cursor.execute(sql)

    lines = cursor.fetchall()
    prices = [ e[0] for e in lines ]
    return prices;




# ini 44.39
# fin 40.45
# def move(gen):
#     i = random.randrange(4)
#     difs = [0.0005,0.001,0.002,0.004,0.008,0.016,0.032,0.064]
#     idifs = [1,2,4,8]
#     muls = [born(),gen]
#     d = difs if i!=1 else idifs
#     for v in d:
#         cgen = gen[:]
#         cgen[i] = valid(cgen[i]+v,i)
#         muls.append(cgen)
#         cgen = gen[:]
#         cgen[i] = valid(cgen[i]-v,i)
#         muls.append(cgen)
#     gen = max(muls,key=fitness)
#     return gen
#
# def evolve(pri, fiat, fee):
#     n = 100  # population size
#     global params
#     params = [pri,fiat,fee]
#     pop = [ born() for i in range(n) ]
#     for i in range(50):
#         for j in range(n):
#             pop[j] = move(pop[j])
#         pop = sorted(pop,key=fitness,reverse=True)
#         print(i, pop[0], fitness(pop[0]) )
#     return pop[0]

def mutate(gen):
    gen = gen[:]
    ale = random.randrange(4)
    nvo = born()
    if ale == 0:
        # gen[ale] += 0.01 if random.randrange(2)==0 else -0.01
        gen[ale] +=  gen[ale ] /2 - random.randrange(2 ) *gen[ale]
        # gen[ale] += random.random() if random.randrange(2)==0 else -random.random()
        if gen[ale] < 0 or gen[ale] > 1:
            gen[ale] = nvo[ale]
    elif ale == 1:
        gen[ale] += gen[ale] // 2 - random.randrange(2) * gen[ale]
        if gen[ale] < 1:
            gen[ale] = nvo[ale]
    elif ale == 2:
        # gen[ale] += 0.01 if random.randrange(2) == 0 else -0.01
        gen[ale] += gen[ale] / 2 - random.randrange(2) * gen[ale]
        # gen[ale] += random.random() if random.randrange(2) == 0 else -random.random()
        if gen[ale] < 0:
            gen[ale] = nvo[ale]
    elif ale == 3:
        # gen[ale] += 0.01 if random.randrange(2) == 0 else -0.01
        gen[ale] += gen[ale] / 2 - random.randrange(2) * gen[ale]
        # gen[ale] += random.random() if random.randrange(2) == 0 else -random.random()
        if gen[ale] > 0:
            gen[ale] = nvo[ale]
    return gen

def reproduce(g1 ,g2):
    g = [0 ,0 ,0 ,0]
    for i in range( len(g) ):
        g[i] = g1[i] if random.randrange(2 ) ==0 else g2[i]
    return g

def evolution(pri, fiat, fee, n):
    global params
    params = [pri ,fiat ,fee]
    pop = [ born() for i in range(n) ]
    for i in range(50):
        for j in range( n //10):
            ind = random.randrange(n)
            pop.append( mutate(pop[ind]) )
            pop.append(born())
            a = random.randrange(n)
            b = random.randrange(n)
            pop.append( reproduce(pop[a] ,pop[b]) )
        pop = sorted(pop, key=fitness, reverse=True)
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
    simugraph(y ,100 ,0.0001 ,0.3 ,80 ,0.05 ,-0.05)

def test():
    x = [ 100* math.sin((4 * t / 100 - 2) * math.pi) + 10 * math.sin((16 * t / 100 - 8) * math.pi) for t in range(100)]
    y = [random.randint(-15, 15) + t + 200 for t in x]

    ema = EMA(0.3)

    z = []
    for t in y:
        z.append(ema.next(t))

    rat = Ratio(z[:10])
    ema_rat = []

    for t in z[10:]:
        ema_rat.append(rat.next(t) * 100)

    print(ema_rat)

    plt.plot(y)
    plt.plot(z)
    plt.plot(ema_rat)

    # Show the plot
    plt.show()


def test2():
    y = [100 * math.sin((2 * t / 100 - 1) * math.pi) + 10 * math.sin((8 * t / 100 - 4) * math.pi) + 10 * math.sin(
        (16 * t / 100 - 8) * math.pi) for t in range(100)]
    x = [random.randint(-15, 15) + t for t in y]

    sma = SMA(x[:5])
    sma_sig = []
    for t in x:
        sma_sig.append(t)

    rat = Ratio(sma_sig[:10])
    sma_rat = []
    for t in sma_sig[10:]:
        sma_rat.append(rat.next(t) * 100)

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
    pop_n = 100
    par = params + [pop_n]
    pop = evolution(*par)
    p = pop[0]
    print(p)
    par = params + p
    simugraph(*par)


def test5():
    prices = genprice()
    params = [prices, 100, 0.0001]
    pop_n = 20
    par = params + [pop_n]
    pop = evolve(*par)
    p = pop[0]
    print(p)
    par = params + p
    simugraph(*par)


def test6():
    prices = genprice()
    d0 = '2018-01-09 12:00:00'
    d1 = '2018-01-10 12:00:00'
    random.seed()
    ini = 1514771096
    fin = 1515912230
    prices = loadPrices(ini, fin)
    params = [prices, 100, 0.0001]
    gen = [0.426427716, 70, 0.020086, -0.016852181]
    gen = [0.25345167092181764, 24, 0.01742015806095379, -0.015868612469587984]
    gen = [0.10797469211486133, 42, 0.0050972323344256965, -0.0006449588306534429]
    gen = [0.5309097710296248, 71, 0.025269520207939822, -0.012467802801351402]
    gen = [0.06322814701689058, 30, 0.006598365101773482, -0.0010635786702839628]
    gen = [0.6976850624011044, 21, 0.013298465589017464]
    # good params for day trading, tested in a 2 week range
    gen = [0.0775214623335717, 108, 0.002508053420643197]
    gen = [0.20823818563981147, 167, 0.012559149541101634]
    gen = [0.11053557405104597, 100, 0.003075100947248841]
    gen = [0.02261740424759078, 109, 0.00665682583458158]
    gen = [0.013560024698097035, 89, 0.004012513576199672]
    gen = [0.3836631910358586, 194, 0.008800493328907144]
    gen = [0.10165607433861673, 99, 0.0032157637929226546]
    gen = [0.01681152953114882, 106, 0.003291656356364636]
    gen = [0.17343723553658355, 100, 0.008349280831410566]
    gen = [0.8419727025377259, 8, 0.2196043970583752]
    par = params + gen
    simugraph(*par)


def test8():
    d0 = '2018-01-09 12:00:00'
    d1 = '2018-01-10 12:00:00'
    random.seed()
    prices = loadPrices(d0, d1)
    train(prices)


def test9():
    ini = 1514771096
    fin = 1515912230
    sec = 24 * 60 * 60 * 3
    train(ini, fin, sec)


test6()
