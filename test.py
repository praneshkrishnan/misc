import cv2
import os
cam_port = 0
cam = cv2.VideoCapture(cam_port) 

result, image = cam.read() 
path = "C:/Users/prane/Downloads/IMAGES"
if result: 
	cv2.imshow("Image", image) 	
	cv2.imwrite(os.path.join(path,'image.jpg'),image)
	cv2.waitKey(0) 
	cv2.destroyWindow("Image") 
else: 
	print("No image detected. Please! try again")