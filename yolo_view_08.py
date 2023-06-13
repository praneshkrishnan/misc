import os
import shutil
from tkinter import *
from tkinter import messagebox
from tkinter import filedialog
from PIL import Image, ImageTk
import torch
import cv2
import numpy as np

# Create the main window
root = Tk()

# Set the window title
root.title('Image Viewer')

# Create a label to display the image
image_label = Label(root)
image_label.pack()

# Create a function to load the yolo model and labels
def load_model():
    global model, labels
    
    # Ask the user for the model and labels paths
    model_path = filedialog.askopenfilename(title='Select yolo model')
    labels_path = filedialog.askopenfilename(title='Select yolo labels')
    
    # Check if a model and labels were selected
    if model_path and labels_path:
        # Load the yolo model
        model = torch.hub.load('ultralytics/yolov5', 'custom', path=model_path)
        
        # Load the yolo labels
        with open(labels_path, 'r') as f:
            labels = f.read().splitlines()

# Create a function to apply inferencing on an image and save the results to a file
def apply_inferencing(image_path):
    # Apply object detection using the loaded yolo model
    results = model(image_path)
    
    # Extract the bounding boxes and class indices
    boxes = results.xyxy[0].numpy()
    class_indices = boxes[:, 5].astype(int)
    
    # Convert the class indices to class names using the loaded yolo labels
    class_names = [labels[i] for i in class_indices]
    
    # Load the image using opencv
    img = cv2.imread(image_path)
    
    # Loop through the bounding boxes and class names
    for box, class_name in zip(boxes, class_names):
        # Extract the box coordinates
        x1, y1, x2, y2 = box[:4].astype(int)
        
        # Draw a rectangle around the object
        cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
        
        # Put the class name above the rectangle
        cv2.putText(img, class_name, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)
    
    # Save the image with bounding boxes to a file using opencv
    cv2.imwrite(image_path, img)
    
    # Convert the image from BGR to RGB color space
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    
    # Convert the image from numpy array to PIL Image
    img = Image.fromarray(img)
    
    return img

# Create a function to check if a directory contains accept or decline subdirectories and prompt the user for action if it does
def check_accept_decline_subdirs(dir_path):
    global accept_dir_name, decline_dir_name
    
    # Check if the directory contains accept or decline subdirectories
    if os.path.exists(os.path.join(dir_path, 'accept')) or os.path.exists(os.path.join(dir_path, 'decline')):
        # Ask the user if they want to use existing accept/decline subdirectories or create new ones with an appending integer
        answer = messagebox.askyesno('Accept/Decline subdirectories exist', 'The selected directory already contains accept/decline subdirectories. Do you want to use them or create new ones with an appending integer?')
        
        # Check if the user wants to use existing accept/decline subdirectories or create new ones with an appending integer
        if answer:
            accept_dir_name = 'accept'
            decline_dir_name = 'decline'
        else:
            i = 1
            
            while True:
                accept_dir_name = f'accept_{i}'
                decline_dir_name = f'decline_{i}'
                
                if not os.path.exists(os.path.join(dir_path, accept_dir_name)) and not os.path.exists(os.path.join(dir_path, decline_dir_name)):
                    break
                
                i += 1

# Create a function to load the images from a directory
def load_images():
    global dir_path, image_files, current_image_index
    
    # Ask the user for the directory path
    dir_path = filedialog.askdirectory()
    
    # Initialize the list of image files and current image index
    image_files = []
    current_image_index = 0
    
    # Check if a directory was selected
    if dir_path:
        # Check if the directory contains accept or decline subdirectories and prompt the user for action if it does
        check_accept_decline_subdirs(dir_path)
        
        # Loop through the files in the directory
        for filename in os.listdir(dir_path):
            # Check if the file is an image
            if filename.endswith('.jpg') or filename.endswith('.png'):
                # Create the full file path and add it to the list of image files
                file_path = os.path.join(dir_path, filename)
                image_files.append(file_path)
        
        # Display the first image
        display_next_image()

# Create a function to display the next image
def display_next_image():
    global current_image_index
    
    # Check if there are more images to display
    if current_image_index < len(image_files):
        # Apply inferencing on the next image using the loaded yolo model and labels and save the results to a file
        img = apply_inferencing(image_files[current_image_index])
        
        # Resize the image to fit the window
        img = img.resize((400, 400), Image.ANTIALIAS)
        
        # Convert the image to a PhotoImage object
        photo = ImageTk.PhotoImage(img)
        
        # Update the image label with the new image
        image_label.config(image=photo)
        image_label.image = photo
        
        # Increment the current image index
        current_image_index += 1
    else:
        # Ask the user if they want to quit or load another directory
        answer = messagebox.askyesno('No more images', 'There are no more images to display. Do you want to load another directory?')
        
        # Check if the user wants to load another directory
        if answer:
            load_images()
        else:
            root.quit()

# Create a function to handle button clicks
def handle_button_click(action):
    global current_image_index
    
    # Check if an image was displayed
    if current_image_index > 0:
        # Get the previous image file path
        prev_image_file = image_files[current_image_index - 1]
        
        # Create the destination directory path based on the action (accept or decline)
        dest_dir_name = accept_dir_name if action == 'accept' else decline_dir_name
        dest_dir = os.path.join(dir_path, dest_dir_name)
        
        # Create the destination directory if it doesn't exist
        if not os.path.exists(dest_dir):
            os.makedirs(dest_dir)
        
        # Create a new file name for the previous image file with bounding boxes in the destination directory
        new_file_name = os.path.basename(prev_image_file)
        
        i = 1
        
        while os.path.exists(os.path.join(dest_dir, new_file_name)):
            new_file_name = f'{os.path.splitext(os.path.basename(prev_image_file))[0]}_{i}{os.path.splitext(os.path.basename(prev_image_file))[1]}'
            i += 1
        
        # Move the previous image file with bounding boxes to the destination directory with a new file name
        shutil.move(prev_image_file, os.path.join(dest_dir, new_file_name))
    
    # Display the next image
    display_next_image()

# Create an accept button
accept_button = Button(root, text='Accept', command=lambda: handle_button_click('accept'))
accept_button.pack(side=LEFT)

# Create a decline button
decline_button = Button(root, text='Decline', command=lambda: handle_button_click('decline'))
decline_button.pack(side=RIGHT)

# Initialize global variables
model = None
labels = []
dir_path = ''
image_files = []
current_image_index = 0

# Initialize accept/decline subdirectory names as accept/decline by default
accept_dir_name = 'accept'
decline_dir_name = 'decline'

# Load the yolo model and labels from files
load_model()

# Load the initial images from a directory
load_images()

# Run the main loop
root.mainloop()