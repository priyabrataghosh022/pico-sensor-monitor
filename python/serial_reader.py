import serial
import csv
import time

# --- CONFIGURATION ---
PORT = 'COM12'         # Change to your Pico's port (e.g., 'COM4', '/dev/ttyACM0')
BAUD_RATE = 115200    # Default USB serial speed
OUTPUT_FILE = '../data/stationary_noise.csv'
MAX_SAMPLES = 500     # Collects 500 lines (5 seconds at 100 Hz)

print(f"Connecting to {PORT}...")

try:
    ser = serial.Serial(PORT, BAUD_RATE, timeout=2)
    time.sleep(2)  # Wait for serial connection to stabilize
    ser.reset_input_buffer()
    
    with open(OUTPUT_FILE, mode='w', newline='') as file:
        writer = csv.writer(file)
        # Write CSV Header
        writer.writerow(['timestamp', 'ax', 'ay', 'az', 'gx', 'gy', 'gz'])
        
        sample_count = 0
        print(f"Logging data to {OUTPUT_FILE}. Keep sensor stationary...")
        
        while sample_count < MAX_SAMPLES:
            if ser.in_waiting > 0:
                line = ser.readline().decode('utf-8', errors='ignore').strip()
                parts = line.split(',')
                
                # Verify packet structure (7 values: time, ax, ay, az, gx, gy, gz)
                if len(parts) == 7:
                    try:
                        data = [float(p) for p in parts]
                        writer.writerow(data)
                        sample_count += 1
                        print(f"Sample {sample_count}/{MAX_SAMPLES}: {data}")
                    except ValueError:
                        continue  # Skip corrupted rows

    ser.close()
    print(f"\nData collection complete! Saved to {OUTPUT_FILE}")

except serial.SerialException as e:
    print(f"Error opening serial port: {e}")