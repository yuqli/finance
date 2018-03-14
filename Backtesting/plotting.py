



import matplotlib.pyplot as plt
plt.style.use('ggplot') # Set plotting style

fig = plt.figure()
ax = fig.add_subplot(1, 1, 1)
ax.plot(dat.index, dat.Total, label = 'Cut-loss')
ax.plot(dat2.index, dat2.Total, label = 'Benchmark')
ax.set_title('Five-Year Cumulative Wealth Curve, RESI US Equity')
ax.legend(loc = 'best')
plt.savefig('BT_Sample.png')
fig.show()
