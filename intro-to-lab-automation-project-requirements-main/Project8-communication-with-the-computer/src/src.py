import PySimpleGUI as sg
import serial
import threading
import time
from serial.tools import list_ports

class ArduinoController:
    def __init__(self):
        self.serial_port = None
        self.is_running = False
        self.read_thread = None
        
        layout = [
            [sg.Text('Select Port:'), sg.Combo(self.get_serial_ports(), key='-PORT-'),
             sg.Button('Connect')],
            [sg.Text('LED Duration (ms):'), sg.Input(key='-DURATION-', default_text='90'),
             sg.Button('Send')],
            [sg.Multiline(size=(50, 10), key='-OUTPUT-', disabled=True)],
            [sg.Button('Exit')]
        ]
        
        self.window = sg.Window('Arduino LED Controller', layout)
        
    def get_serial_ports(self):
        return [port.device for port in list_ports.comports()]
        
    def connect_serial(self, port):
        try:
            self.serial_port = serial.Serial(port, 9600, timeout=1)
            time.sleep(2)  # Wait for Arduino to reset
            # Clear any startup messages
            self.serial_port.reset_input_buffer()
            return True
        except serial.SerialException as e:
            self.update_output(f"Error connecting to {port}: {str(e)}")
            return False
            
    def send_duration(self, duration):
        try:
            if self.serial_port and self.serial_port.is_open:
                command = f"{duration}\n"
                self.serial_port.write(command.encode())
                self.update_output(f"Sent duration: {duration}ms")
            else:
                self.update_output("Not connected to Arduino")
        except serial.SerialException as e:
            self.update_output(f"Error sending data: {str(e)}")
            
    def read_serial(self):
        while self.is_running:
            try:
                if self.serial_port and self.serial_port.in_waiting:
                    response = self.serial_port.readline().decode().strip()
                    if response:
                        self.process_response(response)
            except serial.SerialException as e:
                self.update_output(f"Error reading data: {str(e)}")
                break
            time.sleep(0.1)
            
    def process_response(self, response):
        # Handle numeric responses (echoed values) separately
        try:
            int(response)
            return  # Skip processing echoed numeric values
        except ValueError:
            pass
            
        status_messages = {
            'OFF': 'LED is OFF',
            'ON': 'LED is ON',
            'BUTTON_PRESSED': 'Button pressed',
            'BUTTON_RELEASED': 'Button released'
        }
        
        message = status_messages.get(response, f'Status: {response}')
        self.update_output(message)
        
    def update_output(self, message):
        self.window['-OUTPUT-'].print(f"{time.strftime('%H:%M:%S')}: {message}")
        
    def run(self):
        self.is_running = True
        
        while True:
            event, values = self.window.read(timeout=100)
            
            if event in (None, 'Exit'):
                break
                
            elif event == 'Connect':
                port = values['-PORT-']
                if port:
                    if self.connect_serial(port):
                        self.update_output(f"Connected to {port}")
                        self.read_thread = threading.Thread(target=self.read_serial)
                        self.read_thread.daemon = True
                        self.read_thread.start()
                else:
                    self.update_output("Please select a port")
                    
            elif event == 'Send':
                try:
                    duration = int(values['-DURATION-'])
                    if duration > 0:
                        self.send_duration(duration)
                    else:
                        self.update_output("Duration must be positive")
                except ValueError:
                    self.update_output("Please enter a valid number")
                    
        self.is_running = False
        if self.serial_port:
            self.serial_port.close()
        self.window.close()

if __name__ == '__main__':
    controller = ArduinoController()
    controller.run()