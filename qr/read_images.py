import cv2
import numpy as np

cap = cv2.VideoCapture(0)


result, image = cap.read()

# cv2.imshow('Result',image)
cv2.imwrite('Result.jpg',image)


# cv2.Waitkey(0)
# cv2. destroyAllWindows()
