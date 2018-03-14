# test.py
import pandas as pd
import datetime
import numpy as np

todays_date = datetime.datetime.now().date()
index = pd.date_range(todays_date-datetime.timedelta(10), periods=10, freq='D')

columns = ['A', 'B', 'C']

df_ = pd.DataFrame(index=index, columns=columns) # note how to create a DataFrame
df_ = df_.fillna(0)

data = np.array([np.arange(10)]*3).T

df = pd.DataFrame(data, index=index, columns=columns )

# test if can apply a function with i to a dataframe
def test(df, i):
    df.iloc[2, i] = df.A[i-1]

for i in range(1, len(df)):
newdf =
