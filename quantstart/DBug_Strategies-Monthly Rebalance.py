### 2017 Jun 7
### Li Yuqiong
### Purpose: Debugging Strategies

### Function name: getMonthlyData
### Dependencies: pandas
### Note: This function takes in a pandas dataframe with all data and
##### return slices of it based on year and month
def getMonthlyData(df, year, month):
    dat = df.loc[(df.index.year==year) & (df.index.month == month)]
    return(dat);

## Testing results:
# getMonthlyData(df, 2007, 8)


### the basic check cut loops for monthly data, used for later loop
def checkCondition(dat, threshold, i):
    if ((dat.Close[i] <= threshold) & (i != (len(dat)-1))):
        return True;
    else:
        return False;

## Testing function: checkCondition(dat, threshold, i)
# rng = pd.date_range('1/1/2011', periods=5, freq='D')
# Close = [100, 90, 80, 80, 0]
# dat = pd.DataFrame({'Close': Close, 'Open':abs(np.random.randn(len(rng))*100)}, index=rng)

# for i in range(0, len(dat)):
#     print checkCondition(dat, 95, i)
#### Testing results: passed


def checkCutDouble(dat, percent1, percent2):
    dat['Check'] = False
    for i in range(0, (len(dat)-1)):
        threshold1 = dat.Close[0:i].max() * (1-percent1)
        warninghold = dat.Close[0:i].max() * (1-percent2)
        if (checkCondition(dat, warninghold, i) == True):
            dat.iloc[i, dat.columns.get_loc('Check')] = True
            return {"state": "w", "warningDate": dat.index[i], "afterWarningDate": dat.index[i+1]};
        elif (checkCondition(dat, threshold1, i) == True):
            dat.iloc[i, dat.columns.get_loc('Check')] = True
            for j in range(i, (len(dat)-1)):
                warninghold = dat.Close[i:j].max() * (1-percent2)
                if (checkCondition(dat, warninghold, j) == True):
                    dat.iloc[j, dat.columns.get_loc('Check')] = True
                    return {"state": "tw", "warningDate": dat.index[j], "afterWarningDate": dat.index[j+1],
                    "triggerDate1": dat.index[i], "cutDate1": dat.index[i+1]};
            return {"state": "t", "triggerDate1": dat.index[i], "cutDate1": dat.index[i+1]};
    return {"state": "na"};

## Testing function: checkCutDouble(dat, percent1, percent2)
# pd.set_option('chained_assignment',None)
# rng = pd.date_range('1/1/2011', periods=5, freq='D')
#### No cut
# Close = [100, 100, 98, 105, 200]
## {'state': 'na'}

#### 5% down only, not enddate
#Close = [100, 90, 80, 80, 0]
## {'state': 't', 'triggerDate1': Timestamp('2011-01-02 00:00:00', offset='D'), 'cutDate1': Timestamp('2011-01-03 00:00:00', offset='D')}

#### 5% down only, enddate
# Close = [100, 120, 130, 200, 150]
# {'state': 'na'}

#### 5% down first, 20% down later, not end date
# Close = [100, 90, 50, 80, 150]
# {'state': 'tw', 'warningDate': Timestamp('2011-01-03 00:00:00', offset='D'), 'triggerDate1': Timestamp('2011-01-02 00:00:00', offset='D'), 'afterWarningDate': Timestamp('2011-01-04 00:00:00', offset='D'), 'cutDate1': Timestamp('2011-01-03 00:00:00', offset='D')}

#### 5% down first, 20% down later, 20% down end date
# Close = [100, 90, 80, 80, 0]
# {'state': 't', 'triggerDate1': Timestamp('2011-01-02 00:00:00', offset='D'), 'cutDate1': Timestamp('2011-01-03 00:00:00', offset='D')}

#### 20% down only, not end date
# Close = [100, 160, 165, 70, 165]
# {'state': 'w', 'warningDate': Timestamp('2011-01-04 00:00:00', offset='D'), 'afterWarningDate': Timestamp('2011-01-05 00:00:00', offset='D')}

