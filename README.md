# Robot Arm Programs

This project contains practice code for programming a robot arm built from an old 3D printer. The project includes various scripts for controlling the robot arm, processing images, and practicing inverse kinematics.

## Project Structure

- **RobotArmConnector.py**: Contains functions for interacting with the robot arm, such as sending G-code commands and setting the home position. Now supports PS5 controller input.
- **controller_config.json**: Configuration file for mapping PS5 controller buttons to robot arm actions.
- **# Trig Practice.py**: Practice code for trigonometric calculations related to robot arm movement.
- **#Inverse Kinematics Practice.py**: Practice code for inverse kinematics, crucial for determining joint angles from desired positions.
- **#Picture to Arm V1.py** and **Picture to Arm V2.py**: Scripts for converting images to commands for the robot arm.
- **cv2_practice.py**: Involves computer vision tasks using OpenCV.
- **Img_Processing_Practice.py**: Involves image processing tasks related to the robot arm's operations.
- **Test.jpeg**: An image file used for testing image processing or robot arm operations.

## Installation and Setup

1. Ensure you have Python installed on your system.
2. Install necessary dependencies using pip:
   ```bash
   pip install -r requirements.txt
   ```
   (Note: Create a `requirements.txt` file with necessary packages if not already present.)

## Usage

- Run the scripts using Python to interact with the robot arm or process images.
- Use `RobotArmConnector.py` to send commands to the robot arm.
- **PS5 Controller Setup**:
  1. Connect your PS5 controller to your computer.
  2. Ensure `pygame` is installed for joystick support.
  3. Configure button mappings in `controller_config.json`.
  4. Run `RobotArmConnector.py` to control the robot arm using the PS5 controller.

## Features

- Control a robot arm using G-code commands.
- Practice inverse kinematics and trigonometric calculations.
- Process images and convert them to robot arm commands.
- Control the robot arm using a PS5 controller with customizable button mappings.

## Contributing

Contributions are welcome! Please fork the repository and submit a pull request for any improvements or new features.

## License

This project is licensed under the MIT License.
