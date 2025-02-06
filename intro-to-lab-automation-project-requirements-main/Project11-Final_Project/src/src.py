import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import serial
import threading
import csv
import time
from collections import deque
import os

# -------------------------------
# Configuration Parameters
# -------------------------------
SERIAL_PORT = 'COM5' 
BAUD_RATE = 9600
MAX_DATA_POINTS = 100  # Maximum number of data points to display on the graph

# -------------------------------
# Data Storage and CSV Setup
# -------------------------------
time_data = deque(maxlen=MAX_DATA_POINTS)
angle_data = deque(maxlen=MAX_DATA_POINTS)
buzzer_state = 0  # Latest buzzer state

# Open CSV file to log data
# dir to save 
dir_path = os.path.dirname(os.path.realpath(__file__))
csv_file_path = os.path.join(dir_path, "data_log.csv")
csv_file = open(csv_file_path, "w", newline="")
csv_writer = csv.writer(csv_file)
csv_writer.writerow(["Time (ms)", "Angle (deg)", "Buzzer State"])

# Flag to control the serial reading thread
running = True

# -------------------------------
# Serial Reading Function
# -------------------------------
def read_serial():
    global buzzer_state
    try:
        ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)
        time.sleep(2)  # Wait for the serial connection to initialize
        while running:
            line = ser.readline().decode('utf-8').strip()
            if line:
                try:
                    # Expected CSV format: time,angle,buzzerState
                    parts = line.split(',')
                    if len(parts) == 3:
                        t_val = int(parts[0])
                        angle_val = int(parts[1])
                        buzzer_val = int(parts[2])
                        # Append new values to our data deques
                        time_data.append(t_val)
                        angle_data.append(angle_val)
                        buzzer_state = buzzer_val
                        # Log the data to CSV
                        csv_writer.writerow([t_val, angle_val, buzzer_val])
                        # Update the GUI elements
                        update_plot()
                        update_led()
                except Exception as e:
                    print("Error parsing line:", line, e)
    except Exception as e:
        print("Error opening serial port:", e)

# -------------------------------
# GUI Update Functions
# -------------------------------
def update_plot():
    # Clear and redraw the plot with the latest data
    ax.cla()
    ax.plot(list(time_data), list(angle_data), marker='o', linestyle='-')
    ax.set_xlabel("Time (ms)")
    ax.set_ylabel("Angle (deg)")
    ax.set_title("Servo Angle Over Time")
    canvas.draw()

def update_led():
    # Update the LED indicator color based on buzzer state
    # Green indicates buzzer OFF, Red indicates buzzer ON
    if buzzer_state == 1:
        led_label.config(bg="red")
    else:
        led_label.config(bg="green")

def on_closing():
    global running
    running = False
    time.sleep(0.5)  # Give the serial thread time to finish
    csv_file.close()
    root.destroy()

# -------------------------------
# Set Up the Tkinter GUI
# -------------------------------
root = tk.Tk()
root.title("Servo Angle & Buzzer Monitor")

# LED indicator for buzzer state
led_frame = tk.Frame(root)
led_frame.pack(pady=10)
tk.Label(led_frame, text="Buzzer State:").pack(side=tk.LEFT)
led_label = tk.Label(led_frame, text="    ", bg="green", relief="sunken")
led_label.pack(side=tk.LEFT)

# Create a matplotlib figure for the angle plot
fig, ax = plt.subplots(figsize=(50, 40))
canvas = FigureCanvasTkAgg(fig, master=root)
canvas_widget = canvas.get_tk_widget()
canvas_widget.pack()

# Start the serial reading thread
serial_thread = threading.Thread(target=read_serial, daemon=True)
serial_thread.start()

# Set up a protocol to handle window closing properly
root.protocol("WM_DELETE_WINDOW", on_closing)
root.mainloop()

"""
conda activate intro
python intro-to-lab-automation-project-requirements-main/Project11-Final_Project/src/src.py
"""