import cv2
from pyzbar import pyzbar

# Initialize the webcam
cap = cv2.VideoCapture(0)

# Check if the webcam is opened successfully
if not cap.isOpened():
    print("Failed to open webcam")
    exit()

# Read a frame from the webcam
ret, frame = cap.read()

# Check if the frame is empty
if not ret:
    print("Failed to capture frame from webcam")
    exit()

# Convert the frame to grayscale
gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

# Detect barcodes in the frame
barcodes = pyzbar.decode(gray)

# Iterate over the detected barcodes
for barcode in barcodes:
    # Extract the barcode data
    barcode_data = barcode.data.decode("utf-8")
    
    # Print the barcode data
    print("Barcode:", barcode_data)

# Release the webcam
cap.release()