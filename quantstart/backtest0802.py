# 20170802
# New rounds of analysis

# results.py

import pandas as pd
import numpy as np


# Get dates
path = '/Users/yuqiongli/desktop/python/finance/quantstart/dates.csv'
df = pd.read_csv(path, dayfirst=False)
date = pd.to_datetime(df.Date, dayfirst = False)
date.to_csv('/Users/yuqiongli/desktop/python/finance/quantstart/dates_cleaned.csv', date_format = '%Y%m%d')
date_index = df.index


# read in data
def read_csv_dateindex(path):
    """
    read_csv_dateindex takes in an absolute path containing csv file
    then, takes the date variable as an index and transform the csv into a DataFrame
    """
    df = pd.read_csv(path, parse_dates = ['Date'])
    date = pd.to_datetime(df.Date)
    df = df.set_index(date)
    del df['Date']
    # df = df.dropna() # remove NaN value

    df.sort_index()
    return(df);

price = read_csv_dateindex('/Users/yuqiongli/desktop/python/finance/quantstart/price.csv')
ratio_05 = read_csv_dateindex('/Users/yuqiongli/desktop/python/finance/quantstart/ratio_0.5.csv')
ratio_1 = read_csv_dateindex('/Users/yuqiongli/desktop/python/finance/quantstart/ratio_1.csv')
ratio_2 = read_csv_dateindex('/Users/yuqiongli/desktop/python/finance/quantstart/ratio_2.csv')


# Reshape into panels
# subslice price
# REalized here : missing data leads to data length different
price_subset = price.loc[ratio_05.index[0]:price.index[-1]]
# FB = pd.concat([price_subset['FB US Equity'], ratio_05['FB US Equity']], axis=1)
FB = pd.concat([price_subset['FB US Equity'], ratio_2['FB US Equity']], axis=1)
FB.columns = ['close', 'signal']

# SPY = pd.concat([price_subset['SPY US Equity'], ratio_05['SPY US Equity']], axis=1)
SPY = pd.concat([price_subset['SPY US Equity'], ratio_2['SPY US Equity']], axis=1)
SPY.columns = ['close', 'signal']

#MSCI = pd.concat([price_subset['MSCI US Equity'], ratio_05['MSCI US Equity']], axis=1)
MSCI = pd.concat([price_subset['MSCI US Equity'], ratio_2['MSCI US Equity']], axis=1)
MSCI.columns = ['close', 'signal']

#HK700 = pd.concat([price_subset['700 HK Equity'], ratio_05['700 HK Equity']], axis=1)
HK700 = pd.concat([price_subset['700 HK Equity'], ratio_2['700 HK Equity']], axis=1)
HK700.columns = ['close', 'signal']

# PG = pd.concat([price_subset['PG US Equity'], ratio_05['PG US Equity']], axis=1)
PG = pd.concat([price_subset['PG US Equity'], ratio_2['PG US Equity']], axis=1)
PG.columns = ['close', 'signal']


import matplotlib.pyplot as plt
plt.style.use('ggplot')

def strategy(df): # df is a dataframe with dates, close, and signals
    initial_capital=100000.0
    index = df.index
    columns = ['positions','shares', 'cash', 'holdings', 'total']
    portfolio = pd.DataFrame(index = index, columns = columns)
    portfolio['close'] = df.close
    portfolio['signal'] = df.signal
    portfolio.loc[index[0], 'positions'] = np.floor(initial_capital/portfolio.loc[index[0], 'close'])
    portfolio.loc[index[0], 'shares'] = portfolio.loc[index[0], 'positions']
    portfolio.loc[index[0], 'cash'] = initial_capital - portfolio.shares[0] * portfolio.close[0]
    portfolio.loc[index[0], 'holdings'] = portfolio.close[0] * portfolio.shares[0]
    portfolio.loc[index[0], 'total'] = portfolio.holdings[0] + portfolio.cash[0]
    for i in range(1, len(df.signal)):
        if (df.signal[i] == 1):
            portfolio.loc[index[i], 'positions'] = np.floor(portfolio.loc[index[i-1], 'cash']/portfolio.loc[index[i], 'close']) # use all cash to buy in
            portfolio.loc[index[i], 'cash'] = portfolio.loc[index[i-1], 'cash'] - portfolio.loc[index[i], 'positions']*portfolio.loc[index[i], 'close']
            portfolio.loc[index[i], 'shares'] = portfolio.loc[index[i-1], 'shares'] + portfolio.loc[index[i], 'positions']
        elif(df.signal[i] == 0):
            portfolio.loc[index[i], 'positions'] = 0
            portfolio.loc[index[i], 'cash'] = portfolio.loc[index[i-1], 'cash']
            portfolio.loc[index[i], 'shares'] = portfolio.loc[index[i-1], 'shares']
        elif(df.signal[i] == -1):
            portfolio.loc[index[i], 'positions'] = portfolio.loc[index[i-1], 'shares'] # sell all
            portfolio.loc[index[i], 'cash'] = portfolio.loc[index[i-1], 'cash'] + portfolio.loc[index[i], 'positions']*portfolio.loc[index[i], 'close']
            portfolio.loc[index[i], 'shares'] = 0
        portfolio['holdings'] = portfolio['shares'] * portfolio['close']
        portfolio['total'] = portfolio['cash'] + portfolio['holdings']
        portfolio['returns'] = portfolio['total'].pct_change()
    return(portfolio)

portfolio = strategy(FB)
portfolio.to_csv('/Users/yuqiongli/desktop/python/finance/quantstart/FB_2.csv')

portfolio = strategy(SPY)
portfolio.to_csv('/Users/yuqiongli/desktop/python/finance/quantstart/SPY_2.csv')

portfolio = strategy(MSCI)
portfolio.to_csv('/Users/yuqiongli/desktop/python/finance/quantstart/MSCI_2.csv')

portfolio = strategy(HK700)
portfolio.to_csv('/Users/yuqiongli/desktop/python/finance/quantstart/HK700_2.csv')

portfolio = strategy(PG)
portfolio.to_csv('/Users/yuqiongli/desktop/python/finance/quantstart/PG_2.csv')



# plot returns
def plotreturn(portfolio):
    fig = plt.figure(figsize=(20, 10))
    ax = fig.add_subplot(2, 1, 1)
    ax.plot(portfolio.index, portfolio.returns)
    ax.set_title('Daily Simple return for FB US Equity, Put/Call Ratio Entry/Exit STDEV = 0.5')
    ax = fig.add_subplot(2, 1, 2)
    ax.plot(portfolio.index, portfolio.total)
    ax.set_title('Cumulative Wealth Curve FB US Equity, Put/Call Ratio Entry/Exit STDEV = 0.5')
    plt.savefig('results.png')
    plt.close()


fig = plt.figure(figsize=(20, 10))
ax = fig.add_subplot(2, 1, 1)
ax.plot(portfolio.index, portfolio.returns)
ax.set_title('Daily Simple return for SPY US Equity, Put/Call Ratio Entry/Exit STDEV = 0.5')
ax = fig.add_subplot(2, 1, 2)
ax.plot(portfolio.index, portfolio.total)
ax.set_title('Cumulative Wealth Curve SPY US Equity, Put/Call Ratio Entry/Exit STDEV = 0.5')
plt.savefig('SPY results 0.5.png')
plt.close()
