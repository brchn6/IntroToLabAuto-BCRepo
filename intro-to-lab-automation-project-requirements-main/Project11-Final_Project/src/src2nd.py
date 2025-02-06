import serial
import csv
import time
from collections import deque
import matplotlib.pyplot as plt
import matplotlib.animation as animation

# ======= CONFIGURATION =======
SERIAL_PORT = "COM5"       # Change this to your Arduino serial port (e.g., "/dev/ttyUSB0" on Linux)
BAUD_RATE = 9600           # Must match the Arduino Serial.begin() baud rate
CSV_FILENAME = "data_log.csv"  # Output CSV file name

# ======= SET UP SERIAL =======
try:
    ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)
    # Wait a moment for the serial connection to initialize
    time.sleep(2)
    print(f"Connected to {SERIAL_PORT} at {BAUD_RATE} baud.")
except serial.SerialException as e:
    print("Error opening serial port: ", e)
    exit(1)

# ======= SET UP CSV LOGGING =======
csv_file = open(CSV_FILENAME, mode='w', newline='')
csv_writer = csv.writer(csv_file)
# Write CSV header: Time (ms), Angle (degrees), Buzzer (0=OFF, 1=ON)
csv_writer.writerow(["Time (ms)", "Angle (degrees)", "Buzzer"])

# ======= SET UP DATA CONTAINERS =======
# Using deque so that the plot shows only the most recent data (max 100 points)
times = deque(maxlen=100)
angles = deque(maxlen=100)
buzzer_states = deque(maxlen=100)

# ======= SET UP THE MATPLOTLIB FIGURE =======
fig, (ax_angle, ax_buzzer) = plt.subplots(2, 1, figsize=(10, 8))

# --- Angle plot ---
angle_line, = ax_angle.plot([], [], lw=2, color="blue")
ax_angle.set_title("Real-time Servo Angle")
ax_angle.set_xlabel("Time (ms)")
ax_angle.set_ylabel("Angle (degrees)")
ax_angle.set_ylim(0, 180)
ax_angle.grid(True)

# --- Buzzer indicator ---
# We’ll simply show a text indicator in a separate axis (with no ticks)
ax_buzzer.axis("off")
buzzer_text = ax_buzzer.text(0.5, 0.5, "", fontsize=30, ha='center', va='center')

# ======= UPDATE FUNCTION FOR THE ANIMATION =======
def update(frame):
    # Read all available lines from serial
    while ser.in_waiting:
        try:
            # Read a line and decode from bytes to string
            line_str = ser.readline().decode('utf-8').strip()
            if line_str:
                # Expected CSV format: time, angle, buzzer, fan (we use the first three)
                parts = line_str.split(',')
                if len(parts) >= 3:
                    t = int(parts[0])
                    angle = int(parts[1])
                    buzzer = int(parts[2])
                    
                    # Append the new data to the deques
                    times.append(t)
                    angles.append(angle)
                    buzzer_states.append(buzzer)
                    
                    # Log the data to the CSV file
                    csv_writer.writerow([t, angle, buzzer])
        except Exception as e:
            print("Error reading/parsing serial data:", e)
    
    # --- Update the angle plot ---
    if times:
        # Adjust the x-axis to show recent data
        ax_angle.set_xlim(times[0], times[-1] + 100)
        angle_line.set_data(times, angles)
    
    # --- Update the buzzer indicator ---
    if buzzer_states and buzzer_states[-1] == 1:
        buzzer_text.set_text("Buzzer ON")
        buzzer_text.set_color("red")
    else:
        buzzer_text.set_text("Buzzer OFF")
        buzzer_text.set_color("green")
    
    return angle_line, buzzer_text

# ======= CREATE THE ANIMATION =======
ani = animation.FuncAnimation(fig, update, interval=100, blit=True)

# ======= SHOW THE GUI =======
plt.tight_layout()
plt.show()

# ======= CLEAN UP =======
print("Closing CSV file and serial connection.")
csv_file.close()
ser.close()


# """
# To run this script, you can use a command like:

# conda activate intro
# python C:\Users\itclass11\Desktop\IntroToLabAuto-BCRepo\intro-to-lab-automation-project-requirements-main\Project11-Final_Project\src\src2nd.py
# This updated code now keeps track of the fan state info sent from the ino code
# """