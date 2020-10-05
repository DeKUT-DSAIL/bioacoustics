import sys
from rtc import *
from adc import *
from time import sleep

t=rtc.datetime    #read the rtc time and assign it variable t
voltage=round(volt(),1)    #read the adc voltage reading and assign it variable voltage
sleep_time=30*60  #thirty minutes

#print(voltage, t.tm_hour)
gate_pulse = digitalio.DigitalInOut(board.D13) #Set the GPIO PIN 13 as a digital
gate_pulse.direction=digitalio.Direction.OUTPUT #Set GPIO PIN 13 as an output

while True:
	try:
		if voltage>=3.9 and t.tm_hour>=9 and t.tm_hour<=16:
			gate_pulse.value=True 	#drive an npn transistor to cut off the solar
			sleep(sleep_time)       #sleep for thirty minutes the connects the solar to the battery for charging
			gate_pulse.value=False
			sleep(1)
	except KeyboardInterrupt:
		gate_pulse.value=False
		break



