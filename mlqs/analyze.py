import pandas as pd
import matplotlib.pyplot as plt

# Load your semicolon-delimited accelerometer data,
# parsing Time as floats (you can’t parse it as a datetime here)
df = pd.read_csv('Accelerometer.csv', sep=';', dtype={'Time': float})

# Put Time on the index
df.set_index('Time', inplace=True)

# Quick peek
print(df.head())
print(df.info())
print(df.describe())

# Plot X vs. Time
plt.figure(figsize=(10,4))
plt.plot(df.index, df['x'], marker='o', linestyle='-')
plt.title('X Axis over Time')
plt.xlabel('Time')
plt.ylabel('X')
plt.grid(True)
plt.tight_layout()
plt.show()

# Plot Y vs. Time
plt.figure(figsize=(10,4))
plt.plot(df.index, df['y'], marker='o', linestyle='-')
plt.title('Y Axis over Time')
plt.xlabel('Time')
plt.ylabel('Y')
plt.grid(True)
plt.tight_layout()
plt.show()

# Plot Z vs. Time
plt.figure(figsize=(10,4))
plt.plot(df.index, df['z'], marker='o', linestyle='-')
plt.title('Z Axis over Time')
plt.xlabel('Time')
plt.ylabel('Z')
plt.grid(True)
plt.tight_layout()
plt.show()
