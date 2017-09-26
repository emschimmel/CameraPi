import os
import Tkinter as tk
from picamera import PiCamera
from time import sleep
from PIL import Image,ImageTk

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
	global previewImage
	previewImage = new_photo()
   	tkimage1 = ImageTk.PhotoImage(previewImage)
   	panel1.configure(image=tkimage1)
   	panel1.image = tkimage1

def new_photo():
	camera.capture(filename)
	return Image.open(filename)


def update_bar():
	global previewImage
   	miniImage = ImageTk.PhotoImage(previewImage)
	button = tk.Label(buttonrow, image=miniImage, width=100, height=50)
	button.pack(side='left')

def reset_bar():
	for widget in buttonrow.winfo_children():
		widget.destroy()
	
	button = tk.Button(buttonrow, text='Red Button',command = lambda: photoloop(), width=100, height=50)
	button.pack(side='left')
	button = tk.Button(buttonrow, text='CLOSE',command = lambda: root.destroy())
	button.pack(side='left')


def photoloop():
#	reset_bar()
	for count in range(1, total_pics+1):
		make_filename(count)
		take_photo()
		update_bar()
		sleep(capture_delay)

make_filename(1)		
#============================
# Optional display here
#============================

# Setup a window
root = tk.Tk()
root.title('Photobooth')

w = 640
h = 320
root.geometry("%dx%d+%d+%d" % (w, h, 0, 0))

# root has no image argument, so use a label as a panel
#previewImage = new_photo()
#tkimage1 = ImageTk.PhotoImage(previewImage)

#panel1 = tk.Label(root, image=tkimage1)
#panel1.pack(side='top', fill='both', expand='yes')

# save the panel's image from 'garbage collection'
#panel1.image = tkimage1

# Add some buttons
buttonrow = tk.Frame(root)
buttonrow.place(y=0,x=0)	

button = tk.Button(buttonrow, text='Red Button',command = lambda: photoloop())
button.pack(side='left')
button = tk.Button(buttonrow, text='CLOSE',command = lambda: root.destroy())
button.pack(side='left')


		
		
#photoloop()