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
BUTTON_PIN = 2   # Digital input pin for the button
LED_PIN = 4     # Digital output pin for the LED

# Default LED on time: 300 ms (converted to seconds)
DEFAULT_LED_TIME = 0.3

class ArduinoController:
    """
    This class handles communication with the Arduino board.
    It sets up the digital input (for the button) and output (for the LED),
    and uses a callback to react when the button is pressed.
    """
    def __init__(self, led_pin, button_pin, led_off_time=DEFAULT_LED_TIME):
        self.led_pin = led_pin
        self.button_pin = button_pin
        self.led_off_time = led_off_time  # Time in seconds that LED remains on
        self.led_state = False   # Current state of the LED (True=on, False=off)
        self.button_state = False  # Current state of the button (True=pressed, False=released)
        self.board = pymata4.Pymata4()  # Create an instance of pymata4 to communicate with Arduino

        # Set LED pin as digital output
        self.board.set_pin_mode_digital_output(self.led_pin)
        # Set button pin as digital input; assign a callback for state changes
        self.board.set_pin_mode_digital_input(self.button_pin, callback=self.button_callback)

        self.led_off_timer = None  # Reference to the timer that turns off the LED

    def button_callback(self, data):
        """
        Callback function for button state changes.
        Unpacks the data received from pymata4.
        The expected data list contains at least three items:
        [pin, state, timestamp, ...]. Any extra values are ignored.
        """
        # Extended unpacking: extra values are captured in 'extra' and ignored
        pin, state, timestamp, *extra = data

        # For debugging, you might print the extra data if desired:
        # print("Extra data:", extra)

        # Check for button press (assuming active LOW: 0 means pressed)
        if state == 0 and not self.button_state:
            self.button_state = True
            print("Button pressed!")
            self.turn_led_on()
            # Cancel any previous timer and schedule LED turn off
            if self.led_off_timer is not None:
                self.led_off_timer.cancel()
            self.led_off_timer = threading.Timer(self.led_off_time, self.turn_led_off)
            self.led_off_timer.start()
        elif state == 1 and self.button_state:
            self.button_state = False
            print("Button released!")



    def turn_led_on(self):
        """Turns the LED on if it is not already on."""
        if not self.led_state:
            self.led_state = True
            self.board.digital_write(self.led_pin, 1)
            print("LED turned ON")

    def turn_led_off(self):
        """Turns the LED off if it is currently on."""
        if self.led_state:
            self.led_state = False
            self.board.digital_write(self.led_pin, 0)
            print("LED turned OFF")

    def shutdown(self):
        """Clean up: cancel any running timer and shut down the board connection."""
        if self.led_off_timer is not None:
            self.led_off_timer.cancel()
        self.board.shutdown()

class AppGUI:
    """
    This class creates the Graphical User Interface using Tkinter.
    The GUI shows the current button and LED states, and allows the user
    to adjust the LED on-time via a textbox.
    """
    def __init__(self, root, arduino_controller):
        self.root = root
        self.arduino = arduino_controller
        self.root.title("Arduino Button & LED Controller")
        self.create_widgets()
        # Begin periodic GUI updates to reflect the latest states
        self.update_gui()

    def create_widgets(self):
        """Creates and lays out the GUI widgets."""
        # Status Frame: Displays the current state of the button and LED.
        self.status_frame = ttk.Frame(self.root, padding="10")
        self.status_frame.grid(row=0, column=0, sticky="W")

        self.button_status_label = ttk.Label(self.status_frame, text="Button Status: Unknown")
        self.button_status_label.grid(row=0, column=0, sticky="W", pady=5)

        self.led_status_label = ttk.Label(self.status_frame, text="LED Status: Unknown")
        self.led_status_label.grid(row=1, column=0, sticky="W", pady=5)

        # Timer Frame: Allows user to adjust the LED on-time.
        self.timer_frame = ttk.Frame(self.root, padding="10")
        self.timer_frame.grid(row=1, column=0, sticky="W")

        ttk.Label(self.timer_frame, text="LED ON Time (ms):").grid(row=0, column=0, sticky="W")
        self.timer_entry = ttk.Entry(self.timer_frame, width=10)
        # Pre-fill with the default value converted to milliseconds
        self.timer_entry.insert(0, str(int(self.arduino.led_off_time * 1000)))
        self.timer_entry.grid(row=0, column=1, sticky="W", padx=5)

        self.set_timer_button = ttk.Button(self.timer_frame, text="Set Timer", command=self.set_timer)
        self.set_timer_button.grid(row=0, column=2, padx=5)

    def set_timer(self):
        """
        Reads the timer value from the textbox and updates the LED on-time.
        Expects the value in milliseconds.
        """
        try:
            ms_value = float(self.timer_entry.get())
            self.arduino.led_off_time = ms_value / 1000.0
            print(f"LED on time set to {self.arduino.led_off_time} seconds")
        except ValueError:
            print("Invalid timer value. Please enter a number.")

    def update_gui(self):
        """
        Updates the status labels on the GUI to reflect the current
        state of the button and LED. Called periodically using Tkinter's 'after' method.
        """
        button_state_text = "Pressed" if self.arduino.button_state else "Released"
        led_state_text = "ON" if self.arduino.led_state else "OFF"
        self.button_status_label.config(text=f"Button Status: {button_state_text}")
        self.led_status_label.config(text=f"LED Status: {led_state_text}")
        # Schedule the next update in 100 ms
        self.root.after(100, self.update_gui)

def main():
    # Instantiate the Arduino controller
    arduino_controller = ArduinoController(led_pin=LED_PIN, button_pin=BUTTON_PIN)

    # Set up the GUI
    root = tk.Tk()
    app = AppGUI(root, arduino_controller)

    try:
        root.mainloop()
    except KeyboardInterrupt:
        print("Exiting application.")
    finally:
        # Cleanly shut down communication with the Arduino board
        arduino_controller.shutdown()

if __name__ == "__main__":
    main()
