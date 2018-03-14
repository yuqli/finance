def getMonthDates(tempTradeDays):
    dateRange = [tempTradeDays[0]] # A list with first date
    tempYear = None
    dictYears = tempTradeDays.groupby(tempTradeDays.year)
    for yr in dictYears.keys():
        tempYear = pd.DatetimeIndex(dictYears[yr]).groupby(pd.DatetimeIndex(dictYears[yr]).month)
        for m in tempYear.keys():
            dateRange.append(max(tempYear[m]))
    dateRange = pd.DatetimeIndex(dateRange).order()
    return(dateRange);
