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
from matplotlib.animation import FuncAnimation

# -------------------------------
# Configuration Parameters
# -------------------------------
SERIAL_PORT = 'COM5'
BAUD_RATE = 9600
MAX_DATA_POINTS = 100
UPDATE_INTERVAL = 100  # Update plot every 100ms

# -------------------------------
# Data Storage and CSV Setup
# -------------------------------
time_data = deque(maxlen=MAX_DATA_POINTS)
angle_data = deque(maxlen=MAX_DATA_POINTS)
buzzer_state = 0
fan_state = 0

# Set up CSV file
dir_path = os.path.dirname(os.path.realpath(__file__))
csv_file_path = os.path.join(dir_path, "data_log.csv")
csv_file = open(csv_file_path, "w", newline="")
csv_writer = csv.writer(csv_file)
csv_writer.writerow(["Time (ms)", "Angle (deg)", "Buzzer State", "Fan State"])

# Global variables
ser = None
running = True
plot_pause = False

def cleanup():
    """Comprehensive cleanup function"""
    global running, ser, csv_file
    print("Performing cleanup...")
    running = False
    
    # Stop the fan
    try:
        if ser and ser.is_open:
            ser.write(b'F0')
            time.sleep(0.1)  # Give time for the command to be sent
            ser.close()
            print("Serial port closed and fan stopped")
    except Exception as e:
        print(f"Error during serial cleanup: {e}")

    # Close CSV file
    try:
        if not csv_file.closed:
            csv_file.close()
            print("CSV file closed")
    except Exception as e:
        print(f"Error closing CSV file: {e}")

def read_serial():
    """Enhanced serial reading function with better error handling"""
    global buzzer_state, fan_state, running, ser
    
    while running:
        try:
            if not ser or not ser.is_open:
                ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)
                time.sleep(2)
                print("Serial connection established")
                
            line = ser.readline().decode('utf-8').strip()
            if line:
                parts = line.split(',')
                if len(parts) == 4:
                    t_val = int(parts[0])
                    angle_val = int(parts[1])
                    buzzer_val = int(parts[2])
                    fan_val = int(parts[3])
                    
                    time_data.append(t_val)
                    angle_data.append(angle_val)
                    buzzer_state = buzzer_val
                    fan_state = fan_val
                    
                    csv_writer.writerow([t_val, angle_val, buzzer_val, fan_val])
                    
                    # Update GUI elements
                    root.after(0, update_led)
                    root.after(0, update_fan)
                    
        except serial.SerialException as e:
            print(f"Serial error: {e}")
            time.sleep(1)  # Wait before retrying
        except Exception as e:
            print(f"Error in serial reading: {e}")
            time.sleep(1)

def update_plot(frame):
    """Improved plot update function with better styling"""
    if not plot_pause and len(time_data) > 0:
        ax.clear()
        
        # Plot with improved styling
        ax.plot(list(time_data), list(angle_data), 
                color='#2196F3', 
                linewidth=2, 
                marker='o',
                markersize=4,
                markerfacecolor='white',
                markeredgecolor='#2196F3')
        
        # Customize grid
        ax.grid(True, linestyle='--', alpha=0.7)
        
        # Customize labels and title
        ax.set_xlabel("Time (ms)", fontsize=10, fontweight='bold')
        ax.set_ylabel("Angle (degrees)", fontsize=10, fontweight='bold')
        ax.set_title("Servo Angle Monitor", fontsize=12, fontweight='bold', pad=10)
        
        # Add range indicators
        ax.axhline(y=0, color='#FF9800', linestyle='--', alpha=0.5)
        ax.axhline(y=180, color='#FF9800', linestyle='--', alpha=0.5)
        
        # Set y-axis limits with some padding
        ax.set_ylim(-10, 190)
        
        # Customize appearance
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        
        # Add legend
        ax.legend(['Servo Angle'], loc='upper right')

