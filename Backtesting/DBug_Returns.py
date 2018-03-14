### 2017 Jun 7
### Li Yuqiong
### Purpose: Debugging Plottings

### Total returns as table
for i in range(0, len(df)):
    temp = [df.iloc[i].ETF[0],
    (df.iloc[i].Total0[-1]-df.iloc[i].Total0[0])/df.iloc[i].Total0[0]*100,
    (df.iloc[i].Total1[-1]-df.iloc[i].Total1[0])/df.iloc[i].Total1[0]*100,
    (df.iloc[i].Total2[-1]-df.iloc[i].Total2[0])/df.iloc[i].Total2[0]*100]
    print temp;

### Total returns for equities
for i in range(0, len(df)):
    temp = [df.iloc[i].Equity[0],
    (df.iloc[i].Total0[-1]-df.iloc[i].Total0[0])/df.iloc[i].Total0[0]*100,
    (df.iloc[i].Total1[-1]-df.iloc[i].Total1[0])/df.iloc[i].Total1[0]*100,
    (df.iloc[i].Total2[-1]-df.iloc[i].Total2[0])/df.iloc[i].Total2[0]*100]
    print temp;


-7.3875
-11.0295
