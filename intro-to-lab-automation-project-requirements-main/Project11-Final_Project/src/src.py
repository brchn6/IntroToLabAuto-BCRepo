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
import signal

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
fan_state = 0     # Latest fan state

# Set up CSV file in the same directory as this script
dir_path = os.path.dirname(os.path.realpath(__file__))
csv_file_path = os.path.join(dir_path, "data_log.csv")
csv_file = open(csv_file_path, "w", newline="")
csv_writer = csv.writer(csv_file)
csv_writer.writerow(["Time (ms)", "Angle (deg)", "Buzzer State", "Fan State"])

# Global serial object
ser = None

# Flag to control the serial reading thread
running = True

# -------------------------------
# Serial Reading Function
# -------------------------------
def read_serial():
    global buzzer_state, fan_state, running, ser
    try:
        # Open the serial port and store the object globally
        ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)
        time.sleep(2)  # Wait for the serial connection to initialize
        while running:
            line = ser.readline().decode('utf-8').strip()
            if line:
                try:
                    # Expected CSV format: time,angle,buzzerState,fanState
                    parts = line.split(',')
                    if len(parts) == 4:
                        t_val = int(parts[0])
                        angle_val = int(parts[1])
                        buzzer_val = int(parts[2])
                        fan_val = int(parts[3])
                        
                        # Append new values to our data deques
                        time_data.append(t_val)
                        angle_data.append(angle_val)
                        
                        # Update state variables
                        buzzer_state = buzzer_val
                        fan_state = fan_val
                        
                        # Log the data to CSV
                        csv_writer.writerow([t_val, angle_val, buzzer_val, fan_val])
                        
                        # Update the GUI elements
                        update_plot()
                        update_led()
                        update_fan()
                except Exception as e:
                    print("Error parsing line:", line, e)
    except Exception as e:
        print("Error opening serial port:", e)

# -------------------------------
# GUI Update Functions
# -------------------------------
def update_plot():
    try:
        ax.cla()
        ax.plot(list(time_data), list(angle_data), marker='o', linestyle='-')
        ax.set_xlabel("Time (ms)")
        ax.set_ylabel("Angle (deg)")
        ax.set_title("Servo Angle Over Time")
        ax.grid(True)
        canvas.draw()
    except tk.TclError:
        # Likely the widget was destroyed
        pass

def update_led():
    try:
        # Update the buzzer LED indicator: Red means ON, Green means OFF
        if buzzer_state == 1:
            led_label.config(bg="red")
        else:
            led_label.config(bg="green")
    except tk.TclError:
        pass

def update_fan():
    try:
        # Update the fan LED indicator: Green means ON, Red means OFF
        if fan_state == 1:
            fan_led_label.config(bg="green")
        else:
            fan_led_label.config(bg="red")
    except tk.TclError:
        pass

def on_closing():
    """Cleanup routine to stop threads, close files, and destroy the GUI."""
    global running
    running = False
    # Allow the serial thread to finish up
    time.sleep(0.5)
    csv_file.close()
    if root.winfo_exists():
        root.destroy()

def signal_handler(sig, frame):
    """Handle Ctrl+C (SIGINT) gracefully."""
    print("Ctrl+C detected, exiting gracefully...")
    on_closing()

# -------------------------------
# Main Function
# -------------------------------
def main():
    global root, led_label, fan_led_label, ax, canvas, serial_thread, ser

    # Set up the signal handler for Ctrl+C
    signal.signal(signal.SIGINT, signal_handler)

    # -------------------------------
    # Set Up the Tkinter GUI
    # -------------------------------
    root = tk.Tk()
    root.title("Servo Angle, Buzzer & Fan Monitor")

    # Buzzer state LED indicator
    led_frame = tk.Frame(root)
    led_frame.pack(pady=10)
    tk.Label(led_frame, text="Buzzer State:").pack(side=tk.LEFT)
    led_label = tk.Label(led_frame, text="    ", bg="green", relief="sunken")
    led_label.pack(side=tk.LEFT)

    # Fan state LED indicator
    fan_led_frame = tk.Frame(root)
    fan_led_frame.pack(pady=10)
    tk.Label(fan_led_frame, text="Fan State:").pack(side=tk.LEFT)
    fan_led_label = tk.Label(fan_led_frame, text="    ", bg="green", relief="sunken")
    fan_led_label.pack(side=tk.LEFT)

    # Create a matplotlib figure for the angle plot
    fig, ax = plt.subplots(figsize=(8, 4))
    canvas = FigureCanvasTkAgg(fig, master=root)
    canvas_widget = canvas.get_tk_widget()
    canvas_widget.pack()

    # Start the serial reading thread (set as daemon so it exits when the main thread exits)
    serial_thread = threading.Thread(target=read_serial, daemon=True)
    serial_thread.start()

    # Set up a protocol to handle window closing properly
    root.protocol("WM_DELETE_WINDOW", on_closing)
    
    # Start the Tkinter event loop
    try:
        root.mainloop()
    except KeyboardInterrupt:
        # In some environments, Ctrl+C may trigger a KeyboardInterrupt
        on_closing()

    # Send signal to Arduino to close the board and turn off the fan
    try:
        if ser is not None and ser.is_open:
            ser.write(b'0')  # Send a signal to Arduino to turn off the fan
            ser.close()      # Close the serial port
    except Exception as e:
        print("Error sending close signal to Arduino:", e)

# -------------------------------
# Entry Point
# -------------------------------
if __name__ == '__main__':
    main()



"""
To run this script, you can use a command like:

conda activate intro
python intro-to-lab-automation-project-requirements-main/Project11-Final_Project/src/src.py


This updated code now keeps track of the fan state info sent from the ino code.
"""
