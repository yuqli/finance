### 2017 Jun 7
### Li Yuqiong
### Purpose: Debugging Plottings

# pnl = pnl[:, 0:300,:] # note the grammar

percent1 = 0.10
percent2 = 0.2

s1cutPt1 = 0.2
s1warningPt = 1

s2cutPt1 = 0.2
s2cutPt2 = 0.2
s2warningPt = 1

import time
start_time = time.time()
s0pnl = pnl.apply(lambda x:getAsset0(x), axis=(1, 2)) # results of benchmarks
s1pnl = pnl.apply(lambda x:getAsset1(x, percent1, percent2), axis=(1, 2)) # results of strategy 1
s2pnl = pnl.apply(lambda x:getAsset2(x, percent1, percent2), axis=(1, 2)) # results of strategy 2
print("--- %s seconds ---" % (time.time() - start_time))
# --- 467.82071805 seconds --- for ETFs
# this is, 8 minutes for 300 variables.. thus, 80 minutes for ten of them! roughly two hours

# --- for Equities
# >>> print("--- %s seconds ---" % (time.time() - start_time))
# --- 616.944240093 seconds ---
# this is, 10 minuts for 300 variables... Thus, 100 minutes for 3000. roughly 3 hours

s0pnl
s1pnl
s2pnl

pnlAll = {'Close': s1pnl[:, :, 'Close'],
'Share0': s0pnl[:, :, 'Share'],
'Share1': s1pnl[:, :, 'Share'],
'Share2': s2pnl[:, :, 'Share'],
'Cash0': s0pnl[:, :, 'Cash'],
'Cash1': s1pnl[:, :, 'Cash'],
'Cash2': s2pnl[:, :, 'Cash'],
'Total0': s0pnl[:, :, 'Total'],
'Total1': s1pnl[:, :, 'Total'],
'Total2': s2pnl[:, :, "Total"]}

pnlAll = pd.Panel(pnlAll).transpose(2, 1, 0)
pnlAll.keys()

res = pnlAll.transpose(2, 0, 1).to_frame()
res.to_csv('/Users/yuqiongli/desktop/python/finance/backtesting/ETFs-raw-results-all-threshold-10.csv')

# For equities
res.to_csv('/Users/yuqiongli/desktop/python/finance/backtesting/equities-raw-results-all-threshold-10.csv')