#### 20% down only, end date
# Close = [100, 160, 165, 158, 70]
# {'state': 'na'}

#### 20% down first, 5 % down later, not end date
# Close = [100, 70, 50, 100, 0]
# {'state': 'w', 'warningDate': Timestamp('2011-01-02 00:00:00', offset='D'), 'afterWarningDate': Timestamp('2011-01-03 00:00:00', offset='D')}

# dat = pd.DataFrame({'Close': Close, 'Open':abs(np.random.randn(len(rng))*100)}, index=rng)
# checkCutDouble(dat, 0.05, 0.2)


def checkCutTriple(dat, percent1, percent2):
    dat['Check'] = False
    for i in range(0, (len(dat)-1)):
        threshold1 = dat.Close[0:i].max() * (1-percent1)
        warninghold = dat.Close[0:i].max() * (1-percent2)
        if (checkCondition(dat, warninghold, i) == True):
            dat.iloc[i, dat.columns.get_loc('Check')] = True
            return {"state": "w", "warningDate": dat.index[i], "afterWarningDate": dat.index[i+1]};
        elif (checkCondition(dat, threshold1, i) == True):
            for j in range(i, (len(dat)-1)):
                dat.iloc[j, dat.columns.get_loc('Check')] = True
                threshold2 = dat.Close[i:j].max() * (1-percent1)
                warninghold = dat.Close[i:j].max() * (1-percent2)
                if (checkCondition(dat, warninghold, j) == True):
                    return {"state": "tw", "warningDate": dat.index[j], "afterWarningDate": dat.index[j+1],
                    "triggerDate1": dat.index[i], "cutDate1": dat.index[i+1]};
                elif (checkCondition(dat, threshold2, j) == True):
                    for u in range(j, (len(dat)-1)):
                        dat.iloc[u, dat.columns.get_loc('Check')] = True
                        warninghold = dat.Close[j:u].max() * (1-percent2)
                        if (checkCondition(dat, warninghold, u) == True):
                            return {"state": "ttw", "warningDate": dat.index[u], "afterWarningDate": dat.index[u+1],
                            "triggerDate1": dat.index[i], "cutDate1": dat.index[i+1],
                            "triggerDate2": dat.index[j], "cutDate2": dat.index[j+1]};
                    return {"state": "tt", "triggerDate2": dat.index[j], "cutDate2": dat.index[j+1],
                    "triggerDate1": dat.index[i], "cutDate1": dat.index[i+1]};
            return {"state": "t", "triggerDate1": dat.index[i], "cutDate1": dat.index[i+1]};
    return {"state": "na"};

## Testing function: checkCutTriple(dat, percent1, percent2)
# pd.set_option('chained_assignment',None)
# rng = pd.date_range('1/1/2011', periods=5, freq='D')
#### No cut
# Close = [100, 100, 98, 105, 200]
## {'state': 'na'}

#### 5% down + 5% down, not enddate
# Close = [100, 90, 80, 80, 0]
# {'state': 'tt', 'cutDate1': Timestamp('2011-01-03 00:00:00', offset='D'), 'cutDate2': Timestamp('2011-01-04 00:00:00', offset='D'), 'triggerDate2': Timestamp('2011-01-03 00:00:00', offset='D'), 'triggerDate1': Timestamp('2011-01-02 00:00:00', offset='D')}

#### 5% down + 5% down + 20% down, not enddate
# Close = [100, 90, 80, 0, 80]
# {'warningDate': Timestamp('2011-01-04 00:00:00', offset='D'), 'triggerDate1': Timestamp('2011-01-02 00:00:00', offset='D'), 'triggerDate2': Timestamp('2011-01-03 00:00:00', offset='D'), 'cutDate1': Timestamp('2011-01-03 00:00:00', offset='D'), 'cutDate2': Timestamp('2011-01-04 00:00:00', offset='D'), 'state': 'ttw', 'afterWarningDate': Timestamp('2011-01-05 00:00:00', offset='D')}

