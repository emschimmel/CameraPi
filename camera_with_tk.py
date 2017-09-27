import os
import Tkinter as tk
from picamera import PiCamera
import time
from time import sleep
from PIL import Image,ImageTk

file_path = '/home/pi/photobooth/pics/' # path to save images
camera = PiCamera()
capture_delay = 1 # delay between pics
total_pics = 5 # number of pics to be taken
real_path = os.path.dirname(os.path.realpath(__file__))
filename = ""
gif_delay = 100 # How much time between frames in the animated gif
restart_delay = 10 # how long to display finished message before beginning a new session
now = time.strftime("%Y-%m-%d-%H-%M-%S") #get the current date and time for the start of the filename

def make_filename(itteration):
	global filename 
	filename = file_path + now + '-0' + str(itteration) + '.jpg'

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

def make_gif():
	for x in range(1, total_pics+1): #batch process all the images
		graphicsmagick = "gm convert -size 500x500 " + file_path + now + "-0" + str(x) + ".jpg -thumbnail 500x500 " + file_path + now + "-0" + str(x) + "-sm.jpg"
		os.system(graphicsmagick) #do the graphicsmagick action

	graphicsmagick = "gm convert -delay " + str(gif_delay) + " " + file_path + now + "*-sm.jpg " + file_path + now + ".gif" 
	os.system(graphicsmagick) #make the .gif
	#graphicsmagick = "gm convert -delay " + str(gif_delay) + " " + file_path + now + "*.jpg " + file_path + now + ".gif" 
	#os.system(graphicsmagick) #make the .gif
	generatedGif = Image.open(file_path + now + ".gif" )
	tkimage1 = ImageTk.PhotoImage(generatedGif)
   	panel1.configure(image=tkimage1)
   	panel1.image = tkimage1
	

def photoloop():
	reset_bar()
	for count in range(1, total_pics+1):
		make_filename(count)
		take_photo()
#		update_bar()
		sleep(capture_delay)
	make_gif()

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
previewImage = new_photo()
tkimage1 = ImageTk.PhotoImage(previewImage)

panel1 = tk.Label(root, image=tkimage1)
#panel1.pack(side='top', fill='both', expand='yes')bn
panel1.place(y=50,x=0, width=w, height=(h-50))

# save the panel's image from 'garbage collection'
panel1.image = tkimage1

# Add some buttons
buttonrow = tk.Frame(root)
buttonrow.place(y=0,x=0)	

button = tk.Button(buttonrow, text='Red Button',command = lambda: photoloop())
button.pack(side='left')
button = tk.Button(buttonrow, text='CLOSE',command = lambda: root.destroy())
button.pack(side='left')


		
root.mainloop()		
photoloop()