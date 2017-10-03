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
		print("setup led "+`lednumber`)
#		try:
		int_led_value = int(self.config.get('Leds', 'led_'+`lednumber`))
		GPIO.setup(int_led_value, GPIO.OUT)
#		except:
#			print('GPIO unavailable, unable to setup led_'+`lednumber`)


	def turn_led_on(self, lednumber, status):
		print("turn led "+`lednumber`+' to '+`status`)
#		try:
		int_led_value = int(self.config.get('Leds', 'led_'+`lednumber`))
		GPIO.output(int_led_value,status) #turn on the LED
#		except:
#			print('GPIO unavailable, unable to turn led_'+`lednumber`+' to '+`status`)
		
class button_test:
	config = ConfigParser.RawConfigParser()
	config.read('config.properties')
	
	global run_main_loop
	
	run_main_loop = False
	
	def __init__(self):
		global run_main_loop
		for buttonnumber in range(1, 2):
			self.setup_button(buttonnumber)	
		run_main_loop = True
	
	def setup_button(self, buttonnumber):
		print("setup button "+`buttonnumber`)
#		try:
		btn_int_value = int(self.config.get('Leds', 'led_'+`buttonnumber`))
		GPIO.setup(btn_int_value, GPIO.IN, pull_up_down=GPIO.PUD_UP)	
#		except:
#			print('GPIO unavailable, unable to setup button_'+`buttonnumber`)


	while run_main_loop:
#		try:
		GPIO.wait_for_edge(btn_pin, GPIO.FALLING)
		print('button pressed')
		time.sleep(0.3) #debounce
#		except:
#			run_main_loop = False
#			print('GPIO unavailable, unable to setup button_'+`buttonnumber`)
		
led_test()
button_test()