##########
# setup
##########

# Downloads the dataset files.
import gdown

files = {
    'timeseries.csv': '1IuQib_tPj83kV8XTbCoL6goOZuyOgRB3',
    'sleep.csv': '17ild_0EAWa83siQBbKlZX1uOeeon2Ikx',
    'subjects.csv': '1Uet3e6BQRvinszc8FEaZJC0YH1dcKYry',
}
for name, file_id in files.items():
    gdown.download(id=file_id, output=name, quiet=True)

# Checks that all three files downloaded properly.
import os

for f in ['timeseries.csv', 'sleep.csv', 'subjects.csv']:
    assert os.path.exists(f) and os.path.getsize(f) > 1_000, f'{f} did not download properly. Rerun the download cell.'
print('All files downloaded.')

# Imports the datasets and displays the first 5 rows of the time series.
import numpy as np
import pandas as pd

timeseries = pd.read_csv('timeseries.csv', parse_dates=['timestamp'])
sleep = pd.read_csv('sleep.csv')
subjects = pd.read_csv('subjects.csv')


#############
# end of setup
#############

print(timeseries.head())

# this is our target dataset, columns needed from here are: user_id, in bed date, in bed time, out of
# print(sleep.head())

# subjects is not needed, except for maybe their age and gender
# print(subjects.head())