#RobotArmConnector
import serial
import time
import random

# Replace '/dev/ttyUSB0' with the port to which your 3D printer is connected
printer_port = 'COM3'
# Set the baud rate; replace 115200 with the baud rate of your 3D printer
baud_rate = 250000

# Open a serial connection to the 3D printer
printer = serial.Serial(printer_port, baud_rate, timeout=2)

# Give the printer some time to initialize
time.sleep(2)
home ="G1 X0 Y0 Z0"

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
    c =  random.randint(-120, 120)
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
# Sending some example G-code commands
#send_gcode("G1 X-270 Y-270 Z-320")  # Move to X50, Y50 at 3000mm/min speed
#send_gcode("G1 X-360 Y-360 Z-360")
#send_gcode("G1 X-270 Y-360 Z-360")
#wait(2)
#send_home()
#send_gcode("G1 X-270 Y-360 Z-270")
#send_gcode("G1 X-270 Y-300 Z-270")
#wait(2)
x = 0
t = 0
#if t is one then this enabled 
while x < 10 and t == 1:
    testing()
    x += 1
    print("Testing:  " + x)

#send_gcode("G92 X0 Y0 Z0")


#Manual Control interface
control = False
while control == True:
    r = input("Control:  ")
    print("\n")
    if r == "h":
        send_home()
    elif r == "x":
        a = input()
        send_gcode(gcode_gen(a, 0, 0))
    elif r == "y":
        a = input()
        send_gcode(gcode_gen(0, a, 0))
    elif r == "z":
        a = int(input())
        send_gcode(gcode_gen(0, 0, a))
    elif r == "t":
        ti = int(input(""))
        for i in range(ti):
            testing()
            get_okay()
            print("got Okay from arm")
        send_home()
        
    elif r == "end":
        send_home()
        control == False
    elif r == "g":
        c = input("")
        send_gcode(c)
    elif r == "zero":
        set_zero()
    else:
        send_home
    wait(1)
    get_okay()




#send_gcode("M84")  # Disable steppers

# Close the serial connection
#printer.close()
