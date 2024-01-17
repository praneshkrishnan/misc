import cv2
import time

# Open the webcam (0 indicates the default camera)
cap = cv2.VideoCapture(0)

# Set the desired resolution (3840 x 2160 in this case)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 3840)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 2160)

# Check if the webcam is opened successfully
if not cap.isOpened():
    print("Error: Could not open webcam.")
    exit()

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

    # Save the captured image (you can customize the file name and format)
    image_filename = f"captured_image_{int(time.time())}.jpg"
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