# Downloads the dataset files.
import csv
import gdown
import numpy as np
import pandas as pd
import os
from sklearn.model_selection import train_test_split
import time
from datetime import datetime, timedelta

print("I am running give me a second")

# def download_files():
#     print(f'{f} did not download properly. Rerun the download cell.')
#     files = {
#         'timeseries.csv': '1IuQib_tPj83kV8XTbCoL6goOZuyOgRB3',
#         'sleep.csv': '17ild_0EAWa83siQBbKlZX1uOeeon2Ikx',
#         'subjects.csv': '1Uet3e6BQRvinszc8FEaZJC0YH1dcKYry',
#     }
#     for name, file_id in files.items():
#         gdown.download(id=file_id, output=name, quiet=True)
    
#     return True

# for f in ['timeseries.csv', 'sleep.csv', 'subjects.csv']:
#     print("Checking " + str(f))

#     #This will give an error and crash the program if one of the files is missing however it will download and if you run again all is good
#     assert os.path.exists(f) and os.path.getsize(f) > 1_000, download_files(); f'{f} did not download properly. Rerun the download cell.'

timeseries = pd.read_csv('timeseries.csv', parse_dates=['timestamp'])
sleep = pd.read_csv('sleep.csv')
subjects = pd.read_csv('subjects.csv')


value_cols = timeseries.columns

print("Slow startup complete have fun")

timeseries["timestamp"] = pd.to_datetime(timeseries["timestamp"])
metadata = {"timestamp", "day", "time", "user_id"}

#get every other column in the dataframe
value_cols = [
    c for c in timeseries.select_dtypes(include="number").columns
    if c not in metadata
]

result = (
    timeseries.set_index("timestamp")
      .groupby(["user_id", "day"])[value_cols]
      .resample("60s", closed="right", label="left")
      .mean()
      .reset_index()
      .sort_values(by=["user_id", "timestamp", "day"])
)

#result.to_csv("grouped_times.csv", header=True, index=False)
#print(result[result['user_id'] == 6 or result['HR'] == ""])
#print(result[result['HR'] == ""])

new_df = result.dropna()
new_df.drop(new_df.columns[new_df.columns.str.contains('unnamed', case=False)], axis=1, inplace=True)   #gets rid of a rogue unamed column
#new_df.to_csv("grouped_times_missing.csv", header=True, index=False)

###############
# added in
###############

# making column names more usable
sleep.columns = sleep.columns.str.replace(' ', '')

##############

#transform each row in sleep into a timestamp of starting sleep and a timestamp of ending sleep

starting_date = datetime.strptime('2000-01-01 00:00:00', "%Y-%m-%d %H:%M:%S")
for row in sleep.itertuples(index=False):
    temp = row.InBedTime.split(":")
    hours = temp[0]
    minutes = temp[1]
    startOfSleeping = starting_date + timedelta(days=(row.InBedDate-1), hours=int(hours), minutes=int(minutes))

    temp = row.OutBedTime.split(":")
    hours = temp[0]
    minutes = temp[1]

    endOfSleeping = starting_date + timedelta(days=(row.OutBedDate-1), hours=int(hours), minutes=int(minutes))

    #print(startOfSleeping, endOfSleeping)
print("-"*20)
cleaned_minutes = pd.read_csv('cleaned_minutes.csv', parse_dates=['timestamp'])

#Assign labels to each row of inputed dataframe
list_lables = []
for row in timeseries.itertuples(index=False):          # change timeseries -> cleaned_minutes 
    if startOfSleeping <= row.timestamp <= endOfSleeping:
        #print("Found a timestamp within my range")
        list_lables.append("1")
        continue
    else:
        list_lables.append("0")
            

label_dataframe = pd.DataFrame({"Label": list_lables})
label_dataframe.to_csv("labels_big.csv", header=True, index=False)
print("I am finished")
#timeseries.sort_values(by=["user_id", "timestamp", "day"])
#timeseries.to_csv("sorted_timeseries.csv", header=True, index=False)