#### 5% down only, enddate
# Close = [100, 120, 130, 200, 150]
# {'state': 'na'}

#### 5% down first, 20% down later, not end date
# Close = [100, 90, 50, 80, 150]
# {'state': 'tw', 'warningDate': Timestamp('2011-01-03 00:00:00', offset='D'), 'triggerDate1': Timestamp('2011-01-02 00:00:00', offset='D'), 'afterWarningDate': Timestamp('2011-01-04 00:00:00', offset='D'), 'cutDate1': Timestamp('2011-01-03 00:00:00', offset='D')}

#### 5% down first, 5% down again. 20% down later, 20% down end date
# Close = [100, 90, 80, 80, 0]
# {'state': 'tt', 'cutDate1': Timestamp('2011-01-03 00:00:00', offset='D'), 'cutDate2': Timestamp('2011-01-04 00:00:00', offset='D'), 'triggerDate2': Timestamp('2011-01-03 00:00:00', offset='D'), 'triggerDate1': Timestamp('2011-01-02 00:00:00', offset='D')}

#### 20% down only, not end date
# Close = [100, 160, 165, 70, 165]
# {'state': 'w', 'warningDate': Timestamp('2011-01-04 00:00:00', offset='D'), 'afterWarningDate': Timestamp('2011-01-05 00:00:00', offset='D')}

#### 20% down only, end date
# Close = [100, 160, 165, 158, 70]
# {'state': 'na'}

#### 5% down first, up and new max, 20 % down later, not end date
# Close = [100, 90, 165, 140, 0]
# {'state': 'w', 'warningDate': Timestamp('2011-01-02 00:00:00', offset='D'), 'afterWarningDate': Timestamp('2011-01-03 00:00:00', offset='D')}

# dat = pd.DataFrame({'Close': Close, 'Open':abs(np.random.randn(len(rng))*100)}, index=rng)
# checkCutTriple(dat, 0.05, 0.2)

### Note: This function takes in a pandas dataframe with monthly data and indexes
##### return an updated dataframe slices where stock from index1 are cut at index2
def Cut(dat, index1, index2, percent):
    dat.loc[index2, 'Share'] = np.floor(dat.Share[index1] * (1-percent))
    dat.loc[index2, 'Cash'] = dat.Cash[index1] + (dat.Share[index1] - dat.Share[index2]) * dat.Close[index2]
    dat.loc[index2, 'Position'] = dat.Share[index2] * dat.Close[index2]
    dat.loc[index2, 'Total'] = dat.Position[index2] + dat.Cash[index2]
    return(dat);


### Function name: Hold
### Dependencies: pandas
### Note: This function takes in a pandas dataframe with monthly data and indexes
##### return an updated dataframe slices where stock are hold from index1 to index2
def Hold(dat, index1, index2):
    dat.loc[index1:index2, 'Share'] = dat.Share[index1]
    dat.loc[index1:index2, 'Cash'] = dat.Cash[index1]
    dat.loc[index1:index2, 'Position'] = dat.Share[index1:index2] * dat.Close[index1:index2]
    dat.loc[index1:index2, 'Total'] = dat.Position[index1:index2] + dat.Cash[index1:index2]
    return(dat);


### Function name: getPrevious
### Dependencies: pandas
### Note: This function takes in 1) a pandas dataframe containing all historical data and 2) year and month to fetch data
##### return an the initial state of stock share and cash from last month
### Caveats: Beginning of months are tricky
def getPrevious(df, year, month):
    if ((year == df.index.year[0]) & (month == df.index.month[0])):
        inShare = 0.0
        inCash = 10000.0
    elif (month == 1):
        inShare = df.Share[(df.index.year==year-1) & (df.index.month == 12)].tail(1)[0]
        inCash = df.Cash[(df.index.year==year-1) & (df.index.month == 12)].tail(1)[0]
    else:
        inShare = df.Share[(df.index.year==year) & (df.index.month == month-1)].tail(1)[0]
        inCash = df.Cash[(df.index.year==year) & (df.index.month == month-1)].tail(1)[0]
    return([inShare, inCash]);


