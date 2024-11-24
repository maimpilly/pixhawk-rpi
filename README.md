# pixhawk-rpi
Communication between Pixhawk and Raspberry Pi using XBee

How to setup guide: XBee, RPi, Pixhawk

# Setting Up Raspberry Pi

## Install Raspberry Pi OS

Download Raspberry Pi Imager: <https://www.raspberrypi.com/software/>

Download the Raspberry Pi Imager for your operating system (Windows, macOS, or Linux).

## Write Raspberry Pi OS to the MicroSD Card

Insert the MicroSD card into the card reader and connect it to your computer.

Open the Raspberry Pi Imager.

1. Choose “Raspberry Pi OS” from the operating system options.
2. Select your MicroSD card as the storage target.
3. Then apply customization to enable ssh.      
![image](https://github.com/user-attachments/assets/57901bbd-8fae-46c3-86e6-3483c855c076)
4. Enable SSH for this tab
![image](https://github.com/user-attachments/assets/0c8a1358-74a8-4134-88e7-d4993b533977)
5. Click "Write" to begin writing the OS to the card.
6. Once complete, remove the MicroSD card from the reader.

## Initial Raspberry Pi Setup

Insert the MicroSD card into the slot on the Raspberry Pi.

Connect the power supply to the Raspberry Pi to boot it up. Here, I will be using SSH to connect to the Raspberry Pi. Alternatively, connect a monitor and other peripherals to get a visual view.

Use **ssh \[username\]@\[hostname\].local or ssh \[username\]@\[IP address\]**.

You will be asked to enter the password of your wifi that you had setup while editing the configuration in the previous step.

# Set Up XBee Communication

## Configure XBee Modules Using XCTU

Download and install XCTU from Digi’s website on your computer.

- Connect XBee Modules:
  - Insert the XBee Pro modules into the USB adapters and connect them to your computer.
  - Click on the “Discover Devices” button to find the connected XBee module.
  - Add the discovered XBee module to your XCTU workspace.
- Configure XBee Modules:
  - Set one XBee Pro as the Coordinator (to be used with the ground station).
    - Set the PAN ID (this must be the same on both XBee modules).
    - Set the baud rate to 9600. Other common baud rates like 115200, 57600, 38400, 19200, or 4800.
    - Write the settings to the XBee module.
  - Set the other XBee Pro as a Router (to be used with the drone).
    - Repeat the steps above to connect and configure the second XBee module.
    - Set this XBee module as a Router.
    - Use the same PAN ID and baud rate as the Coordinator.
    - Write the settings to the XBee module.
- **Ensure both XBee modules are on the same PAN ID and use the same communication settings (e.g., baud rate, channel).**
- **Set SH and SL of Coordinator as the DH and DL of the edge device.**
- **CH, ID, and BD of all the routers and coordinators are the same.**
- Make sure that the highlighted ones are the  same for communication. These are to be used for the **different noise measurement units** that sent the data to the drone. These are configured as edge devices. There can be multiple edge devices, but only one coordinator.
![image](https://github.com/user-attachments/assets/73992c8f-bcba-4620-a706-69f5a452cedf)

![image](https://github.com/user-attachments/assets/4c38aa70-b382-4aed-9580-e622dd08cfee)


## Sending Test data

![image](https://github.com/user-attachments/assets/a3f63658-6dae-4e18-beef-9495ad1f9829)

1. Connect one Xbee to your PC and select Discover devices (1 in the above picture). Search for the device and add the device connected to your USB port.
2. Select Open (2) to start communicating, ie sending and receiving message from Xbee usig XCTU software.
3. Type your message in (3) to receive them on your pi.


# Enable UART on RPi

Use raspi-config to Enable UART on Rpi for sending data to Pixhawk

Open the Raspberry Pi configuration tool:

sudo raspi-config

1. Navigate to Interfacing Options.
2. Select Serial.
3. When asked, "Would you like a login shell to be accessible over serial?", select No.
4. When asked, "Would you like the serial port hardware to be enabled?", select Yes.

Exit the raspi-config tool and reboot your Raspberry Pi:

sudo reboot

# Python Scripts

## For the first time, do these

sudo apt-get update

sudo apt-get install python3-serial

sudo apt-get install python3-pip

pip3 install pymavlink --break-system-packages

pip3 install mavproxy --break-system-packages

You could also create a virtual python environment and install pymavlink and mavproxy. Unfortunately, this cannot be done on a global scope and hence the flag “--break-system-packages” is used.

## Check for mavproxy installation

Check if mavproxy is working using this command:  
mavproxy.py --master=/dev/&lt;port that is used to connect to pixhawk&gt; --baudrate &lt;give the baud rate of that port&gt; --out=udp:127.0.0.1:14550

### Forward Data to QGroundControl

The --out=udp:127.0.0.1:14550 part of the command forwards the MAVLink data to the local UDP port 14550.

You can then connect QGroundControl (running on your PC) to this UDP port to visualize and monitor the incoming MAVLink messages.

Connect QGroundControl to MAVProxy:

- Open QGroundControl on your PC.
- Navigate to the Settings menu (usually a gear icon).
- Go to Comm Links and add a new connection.
- Set up a UDP link:
- Protocol: UDP
- Port: 14550 (or the port you used in the MAVProxy command)
- Start the connection. QGroundControl should now be able to receive and display the MAVLink data being forwarded by MAVProxy.

## Python script just to receive data to see everything is working fine

Ssh into pi, then use the following:

1. nano testrx.py
2. Copy and paste the below code
3. Connect Xbee to the USB port of the PC and RPi
4. Write some data in the Console log or Send packets using XCTU software. ![A computer screen with a green arrow
![image](https://github.com/user-attachments/assets/6e9dc3be-df71-4c55-94fe-5006be92a906)
5. The data will be printed by the raspberry pi

CODE:

import serial

import time

\# Function to find the correct serial port

def find_serial_port():

import glob

ports = glob.glob('/dev/ttyUSB\*')

if not ports:

print("No USB serial devices found.")

return None

print(f"Available ports: {ports}")

return ports\[0\]

\# Find the serial port

port = find_serial_port()

if port is None:

exit()

\# Set up serial communication with XBee

try:

ser = serial.Serial(port, 9600, timeout=1) # Adjust baud rate if necessary

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

## Python code for receiving and forwarding the data to Pixhawk

This script would read the data from the Xbee on the Rpi and send it to the PixHawk.

import serial

import time

from pymavlink import mavutil

\# Serial connection to XBee on Raspberry Pi

xb_serial = serial.Serial('/dev/ttyUSB0', 9600) # XBee USB adapter port on Pi

\# Serial connection to Pixhawk on Raspberry Pi

pixhawk_serial = mavutil.mavlink_connection('/dev/ttyACM0', baud=921600) #For serial connection to TELEM2 port use: "serial0" Pixhawk USB connection use:"ttyACM0" or the respective USB port used.

def send_data_to_pixhawk(data):

\# Example MAVLink message: Send data as a custom MAVLink message

pixhawk_serial.mav.command_long_send(

pixhawk_serial.target_system,

pixhawk_serial.target_component,

mavutil.mavlink.MAV_CMD_USER_1, # Custom user command

0, # Confirmation

int(data), 0, 0, 0, 0, 0, 0 # Pass the received data as a parameter

)

print("Waiting for data from XBee...")

while True:

try:

if xb_serial.in_waiting > 0:

\# Read raw bytes from XBee

raw_data = xb_serial.read(xb_serial.in_waiting)

try:

\# Attempt to decode the data to string

data = raw_data.decode('utf-8').strip()

print(f"Received data from XBee: {data}")

\# Send data to Pixhawk

send_data_to_pixhawk(data)

print(f"Data sent to Pixhawk: {data}")

\# Optional: Wait for an acknowledgment or response

msg = pixhawk_serial.recv_match(type='COMMAND_ACK', blocking=True, timeout=2)

if msg:

print(f"Received acknowledgment from Pixhawk: {msg}")

else:

print("No acknowledgment from Pixhawk")

except UnicodeDecodeError:

\# Handle decoding errors

print("Received non-UTF-8 data, ignoring...")

continue

except Exception as e:

print(f"Error: {e}")

time.sleep(1)

# Troubleshooting

## mavproxy.py: command not found

The error mavproxy.py: command not found occurs because the mavproxy command is not available in your system's PATH, even though you installed it using the --break-system-packages option. This usually happens when the installation directory is not included in your PATH, or if there was an issue with the installation itself.

export PATH=$PATH:/home/yourusername/.local/bin

You can add this line to your .bashrc to make it permanent:

echo 'export PATH=$PATH:/home/&lt;yourusername&gt;/.local/bin' >> ~/.bashrc

source ~/.bashrc

Permission Issues: If you encounter permission issues accessing serial ports, add your user to the dialout group:

sudo usermod -aG dialout $USER
