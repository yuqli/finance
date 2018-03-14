# results.py

import pandas as pd
import numpy as np

path = '/Users/yuqiongli/desktop/python/finance/quantstart/dat.csv'
path = '/Users/yuqiongli/downloads/put_call_ratio.csv'
df = pd.read_csv(path, dayfirst = True)
date = pd.to_datetime(df.Date, dayfirst = True)
df = df.set_index(date)
del df['Date']
df = df.dropna()
df.sort_index()

#plot price
import matplotlib.pyplot as plt
plt.style.use('ggplot') # Set plotting style

initial_capital=100000.0
index = df.index
columns = ['positions','shares', 'cash', 'holdings', 'total']
portfolio = pd.DataFrame(index = index, columns = columns)
portfolio['close'] = df.Close
portfolio['signal'] = df.Signal
portfolio.loc[index[0], 'positions'] = np.floor(initial_capital/portfolio.loc[index[0], 'close'])
portfolio.loc[index[0], 'shares'] = portfolio.loc[index[0], 'positions']
portfolio.loc[index[0], 'cash'] = initial_capital - portfolio.shares[0] * portfolio.close[0]
portfolio.loc[index[0], 'holdings'] = portfolio.close[0] * portfolio.shares[0]
portfolio.loc[index[0], 'total'] = portfolio.holdings[0] + portfolio.cash[0]


for i in range(1, len(df.Signal)):
    if (df.Signal[i] == 1):
        portfolio.loc[index[i], 'positions'] = np.floor(portfolio.loc[index[i-1], 'cash']/portfolio.loc[index[i], 'close']) # use all cash to buy in
        portfolio.loc[index[i], 'cash'] = portfolio.loc[index[i-1], 'cash'] - portfolio.loc[index[i], 'positions']*portfolio.loc[index[i], 'close']
        portfolio.loc[index[i], 'shares'] = portfolio.loc[index[i-1], 'shares'] + portfolio.loc[index[i], 'positions']
    elif(df.Signal[i] == 0):
        portfolio.loc[index[i], 'positions'] = 0
        portfolio.loc[index[i], 'cash'] = portfolio.loc[index[i-1], 'cash']
        portfolio.loc[index[i], 'shares'] = portfolio.loc[index[i-1], 'shares']
    elif(df.Signal[i] == -1):
        portfolio.loc[index[i], 'positions'] = portfolio.loc[index[i-1], 'shares'] # sell all
        portfolio.loc[index[i], 'cash'] = portfolio.loc[index[i-1], 'cash'] + portfolio.loc[index[i], 'positions']*portfolio.loc[index[i], 'close']
        portfolio.loc[index[i], 'shares'] = 0
    portfolio['holdings'] = portfolio['shares'] * portfolio['close']
    portfolio['total'] = portfolio['cash'] + portfolio['holdings']
    portfolio['returns'] = portfolio['total'].pct_change()

# plot returns
fig = plt.figure(figsize=(20, 10))
ax = fig.add_subplot(2, 1, 1)
ax.plot(portfolio.index, portfolio.returns)
ax.set_title('Daily Simple return for IBM US Euqity, Put/Call Ratio Entry/Exit STDEV = 1.25')
ax = fig.add_subplot(2, 1, 2)
ax.plot(portfolio.index, portfolio.total)
ax.set_title('Cumulative Wealth Curve IBM US Euqity, Put/Call Ratio Entry/Exit STDEV = 1.25')
plt.savefig('results.png')
plt.close()
