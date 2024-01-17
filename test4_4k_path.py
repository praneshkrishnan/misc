import cv2
import time
import os

# Open the webcam (0 indicates the default camera)
cap = cv2.VideoCapture(0)

# Set the desired resolution (3840 x 2160 in this case)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 3840)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 2160)

# Check if the webcam is opened successfully
if not cap.isOpened():
    print("Error: Could not open webcam.")
    exit()

# Specify the path where you want to save the images
save_path = "C:/Users/prane/Downloads/IMAGES"

# Create the specified path if it doesn't exist
if not os.path.exists(save_path):
    os.makedirs(save_path)

# Create a loop to capture images every 1 second
while True:
    # Read a frame from the webcam
    ret, frame = cap.read()

    # Check if the frame is read successfully
    if not ret:
        print("Error: Could not read frame.")
        break

    # Display the captured frame
    cv2.imshow("Webcam Capture", frame)

    # Save the captured image to the specified path
    image_filename = os.path.join(save_path, f"captured_image_{int(time.time())}.jpg")
    cv2.imwrite(image_filename, frame)
    print(f"Image saved as {image_filename}")

    # Wait for 1 second before capturing the next image
    time.sleep(1)

    # Check for the 'q' key to exit the loop
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the webcam and close all OpenCV windows
cap.release()
cv2.destroyAllWindows()