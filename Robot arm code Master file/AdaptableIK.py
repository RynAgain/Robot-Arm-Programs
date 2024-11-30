"""
Adaptable Inverse Kinematics Module

This module provides a flexible inverse kinematics solution for robotic arms
with varying configurations. It leverages existing functions and structures
from the current project to create a parameterized IK solver.

Author: [Your Name]
"""

import math

class AdaptableIK:
    def __init__(self, arm_lengths):
        """
        Initialize the IK solver with arm segment lengths.
        
        :param arm_lengths: List of lengths for each arm segment.
        """
        self.arm_lengths = arm_lengths

    def calculate_joint_angles(self, target_position):
        """
        Calculate joint angles for a given target position.
        
        :param target_position: Tuple (x, y) representing the target position.
        :return: List of joint angles.
        """
        x, y = target_position
        l1, l2 = self.arm_lengths

        # Calculate the distance from the base to the target position
        distance = math.sqrt(x**2 + y**2)

        # Check if the target is reachable
        if distance > (l1 + l2):
            raise ValueError("Target position is out of reach")

        # Calculate the angle for the first joint
        cos_angle1 = (x**2 + y**2 + l1**2 - l2**2) / (2 * l1 * distance)
        angle1 = math.acos(cos_angle1) + math.atan2(y, x)

        # Calculate the angle for the second joint
        cos_angle2 = (x**2 + y**2 - l1**2 - l2**2) / (2 * l1 * l2)
        angle2 = math.acos(cos_angle2)

        # Convert angles to degrees
        angle1_deg = math.degrees(angle1)
        angle2_deg = math.degrees(angle2)

        return [angle1_deg, angle2_deg]

    def set_configuration(self, config):
        """
        Set the configuration for the IK solver.
        
        :param config: Dictionary containing configuration parameters.
        """
        # Update arm lengths or other parameters based on config
        self.arm_lengths = config.get('arm_lengths', self.arm_lengths)

# Example usage
if __name__ == "__main__":
    # Initialize with default arm lengths
    ik_solver = AdaptableIK(arm_lengths=[100, 100])
    
    # Calculate joint angles for a target position
    target = (150, 50)
    try:
        angles = ik_solver.calculate_joint_angles(target)
        print(f"Calculated joint angles: {angles}")
    except ValueError as e:
        print(e)
