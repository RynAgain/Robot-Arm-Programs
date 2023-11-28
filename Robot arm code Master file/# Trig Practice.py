# Trig Practice

import math

#this function is a test of the X angle motor position
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

# Test the function
x, y = -1, -0
theta = calculate_theta_in_degrees(x, y)
print(f"The angle theta for point ({x}, {y}) is: {theta} degrees.")
