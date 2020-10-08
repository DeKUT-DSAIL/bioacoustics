
import os
import sys
from adc import *
from rtc import *
from time import sleep




depth_of_discharge=2.8  #voltage
shutdown_time=9 #9.00 am

gate_pulse = digitalio.DigitalInOut(board.D18) #Set the GPIO PIN 3 as a d$
gate_pulse.direction=digitalio.Direction.OUTPUT #Set GPIO PIN 3 as an out$

def rpi_shutdown():
    print('The system will shutdown in a few.')
    alarm()                                      #Call the al$
    gate_pulse.value=True #Set GPIO pin 18 high to latch the $
    sleep(0.5)
    gate_pulse.value=False
    os.system('sudo shutdown now') #Shutdown the Pi

count=0 # Initialize count at zero

while True:
    try:
        t=rtc.datetime #read the rtc time
        if t.tm_hour>=shutdown_time:
            rpi_shutdown()
        voltage=volt()
        print(voltage)
        count+=1
        if count%10==0:
            voltage_csv()  #Call the function to save the voltage in a csv file

        #if voltage>2.8 and voltage<=3:
        #    print('Voltage is low')

        if voltage<=depth_of_discharge:
            #print('voltage is extremely low!!!')
            sleep(120)
            voltage=volt()
            voltage_csv()
            if voltage>depth_of_discharge:
                print(voltage,'\nBattery has recovered.')
            elif voltage<=depth_of_discharge:
                rpi_shutdown()
        sleep(30)
    except KeyboardInterrupt:
        sys.exit()




