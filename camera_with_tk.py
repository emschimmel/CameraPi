import os
import Tkinter as tk
from picamera import PiCamera
from time import sleep

camera = PiCamera()
fileNamePrefix = "image"
fileNameSufix = ".jpg"
capture_delay = 1 # delay between pics
total_pics = 4 # number of pics to be taken
real_path = os.path.dirname(os.path.realpath(__file__))
filename = ""

def make_filename(itteration):
	global filename 
	filename = fileNamePrefix+`itteration`+fileNameSufix

def take_photo():
	camera.capture(filename)


def update_bar():
	button = tk.Label(buttonrow, image=filename, width=100, height=50)
	button.pack(side='left')

def reset_bar():
	for widget in buttonrow.winfo_children():
		widget.destroy()
	
	button = tk.Button(buttonrow, text='Red Button',command = lambda: photoloop(), width=100, height=50)
	button.pack(side='left')


def photoloop():
	reset_bar()
	for count in range(1, total_pics+1):
		make_filename(count)
		take_photo()
		update_bar()
		sleep(capture_delay)
		
#============================
# Optional display here
#============================

# Setup a window
root = tk.Tk()
root.title('Image')

image1 = take_photo(filename)

w = tkimage1.width()
h = tkimage1.height()
root.geometry("%dx%d+%d+%d" % (w, h, 0, 0))

# root has no image argument, so use a label as a panel
panel1 = tk.Label(root, image=filename)
panel1.pack(side='top', fill='both', expand='yes')

# save the panel's image from 'garbage collection'
panel1.image = filename

# Add some buttons
buttonrow = tk.Frame(root)
buttonrow.place(y=0,x=0)	

button = tk.Button(buttonrow, text='Red Button',command = lambda: photoloop())
button.pack(side='left')


		
		
photoloop()