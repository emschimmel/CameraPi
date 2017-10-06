#!/usr/bin/env python
# created by chris@drumminhands.com
# see instructions at http://www.drumminhands.com/2014/06/15/raspberry-pi-photo-booth/

import os
import shutil
import glob
import time
import traceback
import config # this is the config python file config.py
from time import sleep
try:
	import RPi.GPIO as GPIO
except:
	print('GPIO unavailable')
try:
	import picamera # http://picamera.readthedocs.org/en/release-1.4/install2.html
except:
	print('picamera unavailable')
	config.file_path = './mock/'
import atexit
import sys
import socket
import random
import threading
import pygame
from pygame.locals import QUIT, KEYDOWN, K_ESCAPE

from signal import alarm, signal, SIGALRM, SIGKILL

########################
### Variables Config ###
########################
led_pin = 7 # LED 
btn_pin = 18 # pin for the start button

total_pics = 4 # number of pics to be taken
capture_delay = 1 # delay between pics
prep_delay = 5 # number of seconds at step 1 as users prep to have photo taken
gif_delay = 100 # How much time between frames in the animated gif
restart_delay = 10 # how long to display finished message before beginning a new session

high_res_w = 1296 # width of high res image, if taken
high_res_h = 972 # height of high res image, if taken

#############################
### Variables that Change ###
#############################
# Do not change these variables, as the code will change it anyway
transform_x = config.monitor_w # how wide to scale the jpg when replaying
transfrom_y = config.monitor_h # how high to scale the jpg when replaying
offset_x = 0 # how far off to left corner to display photos
offset_y = 0 # how far off to left corner to display photos
replay_delay = 1 # how much to wait in-between showing pics on-screen after taking
replay_cycles = 2 # how many times to show each photo on-screen after taking

####################
### Other Config ###
####################
real_path = os.path.dirname(os.path.realpath(__file__))
waiting_for_screensaver = False

class playpreview_threadclass(threading.Thread):

	def __init__(self, threadID, name, counter):
		threading.Thread.__init__(self)
		self.threadID = threadID
		self.name = name
		self.counter = counter
	
	def run(self):
		print('running screensaver')
		global waiting_for_screensaver
		while True:
			if waiting_for_screensaver:
				print('screensaver waits 15')
				time.sleep(15)
				if waiting_for_screensaver: # still waiting?
					print('I still waited')
					self.play_screensaver()	# play!	

	def next_image(self):
		root, dirs, files=next(os.walk(config.file_path))
		imageCollection=list(filter(lambda filename:filename.endswith('.gif'), files))
		if not imageCollection:
			imageCollection=list(filter(lambda filename:filename.endswith('.jpg'), files))
		return random.choice(imageCollection)

	def play_screensaver(self):
		global waiting_for_screensaver
		while waiting_for_screensaver:
			filename = self.next_image()
			print(filename)
			show_image(config.file_path+filename)
			time.sleep(3)

class wait_for_button_threadclass(threading.Thread):
	def __init__(self, threadID, name, counter):
		threading.Thread.__init__(self)
		self.threadID = threadID
		self.name = name
		self.counter = counter
	
	def run(self):
		print('running button')
		while True:
			try:
				GPIO.output(led_pin,True); #turn on the light showing users they can push the button
				GPIO.wait_for_edge(btn_pin, GPIO.FALLING)
				time.sleep(config.debounce) #debounce
			except:
				print('GPIO unavailable, going to sleep for 5')
				time.sleep(5) # screensaver
			start_photobooth()

