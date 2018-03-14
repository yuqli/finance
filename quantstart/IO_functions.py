# IO_functions.py

import numpy as np
import pandas as pd  # pandas for data storage and analysis
import datetime

def read_csv_dateindex(path):
    """
    read_csv_dateindex takes in an absolute path containing csv file
    then, takes the date variable as an index and transform the csv into a DataFrame
    """
    df = pd.read_csv(path)
    date = pd.to_datetime(df.Date)
    df = df.set_index(date)
    del df['Date']
    df = df.dropna() # remove NaN value
    df.sort_index()
    return(df);
