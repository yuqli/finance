import numpy as np
import pandas as pd  # pandas for data storage and analysis
import datetime
import pdb
## Operating on the whole df dataframe
### Read and Clean Data From CSV. CSV is downloaded from Bloomberg.
#### Small caps closing price
df = pd.read_csv('/Users/yuqiongli/desktop/python/finance/backtesting/RTY-small-caps-price.csv')
date = pd.to_datetime(df.date, dayfirst=True)
df = df.set_index(date)
del df.index.name
del df['date']
df = df.dropna() # remove NaN value
df.sort_index()


# In[3]:

#### Small caps RSI
RSIdata = pd.read_csv('/Users/yuqiongli/desktop/python/finance/backtesting/RTY-small-caps-RSI.csv')
date = pd.to_datetime(RSIdata.date, dayfirst=False)
RSIdata = RSIdata.set_index(date)
del RSIdata.index.name
del RSIdata['date']
RSIdata = RSIdata.dropna() # remove NaN value
RSIdata.sort_index()

pnl = {'Close': df, "RSI": RSIdata}
pnl = pd.Panel(pnl).transpose(2, 1, 0)

pnl.loc[:, :, 'Share'] = 0.0
pnl.loc[:, :, 'Position'] = 0.0
pnl.loc[:, :, 'Cash'] = 10000.0
pnl.loc[:, :, 'Total'] = 10000.0
pdb.set_trace()


percent1 = 0.1
percent2 = 0.2

ini_index = 0
inCash = 10000
inShare = 0

def getAsset0(df):
    df['Share'] = np.floor(df.Cash[0]/df.Close[0])
    df['Cash'] = df.Total[0] - df.Share[0] * df.Close[0]
    df['Position'] = df.Share * df.Close
    df['Total'] = df.Cash + df.Position
    return (df);

pdb.set_trace()
s0pnl = pnl.apply(lambda x:getAsset0(x), axis=(1, 2))
pdb.set_trace()
daily_return0 = res0.pct_change()[1:]
cum_wealth0 = (res0.iloc[-1]-res0.iloc[0])/res0.iloc[0]
