##########
# setup
##########

# Downloads the dataset files.
import gdown

# files = {
#     'timeseries.csv': '1IuQib_tPj83kV8XTbCoL6goOZuyOgRB3',
#     'sleep.csv': '17ild_0EAWa83siQBbKlZX1uOeeon2Ikx',
#     'subjects.csv': '1Uet3e6BQRvinszc8FEaZJC0YH1dcKYry',
# }
# for name, file_id in files.items():
#     gdown.download(id=file_id, output=name, quiet=True)

# # Checks that all three files downloaded properly.
# import os

# for f in ['timeseries.csv', 'sleep.csv', 'subjects.csv']:
#     assert os.path.exists(f) and os.path.getsize(f) > 1_000, f'{f} did not download properly. Rerun the download cell.'
# print('All files downloaded.')


#############
# end of setup
#############

# Imports the datasets and displays the first 5 rows of the time series.
import numpy as np
import pandas as pd

timeseries = pd.read_csv('timeseries.csv', parse_dates=['timestamp'])
sleep = pd.read_csv('sleep.csv')
subjects = pd.read_csv('subjects.csv')


###################
# average number of datapoints per minute
###################

# for timeseries, take out minutes that don't have 30 or more data points

# # first minute value
# current_minute = timeseries.iloc[0]["timestamp"].minute
# num_seconds = 0

# # counter
# total_seconds = 0
# num_minutes = 0
# min = 0
# first_min = False

# counter_under_30 = 0

# # iterating over lines in dataframe
# for row in timeseries.itertuples():
#     if (num_seconds == 0):
#         print(f"Current hour: {row.timestamp.hour}, Current minute: {current_minute}")
#     # for this row, check if minute matches
    
#     if (row.timestamp.minute == current_minute):
#         num_seconds += 1
#     else:
#         # minute complete, print number of datapoints
#         print(f"Time: {row.timestamp.hour}:{row.timestamp.minute}, {num_seconds}  datapoints")
#         total_seconds += num_seconds
#         num_minutes += 1

#         if (first_min == False):
#             first_min = True
#             min = num_seconds
#         else:
#             if (num_seconds < min):
#                 min = num_seconds

#         if (num_seconds < 40):
#             counter_under_30 += 1
#         num_seconds = 1
#         current_minute = row.timestamp.minute

# print("Average datapoints per minute: ", total_seconds/num_minutes)
# print("Number of minutes with less than 40 datapoints: ", counter_under_30)
# print("Minimum datapoints in a minute: ", min)


#################
# data preprocessing
#################

# getting clean inclinometer data
inc_clean = []
for row in timeseries.itertuples():
    if row[9] == 0:
        if row[10] == 1:
            inc_clean.append(1)
        elif row[11] == 1:
            inc_clean.append(2)
        elif row[12] == 1:
            inc_clean.append(3)
    else:
        inc_clean.append(0)

timeseries.insert(1, "clean_inclinometer", inc_clean)
print(timeseries.head())
# new dataframe with columns we need
out_df = timeseries[["user_id", "timestamp", "clean_inclinometer", "Vector Magnitude", "HR", "Steps"]]
print(out_df.head())

# getting start minute
current_minute = out_df.iloc[0]["timestamp"].minute
minute_datapoints = []
minute_agg_alt = pd.DataFrame(columns=["user_id", "timestamp", "avg_hr", "avg_vector_magnitude", "sum_steps"])

# getting intial other data
current_user_id = out_df.iloc[0]["user_id"]
current_timestamp = out_df.iloc[0]["timestamp"]

def average_values(datapoints, position):
    total = 0
    for row in datapoints:
        total += row[position]
    average = total / len(datapoints)
    return average

def sum_values(datapoints, position):
    total = 0
    for row in datapoints:
        total += row[position]
    return total

for row in out_df.itertuples():
    if (row.timestamp.minute == current_minute):
        minute_datapoints.append(row)
    else:
        # new minute found, check how many datapoints we have for previous minute
        if minute_datapoints.__len__() < 40:
            # clear minute datapoints, ignore this minute
            minute_datapoints.clear()
        else:
            # get average values for hr and vector magnitude
            avg_hr = average_values(minute_datapoints, 5)
            avg_vector_magnitude = average_values(minute_datapoints, 4)
            sum_steps = sum_values(minute_datapoints, 6)

            new_row = pd.DataFrame({"user_id": [current_user_id], "timestamp": [current_timestamp], "avg_hr": [avg_hr], "avg_vector_magnitude": [avg_vector_magnitude], "sum_steps": [sum_steps]})
            minute_agg_alt = pd.concat([minute_agg_alt, new_row], ignore_index=True)

            # updating current values
            current_user_id = row.user_id
            current_timestamp = row.timestamp
            current_minute = row.timestamp.minute

            # clear datapoints for next minute
            minute_datapoints.clear()

print(minute_agg_alt.head())
minute_agg_alt.to_csv("out_df.csv", header=True, index=False)



# example of concatenation
# minute_df = pd.DataFrame(columns=["user_id", "hr"])

# row = pd.DataFrame({"user_id": [1], "hr": [100]})
# row1 = pd.DataFrame({"user_id": [1], "hr": [90]})
# row2 = pd.DataFrame({"user_id": [1], "hr": [80]})
# row3 = pd.DataFrame({"user_id": [1], "hr": [84]})

# output = pd.concat([minute_df, row, row1, row2, row3], ignore_index=True)
# print(output.head())

# new_col = ["1", "2", "3", "4"]

# output.insert(1, "new_col", new_col)
# print(output.head())



# # columns needed here are: user_id, timestamp, hr(will get averaged over the minute), vector magnitude (in place of movement axis), inclinometer info
# print(timeseries.head())

# # this is our target dataset, columns needed from here are: user_id, in bed date, in bed time, out of bed time (this is our ground truth)
# print(sleep.head())

# # subjects is not needed, except for maybe their age and gender
# print(subjects.head())


# timeseries["timestamp"] = pd.to_datetime(timeseries["timestamp"])

# metadata = {"timestamp", "day", "time", "user_id"}
# value_cols = [
#     c for c in timeseries.select_dtypes(include="number").columns
#     if c not in metadata
# ]

# result = (
#     timeseries.set_index("timestamp")
#       .groupby(["user_id", "day"])[value_cols]
#       .resample("60s", closed="right", label="left")
#       .mean()
#       .reset_index()
#       .sort_values(by=["user_id", "timestamp", "day"])
# )

# #print(result)
# result.to_csv("grouped_times.csv", header=True, index=False)

# # for row in timeseries.head(3).itertuples():
# #     print(row)

# print("I am finished")
# #X_train, X_test, y_train, y_test = train_test_split(timeseries, test_size=0.33, random_state=42)
# #timeseries.sort_values(by=["user_id", "timestamp", "day"])
# #timeseries.to_csv("sorted_timeseries.csv", header=True, index=False)