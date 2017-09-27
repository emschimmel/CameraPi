import os
import Tkinter as tk
from picamera import PiCamera
import time
from time import sleep
from PIL import Image,ImageTk
import random


class CameraDisplay:

    #--------------------------------------------------------------
    #   global vars
    #--------------------------------------------------------------
    global file_path
    global intervalBeforeScreensaver
    global intervalInScreensaver
    global capture_delay
    global total_pics
    
    global displayWith
    global displayHeight
    global root
    global mainwindow
    global mainwindowSubFrame
    global mainwindowPreviewBar
    global staticbuttonrow
    global activePage
    global tkimage1
    global camera
    
	#--------------------------------------------------------------
    #   config assigns
    #--------------------------------------------------------------
    intervalBeforeScreensaver = 10
    intervalInScreensaver = 5
    capture_delay = 1 # delay between pics
    total_pics = 5
    displayWith = 640
    displayHeight = 320
    file_path = '/home/pi/photobooth/pics/' # path to save images
    windowTitle = 'Photobooth'
    camera = PiCamera()
    
    #--------------------------------------------------------------
    #   private functions
    #--------------------------------------------------------------
    def photo_loop(self):
		for count in range(1, total_pics+1):
			tkimage1 = self.take_picture(count)
   			panel1.configure(image=tkimage1)
   			panel1.image = tkimage1
   			
			miniImage = ImageTk.PhotoImage(previewImage)
			label = tk.Label(mainwindowPreviewBar, image=miniImage, width=100, height=50)
			label.pack(side='left')
			sleep(capture_delay)
		make_gif()

    def take_picture(self, count):
		filename = file_path + 'image' + str(count) + '.jpg'
		camera.capture(filename)
		currenctImage = Image.open(filename)
		return ImageTk.PhotoImage(currenctImage)

    #--------------------------------------------------------------
    #   lambda function
    #--------------------------------------------------------------
    def click_red_button(self):
    	global activePage
    	print('red button clicked')
    	if activePage is Page.READY:
    		self.drawTakingPicturePage() # Camera ready, start making a picture
    	elif activePage is Page.CAMERA:
    		self.drawTakingPicturePage() # Make a new picture
    	elif activePage is Page.SCREENSAVER:	
    		self.drawCameraReadyPage() # Cancel screensaver, show ready page

    #--------------------------------------------------------------
    #   window
    #--------------------------------------------------------------
    root = tk.Tk()
    root.title(windowTitle)
    root.geometry("%dx%d+%d+%d" % (displayWith, displayHeight, 0, 0))
    
    #main frame
    mainwindow = tk.Frame(root)
    mainwindow.place(y=20,x=0, width=displayWith, height=(displayHeight-20))
    
    #--------------------------------------------------------------
    #   Controll buttonrow
    #--------------------------------------------------------------
    staticbuttonrow = tk.Frame(root)
    staticbuttonrow.place(y=0,x=0)
    def drawstaticbuttons(self):
        button = tk.Button(staticbuttonrow, text='Close', command = lambda: root.destroy())
        button.pack(side='left')
        button = tk.Button(staticbuttonrow, text='Red Button', command = lambda: self.click_red_button())
        button.pack(side='left',)
    
    #--------------------------------------------------------------
    #   page 1 -- Camera ready
    #--------------------------------------------------------------
    def drawCameraReadyPage(self):
    	global activePage
    	activePage = Page.READY
    	for widget in mainwindow.winfo_children():
            widget.destroy()
        mainwindowSubFrame = tk.Frame(mainwindow)
        mainwindowSubFrame.place(y=100,x=0, width=displayWith, height=50)
        label = tk.Label(mainwindowSubFrame, text="Camera ready", fg = "white", bg = "purple", font = "Helvetica 16 bold", width=displayWith)
        label.pack()
        
    #--------------------------------------------------------------
    #   page 2 -- Taking a picture
    #--------------------------------------------------------------
    def drawTakingPicturePage(self):
    	global activePage
    	global tkimage1
    	activePage = Page.CAMERA
    	for widget in mainwindow.winfo_children():
            widget.destroy()
        mainwindowSubFrame = tk.Frame(mainwindow)
        mainwindowSubFrame.place(y=200,x=0, width=displayWith, height=(displayHeight-250))
        tkimage1 = self.take_picture(0)
        panel1 = tk.Label(mainwindowSubFrame, image=tkimage1)
        panel1.place(y=50,x=0, width=w, height=(h-50))
        self.photo_loop()
        sleep(intervalBeforeScreensaver)
        self.drawScreensaverPage()
    
    #--------------------------------------------------------------
    #   page 3 -- Screensaver
    #--------------------------------------------------------------
    def drawScreensaverPage(self):
    	global activePage
    	global tkimage1
    	activePage = Page.SCREENSAVER
    	for widget in mainwindow.winfo_children():
        	widget.destroy()
        mainwindowSubFrame = tk.Frame(mainwindow)
        mainwindowSubFrame.place(y=100,x=0, width=displayWith, height=50)

        screenSaverItemlabel = tk.Label(mainwindowSubFrame, image=tkimage1)
        screenSaverItemlabel.pack()
        while activePage is Page.SCREENSAVER:
        	previewImage = self.nextPreview()
        	tkimage1 = ImageTk.PhotoImage(previewImage, format="gif -index 2")
        	screenSaverItemlabel.configure(image=tkimage1)
        	screenSaverItemlabel.image = tkimage1	
        	sleep(intervalInScreensaver)
        	
    def nextPreview(self):
    	root, dirs, files=next(os.walk(file_path))
    	imageCollection=list(filter(lambda filename:filename.endswith('.gif'), files))
    	if not imageCollection:
			imageCollection=list(filter(lambda filename:filename.endswith('.jpg'), files))
    	return random.choice(imageCollection)
    	
    
    #--------------------------------------------------------------
    #   run
    #--------------------------------------------------------------
    def __init__(self):
    	self.drawstaticbuttons()
        self.drawCameraReadyPage()
        root.mainloop()
        
        
from enum import Enum
class Page(Enum):
    READY = 'ready'
    CAMERA = 'camera'
    SCREENSAVER = 'screensaver'

CameraDisplay()
    
    