#Inverse Kinematics Practice
import math

def calculate_joint_angles(x, y):
    # Ensure the point can be reached
    total_length = 7 + 8 + 7 + 3  # base + segment 1 + segment 2 + pen
    if math.sqrt(x**2 + y**2) > total_length:
        raise ValueError("The specified point cannot be reached by the arm")

    # Joint 1 angle (rotation in XY plane)
    theta_1 = math.atan2(y, x)

    # Distance from the base to the point in XY plane
    r = math.sqrt(x**2 + y**2)

    # Vertical height the pen needs to cover
    z = 7 + 8 + 7 - 3  # base + segment 1 + segment 2 - pen

    # Length from joint 2 to the pen tip
    l = math.sqrt(r**2 + z**2)

    # Using Law of Cosines to calculate joint 2 and joint 3 angles
    a = 8  # length of segment 1
    b = 7  # length of segment 2

    # Angle between segment 1 and the line connecting joint 2 to pen tip
    alpha = math.acos((b**2 + l**2 - a**2) / (2 * b * l))
    theta_2 = math.atan2(z, r) + alpha

    # Angle between segments 1 and 2
    beta = math.acos((a**2 + b**2 - l**2) / (2 * a * b))
    theta_3 = math.pi - beta

    # Joint 4 angle to ensure pen is perpendicular to ground
    theta_4 = -theta_2 - theta_3

    return theta_1, theta_2, theta_3, theta_4

# Test the function
x, y = 10, 10
angles = calculate_joint_angles(x, y)
print("Joint Angles (in radians):", angles)
