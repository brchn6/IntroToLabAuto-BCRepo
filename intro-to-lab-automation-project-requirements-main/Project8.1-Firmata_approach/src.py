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
BUTTON_PIN = 6   # Digital input pin for the button
LED_PIN = 4     # Digital output pin for the LED

# Default LED on time: 300 ms (converted to seconds)
DEFAULT_LED_TIME = 0.3

# Create a pymata4 instance
board = pymata4.Pymata4()

# Set the pin modes
board.set_pin_mode(BUTTON_PIN, board.INPUT, board.DIGITAL)

# Set the LED pin to output mode
board.set_pin_mode(LED_PIN, board.OUTPUT, board.DIGITAL)

# tkinter GUI setup
root = tk.Tk()
root.title("Button Press Reaction")
root.geometry("300x200")

# Create a label for the button state
button_label = ttk.Label(root, text="Button: ")
button_label.pack()

# Create a label for the LED state
led_label = ttk.Label(root, text="LED: Off")
led_label.pack()

# Create a label for the LED time
time_label = ttk.Label(root, text="LED On Time (s):")
time_label.pack()

# Create a textbox for the LED time
time_entry = ttk.Entry(root)
time_entry.insert(0, str(DEFAULT_LED_TIME))
time_entry.pack()

# Function to turn on the LED
def turn_on_led():
    board.digital_write(LED_PIN, 1)
    led_label.config(text="LED: On")

# Function to turn off the LED
def turn_off_led():
    board.digital_write(LED_PIN, 0)
    led_label.config(text="LED: Off")

# Function to handle button press
def button_press_handler(pin_val):
    if pin_val == 1:
        turn_on_led()
        led_time = float(time_entry.get())
        timer = threading.Timer(led_time, turn_off_led)
        timer.start()

# Function to update the button state
def update_button_state():
    button_state = board.digital_read(BUTTON_PIN)
    button_label.config(text=f"Button: {button_state}")
    button_press_handler(button_state)
    root.after(100, update_button_state)

# Start the button state update loop
update_button_state()

# Start the tkinter main loop
root.mainloop()

# Clean up the board
board.shutdown()
