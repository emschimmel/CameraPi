from picamera import PiCamera
from time import sleep

camera = PiCamera()
imagefile = "image"

def takephoto(itteration):
	jpgword = ".jpg"
	camera.capture(imagefile+`itteration`+jpgword)

def photoloop():
	count = 0
	while (count < 5):
		sleep(1)
		takephoto(count)
		
		count = count + 1
		
photoloop()