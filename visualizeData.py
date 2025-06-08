import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages

sensor_configs = {
    "Accelerometer": {
        "file": "Accelerometer.csv",
        "axes": ['X (m/s^2)', 'Y (m/s^2)', 'Z (m/s^2)']
    },
    "Linear Accelerometer": {
        "file": "Linear Accelerometer.csv",
        "axes": ['X (m/s^2)', 'Y (m/s^2)', 'Z (m/s^2)']
    },
    "Gyroscope": {
        "file": "Gyroscope.csv",
        "axes": ['X (rad/s)', 'Y (rad/s)', 'Z (rad/s)']
    },
    "Location": {
        "file": "Location.csv",
        "axes": ['Latitude (°)', 'Longitude (°)', 'Height (m)', 'Velocity (m/s)']
    }
}

# Output PDF path
pfdGraphs = "bikingGraphs.pdf"

with PdfPages(pfdGraphs) as pdf:
    for sensor_name, config in sensor_configs.items():
        file = config["file"]
        axes = config["axes"]

        try:
            df = pd.read_csv(file, sep=';')
        except FileNotFoundError:
            print(f"file????? {file}")
            continue

        df = df.rename(columns=lambda x: x.strip('"'))
        df.set_index('Time (s)', inplace=True)

        #flow plots
        for axis in axes:
            if axis in df.columns:
                plt.figure(figsize=(10, 4))
                plt.plot(df.index, df[axis])
                plt.title(f'{sensor_name} - {axis} Over Time')
                plt.xlabel('Time (s)')
                plt.ylabel(axis)
                plt.grid(True)
                plt.tight_layout()
                pdf.savefig()
                plt.close()

        #standard deviation
        window = 5
        roll_std = df.rolling(window=window).std()

        for axis in axes:
            if axis in roll_std.columns:
                plt.figure(figsize=(10, 4))
                plt.plot(roll_std.index, roll_std[axis])
                plt.title(f'{sensor_name} - Rolling Std Dev of {axis} (window={window})')
                plt.xlabel('Time (s)')
                plt.ylabel('Std Dev')
                plt.grid(True)
                plt.tight_layout()
                pdf.savefig()
                plt.close()

        #barchart st
        std_vals = df[axes].std()
        plt.figure(figsize=(6, 4))
        std_vals.plot(kind='bar')
        plt.title(f'{sensor_name} - Overall Standard Deviation by Axis')
        plt.xlabel('Axis')
        plt.ylabel('Std Dev')
        plt.grid(axis='y')
        plt.tight_layout()
        pdf.savefig()
        plt.close()

        #boxplots
        data_for_boxplot = [df[axis] for axis in axes if axis in df.columns]
        if data_for_boxplot:
            plt.figure(figsize=(6, 6))
            plt.boxplot(data_for_boxplot, labels=axes)
            plt.title(f'{sensor_name} - Boxplot of Axes')
            plt.ylabel('Value')
            plt.grid(True, axis='y')
            plt.tight_layout()
            pdf.savefig()
            plt.close()
