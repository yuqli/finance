### 2017 Jun 12, 13
### Li Yuqiong
### Purpose: Debugging Strategies

import numpy as np
import pandas as pd  # pandas for data storage and analysis
import datetime
import pdb
## Operating on the whole df dataframe

# What does this function do?
# Loop through. Perform cut if possible.
# After all cut, return a date for initialization

percent1 = 0.1
percent2 = 0.2

ini_index = 0
inCash = 10000
inShare = 0

### Cut-loss strategy here
def cutLoss(dat, ini_index, inCash, inShare):
    while (ini_index < (len(dat)-1)):  # If it's the last day, still buy new on the day
        Initialize(dat, ini_index, inShare, inCash) # initialize date ini_index
        #    pdb.set_trace()
        datelist = checkCutDouble(dat, ini_index, percent1, percent2)
        #    pdb.set_trace()
        update(dat, ini_index, datelist)
        #    pdb.set_trace()

        # Check enter series
        state = datelist['state']
        if (state == 't' or state == 'wt'):
            triggerDate = datelist['triggerDate']
            #        pdb.set_trace()
            cutDate = dat.index[dat.index.get_loc(triggerDate) + 1]
            #        pdb.set_trace()
            enter_signal = getRSIindex(dat, triggerDate, 30)
            #        pdb.set_trace()
            if (enter_signal == None): ## This means the cut date is the last day. No cut, end loop
                break;
            elif (enter_signal == dat.index[-1]): ## This means the signal day is the last day. No re-enter
                Hold(dat, cutDate, enter_signal)
                #            pdb.set_trace()
                break;
            else: ## This means the signal day is neither the last day
                Hold(dat, cutDate, enter_signal)
                inCash = dat.Cash[enter_signal]
                inShare = dat.Share[enter_signal]
                ini_index = dat.index.get_loc(enter_signal) + 1
                #            pdb.set_trace()
                continue;
        elif (state == 'na'): # This case has already been updated
            break;
        elif (state == 'w'): # This case hold till the end
            warningDate = datelist['warningDate']
            afterWarningDate = dat.index[dat.index.get_loc(warningDate) + 1]
            endDate = datelist['endDate']
            Hold(dat, afterWarningDate, endDate)
            break;
    return dat;


def checkCutDouble(df, ini_index, percent1, percent2):
    dat['Check'] = False
    for i in range(ini_index + 1, (len(dat)-1)):
        warning_hold = dat.Close[ini_index:i].max() * (1-percent1)
        trigger_hold = dat.Close[ini_index:i].max() * (1-percent2)
        if (checkCondition(dat, trigger_hold, i) == True):
            dat.iloc[i, dat.columns.get_loc('Check')] = True
            return {"state": "t", "triggerDate": dat.index[i]};
        elif (checkCondition(dat, warning_hold, i) == True):
            dat.iloc[i, dat.columns.get_loc('Check')] = True
            for j in range(i, (len(dat)-1)):
                warning_hold = dat.Close[i:j].max() * (1-percent1)
                if (checkCondition(dat, warning_hold, j) == True):
                    dat.iloc[j, dat.columns.get_loc('Check')] = True
                    return {"state": "wt", "warningDate": dat.index[i], "triggerDate": dat.index[j]};
            return {"state": "w", "warningDate": dat.index[i], 'endDate': dat.index[i]};
    return {"state": "na", 'endDate' : dat.index[-1]};

# datelist = checkCutDouble(dat, ini_index, percent1, percent2)


def update(dat, ini_index, datelist):
    beginDate = dat.index[ini_index]
    state = datelist['state'] # 't', 'wt', 'w', 'na'
    if (state == 'na'):
        endDate = datelist['endDate']
        Hold(dat, beginDate, endDate)
    elif (state == 'w'):
        endDate = datelist['endDate']
        warningDate = datelist['warningDate']
        afterWarningDate = dat.index[dat.index.get_loc(warningDate) + 1]
        Hold(dat, beginDate, warningDate)
        Cut(dat, warningDate, afterWarningDate, 0.5)
        Hold(dat, beginDate, warningDate)
    elif (state == 't'):
        triggerDate = datelist['triggerDate']
        cutDate = dat.index[dat.index.get_loc(triggerDate) + 1] # cutDate is the next day after triggerDate
        Hold(dat, beginDate, triggerDate)
        Cut(dat, triggerDate, cutDate, 1)
    elif (state == 'wt'):
        warningDate = datelist['warningDate']
        afterWarningDate = dat.index[dat.index.get_loc(warningDate) + 1]
        triggerDate = datelist['triggerDate']
        cutDate = dat.index[dat.index.get_loc(triggerDate) + 1]
        Hold(dat, beginDate, warningDate)
        Cut(dat, warningDate, afterWarningDate, 0.5)
        Hold(dat, afterWarningDate, triggerDate)
        Cut(dat, triggerDate, cutDate, 1)


