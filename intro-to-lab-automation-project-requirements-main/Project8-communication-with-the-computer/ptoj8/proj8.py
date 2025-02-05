#!/usr/bin/env python3
"""
Project 8: Two-way communication between computer and Arduino
This script creates a GUI to control an Arduino's LED duration and monitor its state.
"""

import PySimpleGUI as sg
import serial
import threading
import queue
import time

def read_serial(ser, output_queue):
    """
    Continuously reads data from the serial port in a separate thread.
    
    Args:
        ser (serial.Serial): Serial port connection
        output_queue (queue.Queue): Thread-safe queue for serial data
    """
    while True:
        try:
            if ser.in_waiting:
                # Read and decode data
                line = ser.readline().decode('utf-8').strip()
                
                # Only queue state messages (0, 1, 2)
                if line.isdigit() and line in ['0', '1', '2']:
                    output_queue.put(line)
                # Print acknowledgment messages to console
                elif line.startswith("I received:"):
                    print(f"Arduino {line}")
                    
        except Exception as e:
            error_msg = f"Serial read error: {e}"
            output_queue.put(error_msg)
            break
        time.sleep(0.1)

def main():
    # Serial Configuration
    SERIAL_PORT = 'COM5'  # Adjust this to match your Arduino's port
    BAUD_RATE = 9600

    # GUI Theme and Layout
    sg.theme('LightBlue2')
    layout = [
        [sg.Text("LED Duration (milliseconds):", size=(20, 1)),
         sg.Input(key='-INPUT-', size=(10, 1), default_text='1000')],
        [sg.Button("Send"), sg.Button("Exit")],
        [sg.Text("Device Status:", size=(10, 1))],
        [sg.Multiline(size=(50, 10), key='-OUTPUT-', autoscroll=True, disabled=True)]
    ]

    # Create Window
    window = sg.Window("Arduino LED Controller", layout)

    try:
        # Initialize Serial Connection
        ser = serial.Serial(
            port=SERIAL_PORT,
            baudrate=BAUD_RATE,
            timeout=1
        )
        time.sleep(2)  # Wait for Arduino to reset
    except Exception as e:
        sg.popup_error(f"Failed to open {SERIAL_PORT}: {e}")
        return

    # Create and start serial reading thread
    serial_queue = queue.Queue()
    serial_thread = threading.Thread(
        target=read_serial,
        args=(ser, serial_queue),
        daemon=True
    )
    serial_thread.start()

    # Main Event Loop
    while True:
        event, values = window.read(timeout=100)

        if event in (sg.WIN_CLOSED, "Exit"):
            break

        if event == "Send":
            try:
                # Validate input
                duration = int(values['-INPUT-'])
                if duration <= 0:
                    raise ValueError("Duration must be positive")
                
                # Send to Arduino with newline
                send_str = f"{duration}\n"
                ser.write(send_str.encode('utf-8'))
                window['-OUTPUT-'].update(f"Sent: {duration}ms\n", append=True)
                
            except ValueError as ve:
                window['-OUTPUT-'].update(f"Error: {ve}\n", append=True)
            except Exception as e:
                window['-OUTPUT-'].update(f"Send error: {e}\n", append=True)

        # Process any received serial data
        while not serial_queue.empty():
            response = serial_queue.get()
            state_messages = {
                '0': "Device State: LED is off",
                '1': "Device State: Button and LED are on",
                '2': "Device State: Button is off, LED on"
            }
            message = state_messages.get(response, f"Unknown state: {response}")
            window['-OUTPUT-'].update(f"{message}\n", append=True)

    # Cleanup
    ser.close()
    window.close()

if __name__ == "__main__":
    main()