### Function name: firstDay
### Dependencies: pandas, getPrevious function
### Note: This function takes in 1) monthly data to be updated 2) initial states of cash and share
##### return the first day position of each month, where supposed to buy back
def firstDay(dat, inShare, inCash):
    dat.loc[dat.index[0], 'Share'] = inShare + np.floor(inCash/dat.Close[0])
    dat.loc[dat.index[0], 'Cash'] = inCash - (dat.Share[0]-inShare) * dat.Close[0]
    dat.loc[dat.index[0], 'Position'] = dat.Close[0] * dat.Share[0]
    dat.loc[dat.index[0], 'Total'] = dat.Position[0] + dat.Cash[0]
    return(dat);

# Testing: firstDay
# dat = getMonthlyData(pnl['EEM US Equity'], 2008, 8)
# firstDay(dat, 0, 10000)



### Function name: getAsset0
### Note: benchmark performance
def getAsset0(df):
    df['Share'] = np.floor(df.Cash[0]/df.Close[0])
    df['Cash'] = df.Total[0] - df.Share[0] * df.Close[0]
    df['Position'] = df.Share * df.Close
    df['Total'] = df.Cash + df.Position
    return (df);
# Testing: correct

pd.set_option('chained_assignment', 'warn')

def getAsset1(df, percent1, percent2):
    for year in range(df.index.year[0], df.index.year[-1]+1):
        for month in range(df.loc[df.index.year==year].index.month[0], df.loc[df.index.year==year].index.month[-1]+1):
            dat = getMonthlyData(df, year, month)
            inShare = getPrevious(df, year, month)[0]
            inCash = getPrevious(df, year, month)[1]
            dat = firstDay(dat, inShare, inCash)
            beginDate = dat.index[0]
            endDate = dat.index[-1]
            state = checkCutDouble(dat, percent1, percent2)['state'] # 't','w','tw','na'
            if (state == 'na'):
                Hold(dat, beginDate, endDate)
            elif (state == 't'):
                triggerDate1 = checkCutDouble(dat, percent1, percent2)['triggerDate1']
                cutDate1 = checkCutDouble(dat, percent1, percent2)['cutDate1']
                Hold(dat, beginDate, triggerDate1)
                Cut(dat, triggerDate1, cutDate1, s1cutPt1)
                Hold(dat, cutDate1, endDate)
            elif (state == 'w'):
                warningDate = checkCutDouble(dat, percent1, percent2)['warningDate']
                afterWarningDate = checkCutDouble(dat, percent1, percent2)['afterWarningDate']
                Hold(dat, beginDate, warningDate)
                Cut(dat, warningDate, afterWarningDate, s1warningPt)
                Hold(dat, afterWarningDate, endDate)
            elif (state == 'tw'):
                triggerDate1 = checkCutDouble(dat, percent1, percent2)['triggerDate1']
                cutDate1 = checkCutDouble(dat, percent1, percent2)['cutDate1']
                warningDate = checkCutDouble(dat, percent1, percent2)['warningDate']
                afterWarningDate = checkCutDouble(dat, percent1, percent2)['afterWarningDate']
                Hold(dat, beginDate, triggerDate1)
                Cut(dat, triggerDate1, cutDate1, s1cutPt1)
                Hold(dat, cutDate1, warningDate)
                Cut(dat, warningDate, afterWarningDate, s1warningPt)
                Hold(dat, afterWarningDate, endDate)
            df.loc[(df.index.year==year) & (df.index.month == month)] = dat
    return(df);

