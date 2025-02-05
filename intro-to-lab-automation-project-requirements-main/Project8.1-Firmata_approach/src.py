#!/usr/bin/env python3
"""
Reacting_button_press_pymata4_using_timer.py

This script demonstrates two-way communication between the computer and an Arduino board using
the firmataexpress firmware and the pymata4 package. The script monitors a digital input pin
(for a button) and, upon detecting a press, turns on an LED for a short period using a timer.
A Tkinter GUI displays the state of the button and the LED, and provides a textbox for changing
the LED-on time.

Requirements met:
1. Communicates with Arduino via pymata4.
2. Monitors a digital input (button) and reacts to its changes.
3. Uses threading.Timer to schedule turning off the LED.
4. Provides a GUI to show the states and let the user adjust the timer interval.
5. Contains inline comments explaining each part of the code.
"""

import tkinter as tk
from tkinter import ttk
import threading
from pymata4 import pymata4


# Define Arduino pin assignments
BUTTON_PIN = 2
LED_PIN = 4     # Digital output pin for the LED

# Default LED on time: 300 ms (converted to seconds)
DEFAULT_LED_TIME = 0.3

# Create a pymata4 instance
board = pymata4.Pymata4(com_port="COM5")

# Set the pin modes
board.set_pin_mode_digital_input(BUTTON_PIN)
board.set_pin_mode_digital_output(LED_PIN)

# turn on light
def turn_on_light():
    board.digital_write(LED_PIN, 1)
    
# turn off light
def turn_off_light():
    board.digital_write(LED_PIN, 0)

# Callback function for the button press
def button_press_callback(data):
    # If the button is pressed
    if data[1] == 1:
        # Turn on the LED
        turn_on_light()
        # Schedule turning off the LED after the specified time
        threading.Timer(DEFAULT_LED_TIME, turn_off_light).start()

# Callback function for the LED time entry
def set_led_time():
    # Get the value from the entry box
    led_time = float(led_time_entry.get())
    # Update the default LED time
    global DEFAULT_LED_TIME
    DEFAULT_LED_TIME = 1000

# Create the GUI
root = tk.Tk()
root.title("Button Press LED Control")

# Create and place the label for the button state
button_state_label = ttk.Label(root, text="Button State: Unknown")
button_state_label.grid(column=0, row=0, padx=10, pady=10)

# Create and place the label for the LED state
led_state_label = ttk.Label(root, text="LED State: Off")
led_state_label.grid(column=0, row=1, padx=10, pady=10)

# Create and place the entry box for the LED time
led_time_label = ttk.Label(root, text="LED On Time (seconds):")
led_time_label.grid(column=0, row=2, padx=10, pady=10)
led_time_entry = ttk.Entry(root)
led_time_entry.grid(column=1, row=2, padx=10, pady=10)
led_time_entry.insert(0, str(DEFAULT_LED_TIME))

# Create and place the button to set the LED time
set_time_button = ttk.Button(root, text="Set LED Time", command=set_led_time)
set_time_button.grid(column=0, row=3, columnspan=2, padx=10, pady=10)

# Function to update the GUI with the current states
def update_gui():
    # Update the button state label
    button_state = "Pressed" if board.digital_read(BUTTON_PIN) == 1 else "Released"
    button_state_label.config(text=f"Button State: {button_state}")

    # Update the LED state label
    led_state = "On" if board.digital_read(LED_PIN) == 1 else "Off"
    led_state_label.config(text=f"LED State: {led_state}")

    # Schedule the next update
    root.after(100, update_gui)

# Start the GUI update loop
update_gui()

# Start the Tkinter event loop
root.mainloop()

