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
INTERRUPT_PIN = 2  # Interrupt pin for the button

# Default LED on time: 300 ms (converted to seconds)
DEFAULT_LED_TIME = 0.3

# Create a pymata4 instance
board = pymata4.Pymata4("COM5")