def getAsset2(df, percent1, percent2):
    for year in range(df.index.year[0], df.index.year[-1]+1):
        for month in range(df.loc[df.index.year==year].index.month[0], df.loc[df.index.year==year].index.month[-1]+1):
            dat = getMonthlyData(df, year, month)
            inShare = getPrevious(df, year, month)[0]
            inCash = getPrevious(df, year, month)[1]
            dat = firstDay(dat, inShare, inCash)
            beginDate = dat.index[0]
            endDate = dat.index[-1]
            state = checkCutTriple(dat, percent1, percent2)['state'] # 'w','t','tw','tt','ttw','na'
            if (state == 'na'):
                Hold(dat, beginDate, endDate)
            elif (state == 't'):
                triggerDate1 = checkCutTriple(dat, percent1, percent2)['triggerDate1']
                cutDate1 = checkCutTriple(dat, percent1, percent2)['cutDate1']
                Hold(dat, beginDate, triggerDate1)
                Cut(dat, triggerDate1, cutDate1, s2cutPt1)
                Hold(dat, cutDate1, endDate)
            elif (state == 'w'):
                warningDate = checkCutTriple(dat, percent1, percent2)['warningDate']
                afterWarningDate = checkCutTriple(dat, percent1, percent2)['afterWarningDate']
                Hold(dat, beginDate, warningDate)
                Cut(dat, warningDate, afterWarningDate, s2warningPt)
                Hold(dat, afterWarningDate, endDate)
            elif (state == 'tw'):
                triggerDate1 = checkCutTriple(dat, percent1, percent2)['triggerDate1']
                cutDate1 = checkCutTriple(dat, percent1, percent2)['cutDate1']
                warningDate = checkCutTriple(dat, percent1, percent2)['warningDate']
                afterWarningDate = checkCutTriple(dat, percent1, percent2)['afterWarningDate']
                Hold(dat, beginDate, triggerDate1)
                Cut(dat, triggerDate1, cutDate1, s2cutPt1)
                Hold(dat, cutDate1, warningDate)
                Cut(dat, warningDate, afterWarningDate, s2warningPt)
                Hold(dat, afterWarningDate, endDate)
            elif (state == 'tt'):
                triggerDate1 = checkCutTriple(dat, percent1, percent2)['triggerDate1']
                cutDate1 = checkCutTriple(dat, percent1, percent2)['cutDate1']
                triggerDate2 = checkCutTriple(dat, percent1, percent2)['triggerDate2']
                cutDate2 = checkCutTriple(dat, percent1, percent2)['cutDate2']
                Hold(dat, beginDate, triggerDate1)
                Cut(dat, triggerDate1, cutDate1, s2cutPt1)
                Hold(dat, cutDate1, triggerDate2)
                Cut(dat, triggerDate2, cutDate2, s2cutPt2)
                Hold(dat, cutDate2, endDate)
            elif (state == 'ttw'):
                triggerDate1 = checkCutTriple(dat, percent1, percent2)['triggerDate1']
                cutDate1 = checkCutTriple(dat, percent1, percent2)['cutDate1']
                warningDate = checkCutTriple(dat, percent1, percent2)['warningDate']
                afterWarningDate = checkCutTriple(dat, percent1, percent2)['afterWarningDate']
                triggerDate2 = checkCutTriple(dat, percent1, percent2)['triggerDate2']
                cutDate2 = checkCutTriple(dat, percent1, percent2)['cutDate2']
                Hold(dat, beginDate, triggerDate1)
                Cut(dat, triggerDate1, cutDate1, s2cutPt1)
                Hold(dat, cutDate1, triggerDate2)
                Cut(dat, triggerDate2, cutDate2, s2cutPt2)
                Hold(dat, cutDate2, warningDate)
                Cut(dat, warningDate, afterWarningDate, s2warningPt)
                Hold(dat, afterWarningDate, endDate)
            df.loc[(df.index.year==year) & (df.index.month == month)] = dat
    return(df);




# import time
# start_time = time.time()
# df = pnl['EEM US Equity'][0:300]
# getAsset0(df)
# print("--- %s seconds ---" % (time.time() - start_time))
## Roughly 17s for 300 rows
## Total time = 17*20*10*3 = 170 min = 3h
## For another also 3h === total = 6h
