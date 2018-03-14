# sentiment.py

import numpy as np
import pandas as pd
import backtest
import IO_functions

from backtest import Strategy, Portfolio
from IO_functions import read_csv_dateindex

class SentimentStrategy(Strategy):
    """Derives from Strategy to produce a set of signals that
    generates sell/buy signal based on put/call ratios."""

    def __init__(self, symbol, bars):
    	"""Requires the symbol ticker and the pandas DataFrame of bars"""
        self.symbol = symbol
        self.bars = bars

    def generate_signals(self):
        signals = read_csv_dateindex('/Users/yuqiongli/desktop/python/finance/quantstart/put_call_ratio.csv')
        return signals

class MarketOnOpenPortfolio(Portfolio):
    def __init__(self, symbol, bars, signals, initial_capital=100000.0):
        self.symbol = symbol
        self.bars = bars
        self.signals = signals
        self.initial_capital = float(initial_capital)

    def initialize_portfolio(self):
        index = self.bars.index
        columns = ['positions','shares', 'cash', 'holdings', 'total']
        portfolio = pd.DataFrame(index = index, columns = columns)
        portfolio['close'] = bars['Adj. Close']
        portfolio.loc[index[0], 'positions'] = np.floor(10000/portfolio.loc[index[0], 'close'])
        portfolio.loc[index[0], 'shares'] = portfolio.loc[index[0], 'positions']
        portfolio.loc[index[0], 'cash'] = 10000 - portfolio.shares[0] * portfolio.close[0]
        portfolio.loc[index[0], 'holdings'] = portfolio.close[0] * portfolio.shares[0]
        portfolio.loc[index[0], 'total'] = portfolio.holdings[0] + portfolio.cash[0]

    def backtest_portfolio(self):
        for i in range(1, len(self.signals)-1):
            if (self.signals[i] == 1):
                portfolio.loc[index[i], 'positions'] = np.floor(portfolio.loc[index[i-1], 'cash']/portfolio.loc[index[i], 'close']) # use all cash to buy in
                portfolio.loc[index[i], 'cash'] = portfolio.loc[index[i-1], 'cash'] - portfolio.loc[index[i], 'positions']*portfolio.loc[index[i], 'close']
                portfolio.loc[index[i], 'shares'] = portfolio.loc[index[i-1], 'shares'] + portfolio.loc[index[i], 'positions']
            elif(self.signals[i] == 0):
                portfolio.loc[index[i], 'positions'] = 0
                portfolio.loc[index[i], 'cash'] = portfolio.loc[index[i-1], 'cash']
            elif(self.signals[i] == -1):
                portfolio.loc[index[i], 'positions'] = portfolio.loc[index[i-1], 'shares'] # sell all
                portfolio.loc[index[i], 'cash'] = portfolio.loc[index[i-1], 'cash'] + portfolio.loc[index[i], 'positions']*portfolio.loc[index[i], 'close']
                portfolio.loc[index[i], 'shares'] = 0
            portfolio['holdings'] = portfolio['shares'] * portfolio['close']
            portfolio['total'] = portfolio['cash'] + portfolio['holdings']
            portfolio['returns'] = portfolio['total'].pct_change()
        return portfolio

if __name__ == "__main__":
    # Obtain daily bars of SPY (ETF that generally
    # follows the S&P500) from Quandl (requires 'pip install Quandl'
    # on the command line)
    symbol = 'FB'
    # bars = quandl.get("GOOG/NYSE_%s" % symbol, collapse="daily")
    path = "/Users/yuqiongli/desktop/python/finance/quantstart/WIKI-FB.csv"
    bars = IO_functions.read_csv_dateindex(path)

    # Create a set of random forecasting signals for SPY
    rfs = SentimentStrategy(symbol, bars)
    signals = rfs.generate_signals()

    # Create a portfolio of SPY
    portfolio = MarketOnOpenPortfolio(symbol, bars, signals, initial_capital=100000.0)
    returns = portfolio.backtest_portfolio()

    print returns.tail(10)
