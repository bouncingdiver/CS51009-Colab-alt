# Imports the datasets
import numpy as np
import pandas as pd

timeseries = pd.read_csv('timeseries.csv', parse_dates=['timestamp'])
sleep = pd.read_csv('sleep.csv')
subjects = pd.read_csv('subjects.csv')

n_off = 0

# iterating over lines in dataframe
for row in timeseries.itertuples():
    if row.Inclinometer_Off == 1:
        n_off += 1


print(f"Inclinometer off lines: {n_off}")