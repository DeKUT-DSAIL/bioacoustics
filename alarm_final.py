
import os
import sys
from adc import *
from time import sleep

gate_pulse = digitalio.DigitalInOut(board.D18) #Set the GPIO PIN 3 as a digital I/O pin
gate_pulse.direction=digitalio.Direction.OUTPUT #Set GPIO PIN 3 as an output


try:
    count=0 # Initialize count at zero 
    while True:
        voltage=volt()
        print(voltage)
        count+=1
        if count%10==0:
            voltage_csv()  #Call the function to save the voltage in a csv file after every 300 seconds == 5 minutes
        if voltage>2.8 and voltage<=3:
            print('Voltage is low')
        elif voltage<2.8:
            print('voltage is extremely low!!!')
            sleep(120)
            voltage=volt()
            voltage_csv()
            if voltage>2.8:
                print(voltage,'\nBattery has recovered.')
            elif voltage<=2.8:
                print('The system will shutdown in a few.')
                alarm()                                      #Call the alarm function to set the alarm.
                gate_pulse.value=True #Set GPIO pin 18 high to latch the timer circuit
                sleep(0.5)
                gate_pulse.value=False
                os.system('sudo shutdown now') #Shutdown the Pi 
        sleep(30)
except KeyboardInterrupt:
        sys.exit()
