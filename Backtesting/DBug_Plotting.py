### 2017 Jun 7
### Li Yuqiong
### Purpose: Debugging Plottings

## This part for ETFs
df = pd.read_csv('/Users/yuqiongli/desktop/python/finance/backtesting/ETFs-raw-results-all-threshold-10.csv')
df.rename(columns={'major': 'ETF', 'minor': 'date'}, inplace=True)
df.date = pd.to_datetime(df.date) # minor is date
df = df.set_index([df.date, df['ETF']])
del df.index.name
del df['date']
df = df.dropna() # remove NaN value
df = df.to_panel().transpose(2, 1, 0)

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

### The loop part
for i in range(0, len(pnl.keys())):
    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)
    ax.plot(df.iloc[i].index, df.iloc[i].Total0, label = 'Benchmark')
    ax.plot(df.iloc[i].index, df.iloc[i].Total1, label = 'Strategy 1')
    ax.plot(df.iloc[i].index, df.iloc[i].Total2, label = 'Strategy 2')
    ax.legend(loc = 'best')
    ax.set_title('Ten-Year Cumulative Wealth Curve, threshold = 10%, ' + df.iloc[i].ETF[0])
    plt.savefig('BT_ETF_All_Thre_10_'+ df.iloc[i].ETF[0] +'.png')
    plt.close()




## This part for stocks
df = pd.read_csv('/Users/yuqiongli/desktop/python/finance/backtesting/equities-raw-results-all-threshold-10.csv')
df.rename(columns={'major': 'Equity', 'minor': 'date'}, inplace=True)
df.date = pd.to_datetime(df.date) # minor is date
df = df.set_index([df.date, df['Equity']])
del df.index.name
del df['date']
df = df.dropna() # remove NaN value
df = df.to_panel().transpose(2, 1, 0)

import matplotlib.pyplot as plt
plt.style.use('ggplot') # Set plotting style

### The plot function
fig = plt.figure()
ax = fig.add_subplot(1, 1, 1)
ax.plot(df['AAPL US Equity'].index, df['AAPL US Equity'].Total0, label = 'Benchmark')
ax.plot(df['AAPL US Equity'].index, df['AAPL US Equity'].Total1, label = 'Strategy 1')
ax.plot(df['AAPL US Equity'].index, df['AAPL US Equity'].Total2, label = 'Strategy 2')
ax.set_title('Cumulative Wealth Curve, AAPL US Equity')
ax.legend(loc = 'best')
fig.show()

for i in range(3, len(pnl.keys())):
    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)
    ax.plot(df.iloc[i].index, df.iloc[i].Total0, label = 'Benchmark')
    ax.plot(df.iloc[i].index, df.iloc[i].Total1, label = 'Strategy 1')
    ax.plot(df.iloc[i].index, df.iloc[i].Total2, label = 'Strategy 2')
    ax.legend(loc = 'best')
    ax.set_title('Ten-Year Cumulative Wealth Curve, threshold = 10%, ' + df.iloc[i].Equity[0])
    plt.savefig('BT_Equity_All_Thre_10_'+ df.iloc[i].Equity[0] +'.png')
    plt.close()


#    fig.show()
# note: handled an error case brought by illegal character in stock name
fig = plt.figure()
ax = fig.add_subplot(1, 1, 1)
ax.plot(df.iloc[i].index, df.iloc[i].Total0, label = 'Benchmark')
ax.plot(df.iloc[i].index, df.iloc[i].Total1, label = 'Strategy 1')
ax.plot(df.iloc[i].index, df.iloc[i].Total2, label = 'Strategy 2')
ax.legend(loc = 'best')
ax.set_title('Ten-Year Cumulative Wealth Curve, threshold = 10%, ' + df.iloc[i].Equity[0])
plt.savefig('BT_Equity_All_Thre_10_BRKB US Equity.png')
plt.close()
