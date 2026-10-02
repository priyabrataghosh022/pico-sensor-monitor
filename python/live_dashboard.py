import serial
import time
from collections import deque
import matplotlib.pyplot as plt
import matplotlib.animation as animation

# --- CONFIGURATION ---
PORT = 'COM12'        # Pico's COM port
BAUD_RATE = 115200
MAX_SAMPLES = 100     # Display rolling window of 100 data points

# --- DATA BUFFERS ---
t_data = deque(maxlen=MAX_SAMPLES)

ax_data = deque(maxlen=MAX_SAMPLES)
ay_data = deque(maxlen=MAX_SAMPLES)
az_data = deque(maxlen=MAX_SAMPLES)

gx_data = deque(maxlen=MAX_SAMPLES)
gy_data = deque(maxlen=MAX_SAMPLES)
gz_data = deque(maxlen=MAX_SAMPLES)

# --- SERIAL CONNECTION ---
try:
    ser = serial.Serial(PORT, BAUD_RATE, timeout=1)
    time.sleep(2)
    ser.reset_input_buffer()

    print(f"Connected to Pico on {PORT}")

except serial.SerialException as e:
    print(f"Error opening {PORT}: {e}")
    exit()

# --- PLOT LAYOUT (2 ROWS x 3 COLUMNS) ---
fig, axes = plt.subplots(
    2,
    3,
    figsize=(14, 7),
    sharex=True
)

fig.suptitle(
    'MPU6050 Real-Time Sensor Stream (Separate Channels)',
    fontsize=14,
    fontweight='bold'
)

# Unpack subplot grid
(ax_x, ax_y, ax_z), (gx_x, gx_y, gx_z) = axes

# --- CREATE INDIVIDUAL LINES ---
line_ax, = ax_x.plot(
    [], [], color='red', linewidth=1.5, label='Ax'
)

line_ay, = ax_y.plot(
    [], [], color='green', linewidth=1.5, label='Ay'
)

line_az, = ax_z.plot(
    [], [], color='blue', linewidth=1.5, label='Az'
)

line_gx, = gx_x.plot(
    [], [], color='orange', linewidth=1.5, label='Gx'
)

line_gy, = gx_y.plot(
    [], [], color='purple', linewidth=1.5, label='Gy'
)

line_gz, = gx_z.plot(
    [], [], color='darkcyan', linewidth=1.5, label='Gz'
)

# --- SUBPLOT TITLES AND LABELS ---
titles = [
    (ax_x, 'Accel X (g)', 'g'),
    (ax_y, 'Accel Y (g)', 'g'),
    (ax_z, 'Accel Z (g)', 'g'),

    (gx_x, 'Gyro X (°/s)', '°/s'),
    (gx_y, 'Gyro Y (°/s)', '°/s'),
    (gx_z, 'Gyro Z (°/s)', '°/s')
]

for sub_ax, title, ylabel in titles:
    sub_ax.set_title(title, fontsize=10)
    sub_ax.set_ylabel(ylabel)
    sub_ax.grid(True, linestyle='--', alpha=0.6)

# X-axis labels
gx_x.set_xlabel('Time (s)')
gx_y.set_xlabel('Time (s)')
gx_z.set_xlabel('Time (s)')


# --- ANIMATION UPDATE LOOP ---
def update(frame):

    while ser.in_waiting > 0:

        line = ser.readline().decode(
            'utf-8',
            errors='ignore'
        ).strip()

        parts = line.split(',')

        # Expected:
        # timestamp, ax, ay, az, gx, gy, gz
        if len(parts) == 7:

            try:
                # Convert incoming strings to float
                t = float(parts[0])

                ax_v = float(parts[1])
                ay_v = float(parts[2])
                az_v = float(parts[3])

                gx_v = float(parts[4])
                gy_v = float(parts[5])
                gz_v = float(parts[6])

                # Store data
                t_data.append(t)

                ax_data.append(ax_v)
                ay_data.append(ay_v)
                az_data.append(az_v)

                gx_data.append(gx_v)
                gy_data.append(gy_v)
                gz_data.append(gz_v)

            except ValueError:
                # Ignore corrupted/non-numeric data
                continue

    # Update graphs if data exists
    if len(t_data) > 0:

        # Update line data
        line_ax.set_data(t_data, ax_data)
        line_ay.set_data(t_data, ay_data)
        line_az.set_data(t_data, az_data)

        line_gx.set_data(t_data, gx_data)
        line_gy.set_data(t_data, gy_data)
        line_gz.set_data(t_data, gz_data)

        # --- DYNAMIC AXIS SCALING ---
        all_subplots = [
            (ax_x, ax_data),
            (ax_y, ay_data),
            (ax_z, az_data),

            (gx_x, gx_data),
            (gx_y, gy_data),
            (gx_z, gz_data)
        ]

        # Time axis
        if len(t_data) > 1:
            sub_ax_xlim_min = min(t_data)
            sub_ax_xlim_max = max(t_data) + 0.1

            for sub_ax, data_buf in all_subplots:
                sub_ax.set_xlim(
                    sub_ax_xlim_min,
                    sub_ax_xlim_max
                )

        # Y-axis
        for sub_ax, data_buf in all_subplots:

            if len(data_buf) > 0:

                y_min = min(data_buf)
                y_max = max(data_buf)

                # Prevent zero-height axis
                if y_min == y_max:
                    padding = 0.1
                else:
                    padding = max(
                        0.1,
                        (y_max - y_min) * 0.2
                    )

                sub_ax.set_ylim(
                    y_min - padding,
                    y_max + padding
                )

    return (
        line_ax,
        line_ay,
        line_az,
        line_gx,
        line_gy,
        line_gz
    )


# --- START ANIMATION ---
ani = animation.FuncAnimation(
    fig,
    update,
    interval=20,
    blit=False
)

# Adjust layout
plt.tight_layout()

# Display plots
plt.show()

# --- CLOSE SERIAL CONNECTION ---
ser.close()

print("Serial connection closed.")