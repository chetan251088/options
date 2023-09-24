from ib_insync import *

#util.startLoop()

ib = IB()
ib.connect('192.168.0.104', 7496, clientId=12)

bn = Index('BANKNIFTY', 'NSE')
print(ib.qualifyContracts(bn))

ib.reqMarketDataType(4)
[ticker] = ib.reqTickers(bn)
#ticker

bnValue = ticker.marketPrice()
print(bnValue)

chains = ib.reqSecDefOptParams(bn.symbol, '', bn.secType, bn.conId)

util.df(chains)

chain = next(c for c in chains if c.tradingClass == 'BANKNIFTY' and c.exchange == 'NSE')
#chain

strikes = [strike for strike in chain.strikes
        if strike % 5 == 0
        and bnValue - 100 < strike < bnValue + 100]
expirations = sorted(exp for exp in chain.expirations)[:3]
rights = ['P', 'C']

contracts = [Option('BANKNIFTY', expiration, strike, right, 'NSE', tradingClass='BANKNIFTY')
        for right in rights
        for expiration in expirations
        for strike in strikes]

contracts = ib.qualifyContracts(*contracts)
len(contracts)

print(contracts[0])

tickers = ib.reqTickers(*contracts)

print(tickers[0])


ib.disconnect()