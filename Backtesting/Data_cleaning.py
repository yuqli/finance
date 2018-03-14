### Data fetching and cleaning
df = pd.read_csv("/Users/yuqiongli/downloads/RTY.csv")
date = pd.to_datetime(df.Date)
df = df.set_index(date)
res = df.loc[df.index.year < 2013]
res.to_csv("/Users/yuqiongli/downloads/RTY_filtered_2012.csv")


df = pd.read_csv("/Users/yuqiongli/downloads/RSI_equities.csv")
date = pd.to_datetime(df.Date, dayfirst=True)
df = df.set_index(date)
del df['Date']


columns = ['Year', 'Month']+ df.columns.tolist()
mean_df = pd.DataFrame(columns=columns)

mean_df = dict.fromkeys(columns)

for year in range(df.index.year[0], df.index.year[-1]+1):
    for month in range(df.loc[df.index.year==year].index.month[0], df.loc[df.index.year==year].index.month[-1]+1):
        dat = getMonthlyData(df, year, month)
        newrow = [year, month]+ dat.mean().tolist()
        print newrow



        newrow = [year, month]+ dat.mean().tolist()
        mean_df.append(newrow)
        mean_df.concat(newrow)


res = df.loc[df.index.year < 2013]
res.to_csv("/Users/yuqiongli/downloads/RTY_filtered_2012.csv")
