
## Install the Adafruit_MCP3008 libraries before running this code


import os
import sys
import csv
import datetime
from time import sleep
import Adafruit_MCP3008
import RPi.GPIO as GPIO
import Adafruit_GPIO.SPI as SPI



GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(11,GPIO.OUT)

delay = 5        # Initialise delay to be 5 seconds

#This program uses Hardware SPI
# Hardware SPI Configuration
HW_SPI_PORT = 0 # Set the SPI Port. Raspi has two.
HW_SPI_DEV  = 0 # Set the SPI Device


# Instantiate the mcp class from Adafruit_MCP3008 module and set it to 'mcp'.

mcp = Adafruit_MCP3008.MCP3008(spi=SPI.SpiDev(HW_SPI_PORT, HW_SPI_DEV))

# Set the analog pin to input the voltage to pin zero of the MCP ADC
analog_port =0

# Read the analog input and convert to voltage
def volt():
        val = mcp.read_adc(analog_port)
	voltage=(3.3*val/1023)*2
        return voltage
date_object = str(datetime.date.today())
date_object='/home/pi/VoltageData/'+date_object+'.csv'

#This function saves the time and voltage readings in a CSV file format
#The file is saved with that specific day's date as the name
def voltage_csv():
	l1=[]
	now=datetime.datetime.now()
	current_time = now.strftime("%H:%M:%S")
	l1.extend((current_time,voltage))
	with open(date_object,mode='a') as file:
		create=csv.writer(file)
		create.writerow(l1)

try:
    while True:
        voltage=volt()
        print(voltage)
	voltage_csv()
        sleep(2)
        if voltage>=1.5 and voltage<=2:
            print('Voltage is low')
            sleep(0.5)
        elif voltage<1.5:
            print('voltage is extremely low!!!')
            sleep(delay)
            voltage=volt()
            if voltage>1.5 and voltage<2:
                print('Battery has recovered but still low!!!')
            elif voltage<=1.5:
                GPIO.output(11,True)
                sleep(1)
                os.system('shutdown now')
except KeyboardInterrupt:
        sys.exit()



