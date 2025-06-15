import pandas as pd

# Replace these with your actual filenames
file1 = ''
file1 = 's1/Linear Accelerometer.csv'
file2 = 's2/Linear Accelerometer.csv'
output_file = 'Linear Acceleration.csv'


# Load the CSVs
df1 = pd.read_csv(file1, sep=';')
df2 = pd.read_csv(file2, sep = ';')

# Grab the last time value from the first DataFrame
last_time = df1.iloc[-1, 0]

# Shift the time column in the second DataFrame
df2.iloc[:, 0] = df2.iloc[:, 0] + last_time

# Concatenate vertically
combined = pd.concat([df1, df2], ignore_index=True)

# Write out the result
combined.to_csv(output_file, index=False, sep=';')

print(f"Written concatenated CSV to {output_file}")

