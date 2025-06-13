import os
import pandas as pd
import numpy as np
from scipy.fft import fft

SAMPLE_RATE = 60  
WINDOW_SIZE = 300  
#sitting, bus 600 10sec
#walking, biking, walking 300 5sec
#stairs 120 2sec

all_sensors = {
    "Accelerometer.csv": ["X (m/s^2)", "Y (m/s^2)", "Z (m/s^2)"],
    "Gyroscope.csv": ["X (rad/s)", "Y (rad/s)", "Z (rad/s)"],
    "Linear Accelerometer.csv": ["X (m/s^2)", "Y (m/s^2)", "Z (m/s^2)"],
}

def extract_features_from_file(file_name, axes):
    df = pd.read_csv(file_name, sep=";")
    features = []

    time_column = df.columns[0]  
    time_values = df[time_column].dropna().values

    for axis in axes:
        signal = df[axis].dropna().values

        for start in range(0, len(signal) - WINDOW_SIZE, WINDOW_SIZE):
            segment = signal[start:start + WINDOW_SIZE]
            segment_time = time_values[start:start + WINDOW_SIZE]

            if len(segment) < WINDOW_SIZE or len(segment_time) < WINDOW_SIZE:
                continue

            row = {
                "sensor": file_name,
                "axis": axis,
                "start_time": segment_time[0],
                "end_time": segment_time[-1],
                "start_idx": start,
                "end_idx": start + WINDOW_SIZE,
                "mean": np.mean(segment),
                "std": np.std(segment),
                "min": np.min(segment),
                "max": np.max(segment),
                "range": np.ptp(segment),
                "median": np.median(segment),
                "variance": np.var(segment)
            }

            # Frequency domain
            fft_result = fft(segment)
            freqs = np.fft.fftfreq(len(segment), d=1 / SAMPLE_RATE)
            amplitudes = np.abs(fft_result)

            pos_mask = freqs > 0
            freqs = freqs[pos_mask]
            amplitudes = amplitudes[pos_mask]

            if len(freqs) == 0:
                continue

            row["dominant_freq"] = freqs[np.argmax(amplitudes)]
            row["spectral_centroid"] = np.sum(freqs * amplitudes) / np.sum(amplitudes)
            # print(row)
            features.append(row)

    return features

all_features = []
files = ["Accelerometer.csv", "Gyroscope.csv", "Linear Accelerometer.csv"]
print("start")

for file in files:
    axes = all_sensors[file]
    file_features = extract_features_from_file(file, axes)
    for f in file_features:
        f["sensor"] = file.replace(".csv", "")
    all_features.extend(file_features)

features_df = pd.DataFrame(all_features)
features_df.to_csv("features_per_activity.csv", index=False)
print("klaar")
