import serial
import time

# Function to find the correct serial port
def find_serial_port():
    import glob
    ports = glob.glob('/dev/ttyUSB*')
    if not ports:
        print("No USB serial devices found.")
        return None
    print(f"Available ports: {ports}")
    return ports[0]

# Find the serial port
port = find_serial_port()
if port is None:
    exit()

# Set up serial communication with XBee
try:
    ser = serial.Serial(port, 9600, timeout=1)  # Adjust baud rate if necessary
    print(f"Connected to {port}.")
except serial.SerialException as e:
    print(f"Failed to connect to {port}: {e}")
    exit()

print("Waiting for data...")

while True:
    try:
        if ser.in_waiting > 0:
            data = ser.readline().decode().strip()
            if data:
                print(f"Received data: {data}")
            else:
                print("No data received yet")
    except Exception as e:
        print(f"Error: {e}")
        time.sleep(1)
    time.sleep(1)