import os
import shutil
from tkinter import *
from tkinter import messagebox
from tkinter import filedialog
from PIL import Image, ImageTk
import imageio
from datetime import datetime

# Create the main window
root = Tk()

# Set the window title
root.title('Image Viewer')

# Create a label to display the image or video
media_label = Label(root)
media_label.pack()

# Create a function to load the images and videos from a directory
def load_media():
    global dir_path, media_files, current_media_index
    
    # Ask the user for the directory path
    dir_path = filedialog.askdirectory()
    
    # Initialize the list of media files and current media index
    media_files = []
    current_media_index = 0
    
    # Check if a directory was selected
    if dir_path:
        # Loop through the files in the directory
        for filename in os.listdir(dir_path):
            # Check if the file is an image or video
            if filename.endswith(('.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff', '.mp4', '.avi', '.mov', '.flv', '.wmv')):
                # Create the full file path and add it to the list of media files
                file_path = os.path.join(dir_path, filename)
                media_files.append(file_path)
        
        # Display the first media file
        display_next_media()

# Create a function to display the next media file
def display_next_media():
    global current_media_index
    
    # Check if there are more media files to display
    if current_media_index < len(media_files):
        # Get the next media file path
        media_file = media_files[current_media_index]
        
        # Check if the media file is an image or video
        if media_file.endswith(('.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff')):
            # Open the next image file
            img = Image.open(media_file)
            
            # Resize the image to fit the window
            img = img.resize((400, 400), Image.ANTIALIAS)
            
            # Convert the image to a PhotoImage object
            photo = ImageTk.PhotoImage(img)
            
            # Update the media label with the new image
            media_label.config(image=photo)
            media_label.image = photo
        else:
            # Open the next video file
            video = imageio.get_reader(media_file)
            
            # Get the video metadata
            meta_data = video.get_meta_data()
            
            # Calculate the video frame delay in milliseconds
            frame_delay = int(1000 / meta_data['fps'])
            
            # Loop through the video frames
            for frame in video:
                # Convert the frame to an image object
                img = Image.fromarray(frame)
                
                # Resize the image to fit the window
                img = img.resize((400, 400), Image.ANTIALIAS)
                
                # Convert the image to a PhotoImage object
                photo = ImageTk.PhotoImage(img)
                
                # Update the media label with the new frame
                media_label.config(image=photo)
                media_label.image = photo
                
                # Update the window and wait for the frame delay
                root.update_idletasks()
                root.after(frame_delay)
        
        # Increment the current media index
        current_media_index += 1
    else:
        # Ask the user if they want to quit or load another directory
        answer = messagebox.askyesno('No more files', 'There are no more files to display. Do you want to load another directory?')
        
        # Check if the user wants to load another directory
        if answer:
            load_media()
        else:
            root.quit()

# Create a function to handle button clicks
def handle_button_click(action):
    global current_media_index
    
    # Check if a media file was displayed
    if current_media_index > 0:
        # Get the previous media file path
        prev_media_file = media_files[current_media_index - 1]
        
        # Create the destination directory path
        dest_dir = os.path.join(dir_path, action)
        
        # Check if the destination directory already exists
        if os.path.exists(dest_dir):
            # Ask the user if they want to create another subdirectory with a timestamp
            answer = messagebox.askyesno('Subdirectory exists', f'The {action} subdirectory already exists. Do you want to create another subdirectory with a timestamp?')
            
            # Check if the user wants to create another subdirectory
            if answer:
                # Get the current timestamp
                timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
                
                # Append the timestamp to the destination directory path
                dest_dir = os.path.join(dest_dir, timestamp)
        else:
            # Create the destination directory
            os.makedirs(dest_dir)
        
        # Move the previous media file to the destination directory
        shutil.move(prev_media_file, dest_dir)
    
    # Display the next media file
    display_next_media()

# Create an accept button
accept_button = Button(root, text='Accept', command=lambda: handle_button_click('accept'))
accept_button.pack(side=LEFT)

# Create a decline button
decline_button = Button(root, text='Decline', command=lambda: handle_button_click('decline'))
decline_button.pack(side=RIGHT)

# Initialize global variables
dir_path = ''
media_files = []
current_media_index = 0

# Load the initial media files from a directory
load_media()

# Run the main loop
root.mainloop()