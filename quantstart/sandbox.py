


def backtest_portfolio(self):
    for i in range(1, len(self.signals)-1):
        if (self.signals == 1):
            portfolio.loc[index[i], 'positions'] = np.floor(portfolio.loc[index[i-1], 'cash']/portfolio.loc[index[i], 'close']) # use all cash to buy in
            portfolio.loc[index[i], 'cash'] = portfolio.loc[index[i-1], 'cash'] - portfolio.loc[index[i], 'positions']*portfolio.loc[index[i], 'close']
            portfolio.loc[index[i], 'shares'] = portfolio.loc[index[i-1], 'shares'] + portfolio.loc[index[i], 'positions']
        elif(self.signals == 0):
            portfolio.loc[index[i], 'positions'] = 0
            portfolio.loc[index[i], 'cash'] = portfolio.loc[index[i-1], 'cash']
        elif(self.signals == -1):
            portfolio.loc[index[i], 'positions'] = portfolio.loc[index[i-1], 'shares'] # sell all
            portfolio.loc[index[i], 'cash'] = portfolio.loc[index[i-1], 'cash'] + portfolio.loc[index[i], 'positions']*portfolio.loc[index[i], 'close']
            portfolio.loc[index[i], 'shares'] = 0
        portfolio['holdings'] = portfolio['shares'] * portfolio['close']
        portfolio['total'] = portfolio['cash'] + portfolio['holdings']
        portfolio['returns'] = portfolio['total'].pct_change()
    return portfolio



path = '/Users/yuqiongli/desktop/python/finance/quantstart/price.csv'
df = pd.read_csv(path, dayfirst= False)
date = pd.to_datetime(df.Date)
df = df.set_index(date)
del df['Date']
df = df.dropna() # remove NaN value
df.sort_index()

df.to_csv('/Users/yuqiongli/desktop/python/finance/quantstart/price.csv')
price = read_csv_dateindex('/Users/yuqiongli/desktop/python/finance/quantstart/price.csv')
