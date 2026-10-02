import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Load logged CSV dataset
df = pd.read_csv('../data/stationary_noise.csv')

# Calculate Moving Average Filter (Window size = 10 samples)
window_size = 10
df['ax_filtered'] = df['ax'].rolling(window=window_size, min_periods=1).mean()

# Statistical Noise Analysis
raw_std = df['ax'].std()
filtered_std = df['ax_filtered'].std()

print(f"Raw Acceleration Std Dev (Noise Level): {raw_std:.5f} g")
print(f"Filtered Acceleration Std Dev:          {filtered_std:.5f} g")

# Plot Raw vs Filtered Signal
plt.figure(figsize=(10, 5))
plt.plot(df['timestamp'], df['ax'], label='Raw Ax Signal', alpha=0.5, color='orange')
plt.plot(df['timestamp'], df['ax_filtered'], label=f'{window_size}-Sample Moving Avg', color='blue', linewidth=2)

plt.title('MPU6050 Acceleration Signal: Raw vs Filtered')
plt.xlabel('Time (seconds)')
plt.ylabel('Acceleration X (g)')
plt.legend()
plt.grid(True)
plt.show()