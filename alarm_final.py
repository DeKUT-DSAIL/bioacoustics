import sys
import adc
import rtc
import board
import busio
import argparse
import digitalio
import subprocess
from time import sleep
from datetime import datetime

sleep(30) #delay for thirty seconds to have the pi's time set

DEPTH_OF_DISCHARGE = 2.8 #voltage

SHUTDOWN_HOUR = 10 #10.00am

gate_pulse = digitalio.DigitalInOut(board.D18) #Set the GPIO PIN 3 as a d$
gate_pulse.direction = digitalio.Direction.OUTPUT #Set GPIO PIN 3 as an out$



def rpi_shutdown():
    print('The system will shutdown in a few.')
    rtc.alarm()                                      #Call the al$
    gate_pulse.value = True #Set GPIO pin 18 high to gate trigger the timer circuit thyristor
    sleep(0.5)
    gate_pulse.value = False
    subprocess.call(['sudo', 'shutdown' ,'now']) #Shutdown the Pi

count = 0 # Initialize count at zero

while True:
    try:
        t = datetime.now() #get the current time of the pi
        hour = int(t.strftime('%H'))
        if hour >= SHUTDOWN_HOUR:
            rpi_shutdown()
        voltage = adc.volt()
        print(voltage)
        count += 1
        if count % 10 == 0:
            adc.voltage_csv()  #Call the function to save the voltage in a csv file

        if voltage <= DEPTH_OF_DISCHARGE:
            sleep(120) #sleep for 2 minutes
            voltage = adc.volt()
            adc.voltage_csv()
            if voltage > DEPTH_OF_DISCHARGE:
                print(voltage,'\nBattery has recovered.')
            elif voltage <= DEPTH_OF_DISCHARGE:
                rpi_shutdown()
        sleep(30)
    except KeyboardInterrupt:
        sys.exit()




