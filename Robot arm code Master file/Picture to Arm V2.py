#Picture to Arm V2
import tinyik as tk
import numpy as np
import serial
import matplotlib.pyplot as plt

# Define the full arm
arm = tk.Actuator([
    'x', [6.5, 0., 0.],  # Base segment converted to meters (6.5 inches)
    'y', [8.5, 0., 0.],   # Second segment converted to meters (5 inches)
    'y', [5, 0., 0.],  # Third segment converted to meters (8.5 inches)
    'y', [3, 0., 0.]   # Fourth segment converted to meters (3 inches)
])

def send_gcode(gcode, port='COM3', baudrate=25000):
    with serial.Serial(port, baudrate, timeout=1) as ser:
        ser.flushInput()
        ser.flushOutput()
        ser.write(gcode.encode())
        print(f"Sent G-code: {gcode}")
        while True:
            response = ser.readline().decode().strip()
            if response.startswith("ok"):
                print("Device is ready for the next command.")
                break
            elif "error" in response.lower():
                print(f"Error from device: {response}")
                break

def set_home(port='COM3', baudrate=25000):
    send_gcode('G92 X0 Y0 Z0 A0\n', port, baudrate)

def send_home(port='COM3', baudrate=25000):
    gcode = 'G1 X0 Y0 Z0 A0\n'
    send_gcode(gcode, port, baudrate)

def safety_check(angles):
    min_angle_rad = np.deg2rad(-160)
    max_angle_rad = np.deg2rad(160)
    if not np.all((min_angle_rad <= angles) & (angles <= max_angle_rad)):
        raise ValueError("Angles are outside the safe range of -160 to 160 degrees")

def calculate_and_send_angles(ee_coordinates, port='COM3', baudrate=25000):
    arm.ee = ee_coordinates
    angles = arm.angles
    safety_check(angles)
    gcode = 'G1 X{:.2f} Y{:.2f} Z{:.2f} A{:.2f}\n'.format(*np.rad2deg(angles))
    send_gcode(gcode, port, baudrate)

def visualize_with_tinyik(ee_coordinates):
    arm.ee = ee_coordinates
    tk.visualize(arm)

def visualize_with_matplotlib(ee_coordinates):
    arm.ee = ee_coordinates
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.plot(*np.array(arm.ee).T, marker='o')
    plt.show()

def visualize_with_matplotlib(ee_coordinates):
    arm.ee = ee_coordinates
    angles = arm.angles

    # Define link lengths (as you specified in your arm definition)
    link_lengths = [6.5, 8.5, 5, 3]  # in inches or your chosen unit

    # Starting position (base of the arm)
    positions = [[0, 0, 0]]

    # Initial orientation
    orientation = [0, 0, 0]  # Assuming starting orientation is aligned with axes

    for i, length in enumerate(link_lengths):
        # Calculate the transformation for this link
        dx = length * np.cos(orientation[2]) * np.cos(orientation[1])
        dy = length * np.sin(orientation[2]) * np.cos(orientation[1])
        dz = length * np.sin(orientation[1])

        # Update the current position
        new_position = [positions[-1][0] + dx, positions[-1][1] + dy, positions[-1][2] + dz]
        positions.append(new_position)

        # Update orientation based on the current joint angle
        # Adjust this based on how your arm's axes are defined
        if i < len(angles):
            if i % 2 == 0:  # Adjust depending on which axis the joint rotates around
                orientation[1] += angles[i]
            else:
                orientation[2] += angles[i]

    # Convert positions to a format suitable for plotting
    positions = np.array(positions).T

    # Now plot using Matplotlib
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.plot(*positions, marker='o')
    plt.show()



# Example usage:
visualize_with_tinyik([10, 0, 3])
visualize_with_matplotlib([10, 0, 3])