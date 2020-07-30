
## Install the Adafruit_MCP3008 libraries before running this code


import os
import sys
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
        return (3.3*val/1023)




try:
    while True:
        voltage=volt()
        print(voltage)
        sleep(0.5)
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
                sleep(2)
                GPIO.output(11,False)
                sleep(2)
                os.system('shutdown now')
except KeyboardInterrupt:
        sys.exit()



