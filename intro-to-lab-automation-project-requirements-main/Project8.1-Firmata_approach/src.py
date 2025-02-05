#!/usr/bin/env python3
import tkinter as tk
from tkinter import ttk
import threading
from pymata4 import pymata4
import sys

class ArduinoGUI:
    def __init__(self, com_port="COM5"):
        self.DEFAULT_LED_TIME = 0.3
        self.BUTTON_PIN = 2
        self.LED_PIN = 4
        
        try:
            self.board = pymata4.Pymata4(com_port=com_port)
            self.setup_board()
        except Exception as e:
            sys.exit(f"Failed to connect to Arduino: {e}")
            
        self.setup_gui()
        self.led_timer = None
        
    def setup_board(self):
        self.board.set_pin_mode_digital_input(self.BUTTON_PIN, callback=self.button_press_callback)
        self.board.set_pin_mode_digital_output(self.LED_PIN)
        
    def button_press_callback(self, data):
        if len(data) >= 2:
            value = data[2] if len(data) > 2 else data[1]
        if value == 1:  # Button pressed
            self.add_log_message("Button pressed")
            self.turn_on_light()
            
            # Cancel existing timer if any
            if self.led_timer:
                self.led_timer.cancel()
                
            # Start new timer
            self.led_timer = threading.Timer(self.DEFAULT_LED_TIME, self.turn_off_light)
            self.led_timer.start()

    def turn_on_light(self):
        try:
            self.board.digital_write(self.LED_PIN, 1)
            self.add_log_message("LED turned on")
        except Exception as e:
            self.add_log_message(f"Error turning on LED: {e}")

    def turn_off_light(self):
        try:
            self.board.digital_write(self.LED_PIN, 0)
            self.add_log_message("LED turned off")
        except Exception as e:
            self.add_log_message(f"Error turning off LED: {e}")

    def set_led_time(self):
        try:
            new_time = float(self.led_time_entry.get())
            if new_time > 0:
                self.DEFAULT_LED_TIME = new_time
                self.add_log_message(f"LED time set to {new_time} seconds")
            else:
                self.add_log_message("LED time must be positive")
        except ValueError:
            self.add_log_message("Please enter a valid number")

    def setup_gui(self):
        self.root = tk.Tk()
        self.root.title("Arduino LED Control")
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

        # GUI elements
        self.button_state_label = ttk.Label(self.root, text="Button State: Released")
        self.button_state_label.grid(column=0, row=0, padx=10, pady=10)

        self.led_state_label = ttk.Label(self.root, text="LED State: Off")
        self.led_state_label.grid(column=0, row=1, padx=10, pady=10)

        ttk.Label(self.root, text="LED On Time (seconds):").grid(column=0, row=2, padx=10, pady=10)
        self.led_time_entry = ttk.Entry(self.root)
        self.led_time_entry.grid(column=1, row=2, padx=10, pady=10)
        self.led_time_entry.insert(0, str(self.DEFAULT_LED_TIME))

        ttk.Button(self.root, text="Set LED Time", command=self.set_led_time).grid(
            column=0, row=3, columnspan=2, padx=10, pady=10)

        self.log_text = tk.Text(self.root, height=10, width=50)
        self.log_text.grid(column=0, row=4, columnspan=2, padx=10, pady=10)

        self.update_gui()

    def add_log_message(self, message):
        self.log_text.insert(tk.END, f"{message}\n")
        self.log_text.see(tk.END)

    def update_gui(self):
        try:
            button_state = "Pressed" if self.board.digital_read(self.BUTTON_PIN)[0] == 1 else "Released"
            led_state = "On" if self.board.digital_read(self.LED_PIN)[0] == 1 else "Off"
            
            self.button_state_label.config(text=f"Button State: {button_state}")
            self.led_state_label.config(text=f"LED State: {led_state}")
            
        except Exception as e:
            self.add_log_message(f"Error updating GUI: {e}")
            
        self.root.after(100, self.update_gui)

    def on_closing(self):
        if self.led_timer:
            self.led_timer.cancel()
        self.board.shutdown()
        self.root.destroy()

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = ArduinoGUI()
    app.run()