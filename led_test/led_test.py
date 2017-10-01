import ConfigParser
from time import sleep
try:
	import RPi.GPIO as GPIO
except ImportError:
	print('GPIO unavailable')
 
class led_test:
	config = ConfigParser.RawConfigParser()
	config.read('config.properties')

	def __init__(self):
		for lednumer in range(1, 17):
			self.turn_led_on(lednumer, True)	
			sleep(0.25)
		sleep(5)
		for lednumer in range(1, 17):
			self.turn_led_on(lednumer, False)	
			sleep(0.25)


	def turn_led_on(self, lednumber, status):
		try:
			GPIO.output(self.config.get('Leds', 'led_'+`lednumber`),status) #turn on the LED
		except:
			print('GPIO unavailable, unable to turn led_'+`lednumber`+' to '+`status`)
			
led_test()