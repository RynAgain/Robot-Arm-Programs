import cv2
import numpy as np

# Initialize a video capture object
cap = cv2.VideoCapture(0)  # 0 for default camera, 1 for external camera and so on

# Check if the camera opened successfully
if not cap.isOpened():
    print("Error: Could not open camera.")
    exit()

# Choose the same dictionary you used for generating markers
dictionary = cv2.aruco.Dictionary_get(cv2.aruco.DICT_6X6_250)
parameters = cv2.aruco.DetectorParameters_create()

while True:
    # Capture frame-by-frame
    ret, frame = cap.read()

    if not ret:
        print("Failed to grab frame")
        break

    # Convert the frame to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Detect ArUco markers
    corners, ids, rejected = cv2.aruco.detectMarkers(gray, dictionary, parameters=parameters)

    if len(corners) > 0:
        cv2.aruco.drawDetectedMarkers(frame, corners, ids)

        for corner in corners:
            pts = corner[0].astype(int)

            # Calculate the mid points of the edges of the marker
            mid1 = (pts[0] + pts[1]) // 2
            mid2 = (pts[2] + pts[3]) // 2

            # Draw the line connecting the mid points
            cv2.line(frame, tuple(mid1), tuple(mid2), (0, 255, 0), 2)

            # Calculate the angle
            angle = np.degrees(np.arctan2(mid2[1] - mid1[1], mid2[0] - mid1[0]))
            print(f"Angle: {angle:.2f} degrees")

    # Display the resulting frame
    cv2.imshow('Frame', frame)

    # Press 'q' to exit the loop
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything is done, release the capture
cap.release()
cv2.destroyAllWindows()
