import pandas as pd
results = pd.read_csv('out_df.csv')

off = 0
standing = 0
sitting = 0
lying = 0

for row in results.itertuples():
    match row.inclinometer_value:
        case 0:
            off += 1
        case 1:
            standing += 1
        case 2:
            sitting += 1
        case 3:
            lying += 1

print(f"Off: {off}\nStanding: {standing}\nSitting: {sitting}\nLying: {lying}")