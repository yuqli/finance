### 2017 Jun 7
### Li Yuqiong
### Purpose: Debugging Data input parts

import numpy as np
import pandas as pd  # pandas for data storage and analysis
import datetime


## Equities
df = pd.read_csv('/Users/yuqiongli/desktop/python/finance/backtesting/equities_historical_prices.csv')
date = pd.to_datetime(df.Date, dayfirst=True)
df = df.set_index(date)
del df.index.name
del df['Date']
df = df.dropna() # remove NaN value
df.sort_index()

## ETFs
df = pd.read_csv('/Users/yuqiongli/desktop/python/finance/backtesting/ETFs_historical_prices.csv')
date = pd.to_datetime(df.Ticket, dayfirst=False)
df = df.set_index(date)
del df.index.name
del df['Ticket']
df = df.dropna() # remove NaN value
df.sort_index()

# Small caps closing price
df = pd.read_csv('/Users/yuqiongli/desktop/python/finance/backtesting/RTY-small-caps-price.csv')
date = pd.to_datetime(df.date, dayfirst=True)
df = df.set_index(date)
del df.index.name
del df['date']
df = df.dropna() # remove NaN value
df.sort_index()

# Small caps RSI
RSIdata = pd.read_csv('/Users/yuqiongli/desktop/python/finance/backtesting/RTY-small-caps-RSI.csv')
date = pd.to_datetime(RSIdata.date, dayfirst=False)
RSIdata = RSIdata.set_index(date)
del RSIdata.index.name
del RSIdata['date']
RSIdata = RSIdata.dropna() # remove NaN value
RSIdata.sort_index()


# transform dataframe to panel
pnl = {'Close': df, "RSI": RSIdata}
pnl = pd.Panel(pnl).transpose(2, 1, 0)

pnl.loc[:, :, 'Share'] = 0.0
pnl.loc[:, :, 'Position'] = 0.0
pnl.loc[:, :, 'Cash'] = 10000.0
pnl.loc[:, :, 'Total'] = 10000.0
#### Debugging finished for this part

# >>> pnl
# <class 'pandas.core.panel.Panel'>
# Dimensions: 214 (items) x 1108 (major_axis) x 6 (minor_axis)
# Items axis: RESI US Equity to MED US Equity
# Major_axis axis: 2013-01-04 00:00:00 to 2017-06-09 00:00:00
# Minor_axis axis: Close to Total