try:
	# GPIO setup
	GPIO.setmode(GPIO.BOARD)
	GPIO.setup(led_pin,GPIO.OUT) # LED
	GPIO.setup(btn_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
	GPIO.output(led_pin,False) #for some reason the pin turns on at the beginning of the program. Why?
except:
	print('GPIO unavailable')

# initialize pygame
pygame.init()
pygame.display.set_mode((config.monitor_w, config.monitor_h))
screen = pygame.display.get_surface()
pygame.display.set_caption('Photo Booth Pics')
pygame.mouse.set_visible(False) #hide the mouse cursor
pygame.display.toggle_fullscreen()

#################
### Functions ###
#################

# clean up running programs as needed when main program exits
def cleanup():
  print('Ended abruptly')
  pygame.quit()
  try:
  	GPIO.cleanup()
  except:
	print('GPIO unavailable')
atexit.register(cleanup)

# A function to handle keyboard/mouse/device input events    
def input(events):
    for event in events:  # Hit the ESC key to quit the slideshow.
        if (event.type == QUIT or
            (event.type == KEYDOWN and event.key == K_ESCAPE)):
            pygame.quit()
                
#delete files in folder
def clear_pics(channel):
	files = glob.glob(config.file_path + '*')
	for f in files:
		os.remove(f) 
	#light the lights in series to show completed
	print "Deleted previous pics"
	try:
		for x in range(0, 3): #blink light
			GPIO.output(led_pin,True); 
			sleep(0.25)
			GPIO.output(led_pin,False);
			sleep(0.25) 
	except:
		print('GPIO unavailable')

# set variables to properly display the image on screen at right ratio
def set_demensions(img_w, img_h):
	# Note this only works when in booting in desktop mode. 
	# When running in terminal, the size is not correct (it displays small). Why?

    # connect to global vars
    global transform_y, transform_x, offset_y, offset_x

    # based on output screen resolution, calculate how to display
    ratio_h = (config.monitor_w * img_h) / img_w 
    transform_x = config.monitor_w
    transform_y = config.monitor_h
    offset_y = offset_x = 0

    # uncomment these lines to troubleshoot screen ratios
#     print str(img_w) + " x " + str(img_h)
#     print "ratio_h: "+ str(ratio_h)
#     print "transform_x: "+ str(transform_x)
#     print "transform_y: "+ str(transform_y)
#     print "offset_y: "+ str(offset_y)
#     print "offset_x: "+ str(offset_x)

# display one image on screen
def show_image(image_path):

	# clear the screen
	screen.fill( (0,0,0) )

	# load the image
	img = pygame.image.load(image_path)
	img = img.convert() 

	# set pixel dimensions based on image
	set_demensions(img.get_width(), img.get_height())

	# rescale the image to fit the current display
	img = pygame.transform.scale(img, (transform_x,transfrom_y))
	screen.blit(img,(offset_x,offset_y))
	pygame.display.flip()

# display a blank screen
def clear_screen():
	screen.fill( (0,0,0) )
	pygame.display.flip()

# display a group of images
def display_pics(jpg_group):
    for i in range(0, replay_cycles): #show pics a few times
		for i in range(1, total_pics+1): #show each pic
			show_image(config.file_path + jpg_group + "-0" + str(i) + ".jpg")
			time.sleep(replay_delay) # pause 
				
# define the photo taking function for when the big button is pressed 
def start_photobooth(): 

	input(pygame.event.get()) # press escape to exit pygame. Then press ctrl-c to exit python.

	################################# Begin Step 1 #################################
	
	print "Get Ready"
	try:
		GPIO.output(led_pin,False);
	except:
		print('GPIO unavailable')
	show_image(real_path + "/instructions.png")
	sleep(prep_delay)
	
	# clear the screen
	clear_screen()
	try:
		camera = picamera.PiCamera()  
		camera.vflip = False
		camera.hflip = True # flip for preview, showing users a mirror image
		camera.saturation = -100 # comment out this line if you want color images
		camera.iso = config.camera_iso
		camera.resolution = (high_res_w, high_res_h) # set camera resolution to high res
	except:
		print('picamera unavailable')
	################################# Begin Step 2 #################################
	
	print "Taking pics"
	
	now = time.strftime("%Y-%m-%d-%H-%M-%S") #get the current date and time for the start of the filename
	waiting_for_screensaver = False
	if config.capture_count_pics:
		try: # take the photos
			for i in range(1,total_pics+1):
				camera.hflip = True # preview a mirror image
				camera.start_preview(resolution=(config.monitor_w, config.monitor_h)) # start preview at low res but the right ratio
				time.sleep(2) #warm up camera
				try:
					GPIO.output(led_pin,True) #turn on the LED
				except:
					print('GPIO unavailable')
				filename = config.file_path + now + '-0' + str(i) + '.jpg'
				camera.hflip = False # flip back when taking photo
				camera.capture(filename)
				print(filename)
				try:
					GPIO.output(led_pin,False) #turn off the LED
				except:
					print('GPIO unavailable')
				camera.stop_preview()
				show_image(real_path + "/pose" + str(i) + ".png")
				time.sleep(capture_delay) # pause in-between shots
				clear_screen()
				if i == total_pics+1:
					break
		except:
			print('picamera unavailable, generating images')
			for i in range(1, 5):
				filename = config.file_path + now + '-0' + str(i) + '.jpg'	
				shutil.copy("pose"+str(i)+".png", filename)
				show_image(real_path + "/pose" + str(i) + ".png")
				time.sleep(capture_delay) # pause in-between shots
				clear_screen()
			
		finally:
			try:
				camera.close()
			except:
					print('picamera unavailable')	
	else:
		try: #take the photos
			camera.start_preview(resolution=(config.monitor_w, config.monitor_h)) # start preview at low res but the right ratio
			time.sleep(2) #warm up camera
		
		
			for i, filename in enumerate(camera.capture_continuous(config.file_path + now + '-' + '{counter:02d}.jpg')):
				try:
					GPIO.output(led_pin,True) #turn on the LED
				except:
					print('GPIO unavailable')
				print(filename)
				time.sleep(capture_delay) # pause in-between shots
				try:
					GPIO.output(led_pin,False) #turn off the LED
				except:
					print('GPIO unavailable')
				if i == total_pics-1:
					break
		finally:
			camera.stop_preview()
			camera.close()
		
	########################### Begin Step 3 #################################
	
	input(pygame.event.get()) # press escape to exit pygame. Then press ctrl-c to exit python.
	
	print "Creating an animated gif" 
	
	show_image(real_path + "/processing.png")
	
	graphicsmagick = "gm convert -delay " + str(gif_delay) + " " + config.file_path + now + "*.jpg " + config.file_path + now + ".gif" 
	os.system(graphicsmagick) #make the .gif
	
	########################### Begin Step 4 #################################
	
	input(pygame.event.get()) # press escape to exit pygame. Then press ctrl-c to exit python.
	
	try:
		display_pics(now)
	except Exception, e:
		tb = sys.exc_info()[2]
		traceback.print_exception(e.__class__, e, tb)
		pygame.quit()
		
	print "Done"
	waiting_for_screensaver = True
	show_image(real_path + "/finished2.png")
	
	time.sleep(restart_delay)
	show_image(real_path + "/intro.png");
	try:
		GPIO.output(led_pin,True) #turn on the LED
	except:
		print('GPIO unavailable')

####################
### Main Program ###
####################

## clear the previously stored pics based on config settings
if config.clear_on_startup:
	clear_pics(1)

print "Photo booth app running..." 
try:
	for x in range(0, 5): #blink light to show the app is running
		GPIO.output(led_pin,True)
		sleep(0.25)
		GPIO.output(led_pin,False)
		sleep(0.25)
except:
	print('GPIO unavailable')

show_image(real_path + "/intro.png");

t1 = playpreview_threadclass(1, "Screensaver", 1)
t1.start()
input(pygame.event.get()) # press escape to exit pygame. Then press ctrl-c to exit python.
t2 = wait_for_button_threadclass(2, "Button", 2)
#	t2.setDeamon(True)
t2.start()