# if state = t or state = wt then continue into next loop
def getRSIindex(dat, triggerDate, RSI_threshold):
    cutDate = dat.index.get_loc(triggerDate) + 1
    if cutDate == (len(dat)-1):
        return None;
    for i in range(cutDate, (len(dat)-1)):
        if (dat.RSI[i] <= 40):
            return dat.index[i];
    return dat.index[-1];


### the basic check cut loops for monthly data, used for later loop
def checkCondition(dat, threshold, i):
    if ((dat.Close[i] <= threshold) & (i != (len(dat)-1))):
        return True;
    else:
        return False;

def Initialize(dat, i, inShare, inCash):
    dat.loc[dat.index[i], 'Share'] = inShare + np.floor(inCash/dat.Close[i])
    dat.loc[dat.index[i], 'Cash'] = inCash - (dat.Share[i]-inShare) * dat.Close[i]
    dat.loc[dat.index[i], 'Position'] = dat.Close[i] * dat.Share[i]
    dat.loc[dat.index[i], 'Total'] = dat.Position[i] + dat.Cash[i]
    return(dat);



## Testing function: checkCutDouble(dat, i, percent1, percent2)

#### No cut
# Close = [100, 100, 98, 105, 200]
## {'state': 'na'}

#### 10% down + 10% down, not enddate
# Close = [100, 88, 90, 60, 10]
# {'state': 'tt', 'cutDate1': Timestamp('2011-01-03 00:00:00', offset='D'), 'cutDate2': Timestamp('2011-01-04 00:00:00', offset='D'), 'triggerDate2': Timestamp('2011-01-03 00:00:00', offset='D'), 'triggerDate1': Timestamp('2011-01-02 00:00:00', offset='D')}

#### 20% down not enddate
# Close = [100, 90, 80, 0, 80]
# {'warningDate': Timestamp('2011-01-04 00:00:00', offset='D'), 'triggerDate1': Timestamp('2011-01-02 00:00:00', offset='D'), 'triggerDate2': Timestamp('2011-01-03 00:00:00', offset='D'), 'cutDate1': Timestamp('2011-01-03 00:00:00', offset='D'), 'cutDate2': Timestamp('2011-01-04 00:00:00', offset='D'), 'state': 'ttw', 'afterWarningDate': Timestamp('2011-01-05 00:00:00', offset='D')}

#### 10% down + 20% down only, enddate
# Close = [100, 87, 49, 200, 150]
# {'state': 'na'}

#### 10% down only, no other cut
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


## Debug: Buying back
#### 10% down + 10% down, not enddate, buy back the next day
# Close = [100, 88, 90, 60, 10, 30, 40, 50]
# RSI = [70, 70, 70, 70, 20, 50, 70, 70]
# {'state': 'tt', 'cutDate1': Timestamp('2011-01-03 00:00:00', offset='D'), 'cutDate2': Timestamp('2011-01-04 00:00:00', offset='D'), 'triggerDate2': Timestamp('2011-01-03 00:00:00', offset='D'), 'triggerDate1': Timestamp('2011-01-02 00:00:00', offset='D')}

#### 20% down not enddate
# Close = [100, 90, 80, 0, 80]
# {'warningDate': Timestamp('2011-01-04 00:00:00', offset='D'), 'triggerDate1': Timestamp('2011-01-02 00:00:00', offset='D'), 'triggerDate2': Timestamp('2011-01-03 00:00:00', offset='D'), 'cutDate1': Timestamp('2011-01-03 00:00:00', offset='D'), 'cutDate2': Timestamp('2011-01-04 00:00:00', offset='D'), 'state': 'ttw', 'afterWarningDate': Timestamp('2011-01-05 00:00:00', offset='D')}

#### 10% down + 20% down only, enddate
# Close = [100, 87, 49, 200, 150]
# {'state': 'na'}

#### 10% down only, no other cut
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



# pd.set_option('chained_assignment',None)
# Building testing data
Close = [100, 99, 95, 99, 98, 100, 100, 80]
RSI = [70, 70, 70, 70, 20, 50, 70, 70]
rng = pd.date_range('1/1/2011', periods=8, freq='D')
dat = pd.DataFrame({'Close': Close, 'Open':abs(np.random.randn(len(rng))*100)}, index=rng)
dat['Share'] = 0
dat['Cash'] = 10000
dat['Position'] = dat.Share * dat.Close
dat['Total'] = dat.Cash + dat.Position
dat['RSI'] = RSI

# checkCutTriple(dat, 0.05, 0.2)

### Note: This function takes in a pandas dataframe with monthly data and indexes
##### return an updated dataframe slices where stock from index1 are cut at index2
def Cut(dat, index1, index2, percent):
    dat.loc[index2, 'Share'] = np.floor(dat.Position[index1] * (1-percent) / dat.Close[index2])
    dat.loc[index2, 'Position'] = dat.Share[index2] * dat.Close[index2]
    dat.loc[index2, 'Cash'] = dat.Cash[index1] + (dat.Share[index1] - dat.Share[index2]) * dat.Close[index2]
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





## With pnl
df = pnl['RESI US Equity']
dat = df.loc[df.index.year==2013][0:100]
