
import os
import sys
from adc import *
from time import sleep

gate_pulse = digitalio.DigitalInOut(board.D18) #Set the GPIO PIN 3 as a digital I/O pin
gate_pulse.direction=digitalio.Direction.OUTPUT #Set GPIO PIN 3 as an output


try:
    count=0
    while True:
        voltage=volt()
        print(voltage)
        count+=1
        if count%10==0:
            voltage_csv()
        if voltage>=3 and voltage<=3.5:
            print('Voltage is low')
        elif voltage<3:
            print('voltage is extremely low!!!')
            sleep(30)
            voltage=volt()
            if voltage>3 and voltage<3.5:
                print(voltage,'\nBattery has recovered but still low!!!')
            elif voltage<=3:
                print('The system will shutdown in a few.')
                alarm()                                      #Call the alarm function to set the alarm.
                gate_pulse.value=True
                sleep(0.5)
                gate_pulse.value=False
                os.system('shutdown now')
        sleep(30)
except KeyboardInterrupt:
        sys.exit()
