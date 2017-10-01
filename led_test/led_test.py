import ConfigParser
from time import sleep
try:
	import RPi.GPIO as GPIO
	GPIO.setmode(GPIO.BOARD)                                                                                                    
except ImportError:
	print('GPIO unavailable')
 
class led_test:
	config = ConfigParser.RawConfigParser()
	config.read('config.properties')

	def __init__(self):
		for lednumber in range(1, 17):
			self.setup_led(lednumber)	

		for lednumber in range(1, 17):
			self.turn_led_on(lednumber, True)	
			sleep(0.25)
		sleep(5)
		for lednumber in range(1, 17):
			self.turn_led_on(lednumber, False)	
			sleep(0.25)

	def setup_led(self, lednumber):
		int_led_value = int(self.config.get('Leds', 'led_'+`lednumber`))
#		try:
		GPIO.setup(int_led_value, GPIO.OUT)
#		except:
#			print('GPIO unavailable, unable to setup led_'+`lednumber`)


	def turn_led_on(self, lednumber, status):
		int_led_value = int(self.config.get('Leds', 'led_'+`lednumber`))
#		try:
		GPIO.output(int_led_value,status) #turn on the LED
#		except:
#			print('GPIO unavailable, unable to turn led_'+`lednumber`+' to '+`status`)
			
led_test()