def update_led():
    """Update buzzer LED indicator"""
    try:
        color = "red" if buzzer_state == 1 else "green"
        led_label.config(bg=color)
    except tk.TclError:
        pass

def update_fan():
    """Update fan LED indicator"""
    try:
        color = "green" if fan_state == 1 else "red"
        fan_led_label.config(bg=color)
    except tk.TclError:
        pass

def toggle_plot():
    """Toggle plot updates"""
    global plot_pause
    plot_pause = not plot_pause

def on_closing():
    """Enhanced cleanup routine for window closing"""
    if tk.messagebox.askokcancel("Quit", "Do you want to quit?"):
        cleanup()
        root.quit()
        root.destroy()

def signal_handler(sig, frame):
    """Enhanced signal handler for Ctrl+C"""
    print("\nCtrl+C detected, performing cleanup...")
    cleanup()
    os._exit(0)

def create_gui():
    """Create the main GUI with improved styling"""
    global root, led_label, fan_led_label, ax, canvas
    
    root = tk.Tk()
    root.title("Servo Angle Monitor")
    root.geometry("800x600")
    
    # Create main container
    main_frame = ttk.Frame(root, padding="10")
    main_frame.pack(fill=tk.BOTH, expand=True)
    
    # Status indicators frame
    status_frame = ttk.LabelFrame(main_frame, text="Status Indicators", padding="5")
    status_frame.pack(fill=tk.X, pady=(0, 10))
    
    # Buzzer indicator
    buzzer_frame = ttk.Frame(status_frame)
    buzzer_frame.pack(side=tk.LEFT, padx=10)
    ttk.Label(buzzer_frame, text="Buzzer:").pack(side=tk.LEFT, padx=(0, 5))
    led_label = tk.Label(buzzer_frame, width=2, height=1, bg="green", relief="sunken")
    led_label.pack(side=tk.LEFT)
    
    # Fan indicator
    fan_frame = ttk.Frame(status_frame)
    fan_frame.pack(side=tk.LEFT, padx=10)
    ttk.Label(fan_frame, text="Fan:").pack(side=tk.LEFT, padx=(0, 5))
    fan_led_label = tk.Label(fan_frame, width=2, height=1, bg="red", relief="sunken")
    fan_led_label.pack(side=tk.LEFT)
    
    # Plot frame
    plot_frame = ttk.Frame(main_frame)
    plot_frame.pack(fill=tk.BOTH, expand=True)
    
    # Create matplotlib figure
    fig, ax = plt.subplots(figsize=(8, 4), dpi=100)
    canvas = FigureCanvasTkAgg(fig, master=plot_frame)
    canvas.draw()
    canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
    
    # Control buttons
    button_frame = ttk.Frame(main_frame)
    button_frame.pack(fill=tk.X, pady=(10, 0))
    
    ttk.Button(button_frame, text="Pause/Resume", command=toggle_plot).pack(side=tk.LEFT, padx=5)
    
    return fig, ax

def main():
    """Main application function"""
    global root, fig, ax
    
    # Set up signal handler
    signal.signal(signal.SIGINT, signal_handler)
    
    # Create GUI
    fig, ax = create_gui()
    
    # Set up animation
    ani = FuncAnimation(fig, update_plot, interval=UPDATE_INTERVAL, cache_frame_data=False)
    
    # Start serial reading thread
    serial_thread = threading.Thread(target=read_serial, daemon=True)
    serial_thread.start()
    
    # Set up window close handler
    root.protocol("WM_DELETE_WINDOW", on_closing)
    
    # Start main loop
    try:
        root.mainloop()
    except KeyboardInterrupt:
        cleanup()
        os._exit(0)

if __name__ == '__main__':
    main()
    
"""
To run this script, you can use a command like:

conda activate intro
python intro-to-lab-automation-project-requirements-main/Project11-Final_Project/src/src.py


This updated code now keeps track of the fan state info sent from the ino code.
"""
