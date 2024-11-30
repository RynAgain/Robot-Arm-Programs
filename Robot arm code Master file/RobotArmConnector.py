# RobotArmConnector
import serial
import time
import random
import pygame

# Initialize Pygame for joystick support
pygame.init()
pygame.joystick.init()

# Replace '/dev/ttyUSB0' with the port to which your 3D printer is connected
printer_port = 'COM3'
# Set the baud rate; replace 115200 with the baud rate of your 3D printer
baud_rate = 250000

# Open a serial connection to the 3D printer
printer = serial.Serial(printer_port, baud_rate, timeout=2)

# Give the printer some time to initialize
time.sleep(2)
home = "G1 X0 Y0 Z0"

def wait(x):
    time.sleep(x)

# A function to send G-code commands to the 3D printer
def send_gcode(gcode):
    print(f"Sending: {gcode}")
    printer.write((gcode + '\n').encode())
    # Wait for the command to be processed and read the response
    response = printer.readlines()
    for line in response:
        print(line.decode().strip())

def send_home():
    send_gcode(home)

def gcode_gen(x, y, z):
    return (f'G1 X{x} Y{y} Z{z} F300')

def testing():
    a = random.randint(-90, 90)
    b = random.randint(-70, 70)
    c = random.randint(-120, 120)
    send_gcode(gcode_gen(a, b, c))

def set_zero():
    send_gcode("G92 X0 Y0 Z0")

def get_okay():
    response = ''
    latest_response = ''

    # Wait for the expected response
    while True:
        response = printer.readline().decode().strip()
        if response:
            print(f"Response: {response}")
            latest_response = response
            if 'ok' in latest_response.lower():
                break
        else:
            # If there's no more data coming in, exit the loop
            break

# Initialize the first joystick
if pygame.joystick.get_count() > 0:
    joystick = pygame.joystick.Joystick(0)
    joystick.init()
    print(f"Initialized Joystick: {joystick.get_name()}")

# PS5 Controller Mapping
button_mapping = {
    0: "home",  # Example: Button 0 maps to home
    1: "zero",  # Example: Button 1 maps to set zero
    # Add more mappings as needed
}

# Main loop for joystick control
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.JOYBUTTONDOWN:
            button = event.button
            if button in button_mapping:
                action = button_mapping[button]
                if action == "home":
                    send_home()
                elif action == "zero":
                    set_zero()
                # Add more actions as needed
        elif event.type == pygame.QUIT:
            running = False

# Close the serial connection
printer.close()
pygame.quit()
