import time
import csv
from grove.grove_accelerometer import GroveAccelerometer
from grove.grove_oled_display import GroveOledDisplay
from grove.grove_buzzer import GroveBuzzer
from grove.grove_servo import GroveServo

# Initialize components
accelerometer = GroveAccelerometer()
oled_display = GroveOledDisplay()
buzzer = GroveBuzzer()
servo = GroveServo()

# CSV file setup
csv_file = 'data_log.csv'
with open(csv_file, mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(["Time", "Angle", "Buzzer State"])

# Function to get angle from accelerometer
def get_angle():
    x, y, z = accelerometer.read()
    angle = int((x + y + z) / 3)  # Simplified calculation for example
    return angle

# Main loop
start_time = time.time()
while True:
    current_time = time.time() - start_time
    angle = get_angle()
    buzzer_state = "OFF"
    
    if angle > 45:  # Threshold for buzzer
        buzzer.on()
        buzzer_state = "ON"
    else:
        buzzer.off()
    
    # Update servo and OLED display
    servo.set_angle(angle)
    oled_display.show_text(f"Angle: {angle}\nBuzzer: {buzzer_state}")
    
    # Log data to CSV
    with open(csv_file, mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([current_time, angle, buzzer_state])
    
    time.sleep(1)