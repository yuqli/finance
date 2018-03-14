import matplotlib.pyplot as plt
plt.style.use('ggplot') # Set plotting style

### The plot function
fig = plt.figure()
ax = fig.add_subplot(1, 1, 1)
ax.plot(df['EEM US Equity'].index, df['EEM US Equity'].Total0, label = 'Benchmark')
ax.plot(df['EEM US Equity'].index, df['EEM US Equity'].Total1, label = 'Strategy 1')
ax.plot(df['EEM US Equity'].index, df['EEM US Equity'].Total2, label = 'Strategy 2')
ax.set_title('Ten-Year Cumulative Wealth Curve, EEM US Equity')
ax.legend(loc = 'best')
fig.show()

import numpy as np
import pandas as pd  # pandas for data storage and analysis
import datetime
import pdb
## Operating on the whole df dataframe
### Read and Clean Data From CSV. CSV is downloaded from Bloomberg.
#### Small caps closing price
df = pd.read_csv('/Users/yuqiongli/downloads/read.csv')
date = pd.to_datetime(df.Date, dayfirst=False)
df = df.set_index(date)
del df.index.name
del df['Date']
df = df.dropna() # remove NaN value
df.sort_index()
df.to_csv('/Users/yuqiongli/downloads/out.csv', date_format = '%Y-%m-%d')

### The plot function
fig = plt.figure()
ax = fig.add_subplot(1, 1, 1)
ax.plot(df.index, df['USGG1M'], label = 'USGG 1M')
ax.plot(df.index, df['USGG1M'], label = 'USGG 1M')
ax.plot(df.index, df['USGG1M'], label = 'USGG 1M')
fig.show()

fig = plt.figure()
ax = fig.add_subplot(1, 1, 1)
ax.plot(df.index, df['USGG1M'], label = 'USGG 1M')
ax.plot(df.index, df['USGG1M'], label = 'USGG 1M')
ax.plot(df.index, df['USGG1M'], label = 'USGG 1M')
fig.show()

fig = plt.figure()
ax = fig.add_subplot(1, 1, 1)
ax.plot(df.index, df['USGG1M'], label = 'USGG 1M')
ax.plot(df.index, df['USGG1M'], label = 'USGG 1M')
ax.plot(df.index, df['USGG1M'], label = 'USGG 1M')
fig.show()



## Import csv
import numpy as np
import pandas as pd  # pandas for data storage and analysis
import datetime
import pdb
price = pd.read_csv('/Users/yuqiongli/downloads/price.csv')
dates = pd.read_csv('/Users/yuqiongli/downloads/dates.csv')
## This is the date series for indexing
dates = dates.ix[:, 1]
date = pd.to_datetime(dates, dayfirst=True)
### This is the total dataframe
date_idx = pd.to_datetime(price.Date, dayfirst=True)
price = price.set_index(date_idx)
### Selection
x = price[price.index.isin(dates)]

x.to_csv('/Users/yuqiongli/downloads/return.csv')
