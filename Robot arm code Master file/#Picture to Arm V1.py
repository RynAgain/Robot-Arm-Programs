#Picture to Arm V1
import numpy as np
import matplotlib.pyplot as plt
import math
from PIL import Image
import matplotlib.patches as patches
import RobotArmConnector as RAC
import serial
import time

#connect and setup ARM first step
#printer = serial.Serial(RAC.printer_port, RAC.baud_rate, timeout=2)
time.sleep(2)
print(RAC.home)
RAC.send_gcode("G92 X0 Y0 Z0 E0")
#this function is a test of the X angle motor position
#takes desired Picture corrinates XY to determin the angle fo the first motor
def calculate_theta_in_degrees(x, y):
    """
    Calculate the angle (in degrees) from the origin to the point (x, y).

    Parameters:
    - x: The x-coordinate of the point.
    - y: The y-coordinate of the point.

    Returns:
    - theta_degrees: The angle in degrees from the origin to the point (x, y).
    """
    theta_radians = math.atan2(y, x)
    theta_degrees = math.degrees(theta_radians)
    return theta_degrees

#distance and rest of angles
def distance_from_origin(X, Y):
    """Returns the distance from the origin to the point (X, Y)."""
    return math.sqrt(X**2 + Y**2)

#

#angle test via plot
def find_angles(Length, YHeight):
    base = 6
    L1 =  8 
    L2 = 7
    pen = 3

def inverse_kinematics(x, y):
    L1 = 8.5  # length of the first segment (green line)
    L2 = 6.5  # length of the second segment (pink line)
    L3 = 6 # length of the base (red line)
    
    # Compute the distance from (0, L3) to (x, y)
    r = math.sqrt(x**2 + (y - L3)**2)
    
    # Check if the point is reachable
    if r > L1 + L2:
        return "Error"
    
    # Angle between line joining (0, L3) to (x, y) and X-axis
    phi = math.atan2(y - L3, x)
    
    # Using the Law of Cosines to find angle beta
    cos_beta = (L1**2 + L2**2 - r**2) / (2 * L1 * L2)
    beta = math.acos(cos_beta)
    
    # Another angle required for alpha calculation
    delta = math.asin((L2 * math.sin(beta)) / r)
    
    # Alpha is phi + delta
    alpha = phi + delta
    
    # Gamma is fixed because the pen needs to be perpendicular to the X-axis
    gamma = math.pi / 2  # 90 degrees
    
    # Convert radians to degrees for the results
    alpha = math.degrees(alpha)
    beta = math.degrees(beta)
    gamma = math.degrees(gamma)
    
    return alpha, beta, gamma

def plot_arm(alpha, beta, gamma):
    L1 = 8.5
    L2 = 6.5
    L3 = 6
    
    # Convert degrees back to radians for trig functions
    alpha = math.radians(alpha)
    beta = math.radians(beta)
    
    # Calculate end points of the first segment (green line)
    x1 = L1 * math.cos(alpha)
    y1 = L3 + L1 * math.sin(alpha)
    
    # Calculate end points of the second segment (pink line)
    x2 = x1 + L2 * math.cos(alpha + beta - math.pi)
    y2 = y1 + L2 * math.sin(alpha + beta - math.pi)
    
    # Plot the arm
    fig, ax = plt.subplots()
    ax.plot([0, 0], [0, L3], 'r-')  # Red base
    ax.plot([0, x1], [L3, y1], 'g-')  # Green segment
    ax.plot([x1, x2], [y1, y2], 'm-')  # Pink segment
    
    # Plot the end effector (pen tip)
    circle = patches.Circle((x2, y2), radius=0.2, color='b')
    ax.add_patch(circle)

        # Add labels
    ax.text(-1, L3/2, 'Base (Red)', color='r', verticalalignment='center')
    ax.text((0 + x1) / 2, (L3 + y1) / 2, 'Arm 1 (Green)', color='g', verticalalignment='center')
    ax.text((x1 + x2) / 2, (y1 + y2) / 2, 'Arm 2 (Pink)', color='m', verticalalignment='center')
    ax.text(x2 + 0.5, y2, 'End Effector (Pen Tip)', color='b')
    
    ax.set_xlim(-20, 20)
    ax.set_ylim(0, 20)
    plt.axis('equal')
    plt.xlabel('X-axis')
    plt.ylabel('Y-axis')
    plt.title('Robot Arm Visualization')
    plt.grid(True)
    plt.show()

def convert_to_gcode_angles(alpha, beta, gamma): #might not need to use this
    # Convert angles to a range of 0 to 360 (0° being the straight upward position)
    motor_Y = 180 - alpha if alpha >= 0 else 360 + alpha
    motor_Z = -beta if beta >= 0 else -(360 + beta)  # reverse for Motor Z
    motor_A = gamma if gamma >= 0 else 360 + gamma

    return motor_Y, motor_Z, motor_A

# Test
x, y, z = 10, 0, 3 #test coordinates
L = distance_from_origin(x, y) #find the distance so that the Y, Z motors can be angled on a 2d verticleplane
alpha, beta, gamma = inverse_kinematics(L, z)
Omega = calculate_theta_in_degrees(x, y)
print(alpha, beta, gamma)
print("Basic")
print(f"G1 X{Omega} Y{90 - alpha} Z{beta}")
#A, B, C= convert_to_gcode_angles(alpha, beta, gamma)
#print(A, B ,C)
if alpha != "Error":
    plot_arm(alpha, beta, gamma)

# Safety Check function
def safety(O, a, b, g):
    args = [O, a, b, g]   
    for arg in args:
        if abs(arg) >= 170:
            raise ValueError(f"Value {arg} is out of the safety range!")

#Go to Command Function

def GotoTAP(x, y, z, f):
    print(f"Going to {x},{y},{z}")
    updown = [z+1, z]
    L = distance_from_origin(x, y) # find the distance on the plane
    for i in updown:
        alpha, beta, gamma = inverse_kinematics(L, i) # find arm angles
        Omega = calculate_theta_in_degrees(x, y) # finds the rotation of base
        #Best way to easily achieve safe movements is to go from top to bottom and check the angles are less than 180
        #for that we will 
        safety(Omega, alpha, beta, gamma)
        #Move Z then Y then X
        RAC.send_gcode(f"G1 A{90-beta} F{f}") #Pen angle
        RAC.get_okay()
        RAC.send_gcode(f"G1 X{Omega} F{f}") #base position
        RAC.get_okay()
        RAC.send_gcode(f"G1 Z{beta} F{f}") #2nd arm position
        RAC.get_okay()
        RAC.send_gcode(f" G1 Y{90-alpha} F{f}") #final arm position
        RAC.get_okay()
        time.sleep(0.5)
        RAC.get_okay()

def back_off():
    RAC.send_gcode(f"G1 Y0 F{200}")
    
GotoTAP(x, y-5, 2.5, 150)
back_off()
GotoTAP(x+1, y-5 , 2.5, 150)
back_off()
GotoTAP(x, y-4, 2.5, 150)
back_off()
GotoTAP(x, y, 2.5, 150)
back_off()
GotoTAP(x+2, y, 2.5, 150)
back_off()
GotoTAP(x+3, y, 2.5, 150)
back_off()
time.sleep(5)
RAC.send_home()