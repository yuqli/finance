#backtest0808

import pandas as pd
import numpy as np


# Get dates
path = '/Users/yuqiongli/desktop/python/finance/sentiment0808/dates.csv'
df = pd.read_csv(path, dayfirst=False)
date = pd.to_datetime(df.dates, dayfirst = False)
date.to_csv('/Users/yuqiongli/desktop/python/finance/sentiment0808/dates_cleaned.csv', date_format = '%Y%m%d')
date_index = df.index


# Read in dates and price
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

MMM = read_csv_dateindex('/Users/yuqiongli/desktop/python/finance/sentiment0808/MMM.csv')
MO = read_csv_dateindex('/Users/yuqiongli/desktop/python/finance/sentiment0808/MO.csv')
KO = read_csv_dateindex('/Users/yuqiongli/desktop/python/finance/sentiment0808/KO.csv')

# Compute strategy

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


for i in [0.5, 1, 2]:
    dat = MO[['Price','Signal_' + str(i)]]
    dat.columns = ['close', 'signal']
    portfolio = strategy(dat)
    portfolio.to_csv('/Users/yuqiongli/desktop/python/finance/sentiment0808/MO' + str(i) + '.csv')
