# Imports the datasets
import numpy as np
import pandas as pd

timeseries = pd.read_csv('timeseries.csv', parse_dates=['timestamp'])
sleep = pd.read_csv('sleep.csv')
subjects = pd.read_csv('subjects.csv')

# making column names more usable
timeseries.columns = timeseries.columns.str.replace(' ', '_')

#################
# data preprocessing
#################

# new dataframe with columns we need
out_df = timeseries[["user_id", "timestamp", "Inclinometer_Off", "Inclinometer_Standing", "Inclinometer_Sitting", "Inclinometer_Lying", "Vector_Magnitude", "HR", "Steps"]]
print(out_df.head())

# getting start minute
current_minute = out_df.iloc[0]["timestamp"].minute
minute_datapoints = []
minute_aggregated_data = pd.DataFrame(columns=["user_id", "timestamp", "avg_hr", "avg_vector_magnitude", "sum_steps", "inc_standing", "inc_sitting", "inc_lying"])

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

def determineInclinometerValue(datapoints):
    standing = 0
    sitting = 0
    lying = 0
    total = 0

    for row in datapoints:
        if row.Inclinometer_Standing == 1:
          standing += 1
          total += 1
        elif row.Inclinometer_Sitting == 1:
          sitting += 1
          total += 1
        elif row.Inclinometer_Lying == 1:
          lying += 1
          total += 1

    if (total != 0):
      values = [(standing / total), (sitting / total), (lying / total)]
    else:
      values = [0,0,0]
    return values


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
            minute_inclinometer_values = determineInclinometerValue(minute_datapoints)

            new_row = pd.DataFrame({"user_id": [current_user_id], "timestamp": [current_timestamp], "avg_hr": [avg_hr], "avg_vector_magnitude": [avg_vector_magnitude], "sum_steps": [sum_steps], "inc_standing": [minute_inclinometer_values[0]], "inc_sitting": [minute_inclinometer_values[1]], "inc_lying": [minute_inclinometer_values[2]]})
              


            minute_aggregated_data = pd.concat([minute_aggregated_data, new_row], ignore_index=True)

            # updating current values
            current_user_id = row.user_id
            current_timestamp = row.timestamp
            current_minute = row.timestamp.minute

            # clear datapoints for next minute
            minute_datapoints.clear()

print(minute_aggregated_data.head())

standing = 0
sitting = 0
lying = 0
rows = 0

for row in minute_aggregated_data.itertuples():
    standing += row.inc_standing
    sitting += row.inc_sitting
    lying += row.inc_lying
    rows += 1

print(f"Total number of rows: {rows}")
print(f"Average standing: {standing / rows}")
print(f"Average sitting: {sitting / rows}")
print(f"Average lying: {lying / rows}")