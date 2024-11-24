import serial
import time
from pymavlink import mavutil

# Serial connection to XBee on Raspberry Pi
xb_serial = serial.Serial('/dev/ttyUSB0', 9600)  # XBee USB adapter port on Pi

# Serial connection to Pixhawk on Raspberry Pi
pixhawk_serial = mavutil.mavlink_connection('/dev/ttyACM0', baud=921600)  #For serial connection to TELEM2 port use: "serial0" Pixhawk USB connection use:"ttyACM0"

def send_data_to_pixhawk(data):
    # Example MAVLink message: Send data as a custom MAVLink message
    pixhawk_serial.mav.command_long_send(
        pixhawk_serial.target_system,
        pixhawk_serial.target_component,
        mavutil.mavlink.MAV_CMD_USER_1,  # Custom user command
        0,  # Confirmation
        int(data), 0, 0, 0, 0, 0, 0  # Pass the received data as a parameter
    )

print("Waiting for data from XBee...")

while True:
    try:
        if xb_serial.in_waiting > 0:
            # Read raw bytes from XBee
            raw_data = xb_serial.read(xb_serial.in_waiting)

            try:
                # Attempt to decode the data to string
                data = raw_data.decode('utf-8').strip()
                print(f"Received data from XBee: {data}")

                # Send data to Pixhawk
                send_data_to_pixhawk(data)
                print(f"Data sent to Pixhawk: {data}")

                # Optional: Wait for an acknowledgment or response
                msg = pixhawk_serial.recv_match(type='COMMAND_ACK', blocking=True, timeout=2)
                if msg:
                    print(f"Received acknowledgment from Pixhawk: {msg}")
                else:
                    print("No acknowledgment from Pixhawk")

            except UnicodeDecodeError:
                # Handle decoding errors
                print("Received non-UTF-8 data, ignoring...")
                continue

    except Exception as e:
        print(f"Error: {e}")
    time.sleep(1)
