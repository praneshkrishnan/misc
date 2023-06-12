import shutil
import os
from tkinter import *
from PIL import Image, ImageTk

# Create the main window
root = Tk()

# Set the window title
root.title('Image Viewer')

# Create a label to display the image
image_label = Label(root)
image_label.pack()

# Create a function to display the next image
def display_next_image():
    global current_image_index
    
    # Check if there are more images to display
    if current_image_index < len(image_files):
        # Open the next image file
        img = Image.open(image_files[current_image_index])
        
        # Resize the image to fit the window
        img = img.resize((400, 400), Image.ANTIALIAS)
        
        # Convert the image to a PhotoImage object
        photo = ImageTk.PhotoImage(img)
        
        # Update the image label with the new image
        image_label.config(image=photo)
        image_label.image = photo
        
        # Increment the current image index
        current_image_index += 1

# Create a function to handle button clicks
def handle_button_click(action):
    global current_image_index
    
    # Check if an image was displayed
    if current_image_index > 0:
        # Get the previous image file path
        prev_image_file = image_files[current_image_index - 1]
        
        # Create the destination directory path
        dest_dir = os.path.join(dir_path, action)
        
        # Create the destination directory if it doesn't exist
        if not os.path.exists(dest_dir):
            os.makedirs(dest_dir)
        
        # Move the previous image file to the destination directory
        shutil.move(prev_image_file, dest_dir)
    
    # Display the next image
    display_next_image()

# Create an accept button
accept_button = Button(root, text='Accept', command=lambda: handle_button_click('accept'))
accept_button.pack(side=LEFT)

# Create a decline button
decline_button = Button(root, text='Decline', command=lambda: handle_button_click('decline'))
decline_button.pack(side=RIGHT)

# Ask the user for the directory path
dir_path = input('Enter the directory path: ')

# Initialize the list of image files and current image index
image_files = []
current_image_index = 0

# Loop through the files in the directory
for filename in os.listdir(dir_path):
    # Check if the file is an image
    if filename.endswith('.jpg') or filename.endswith('.png'):
        # Create the full file path and add it to the list of image files
        file_path = os.path.join(dir_path, filename)
        image_files.append(file_path)

# Display the first image
display_next_image()

# Run the main loop
root.mainloop()