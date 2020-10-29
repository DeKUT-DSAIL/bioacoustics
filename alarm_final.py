import os
import sys
import board
import busio
import argparse
import digitalio
from time import sleep
from rtc import time_dict, alarm
from adc import volt, voltage_csv


parser = argparse.ArgumentParser(description='Save Audio Recordings')
parser.add_argument('-d',
                    '--depth_of_discharge',
                    type=float,
                    metavar='',
                    default=2.8,
                    help='The lowest voltage the battery should be discharged to.')

parser.add_argument('-s',
                    '--shutdown',
                    type=int,
                    metavar='',
                    default=10,
                    help='The time the raspberry pi should shutdown.')

parser.add_argument('-w',
                    '--wake_hour',
                    type=int,
                    metavar='',
                    default=5,
                    help='The time the raspberrypi should wake up')

parser.add_argument('-p',
                    '--path',
                    type=str,
                    metavar='',
                    help='path to the external storage device')

args = parser.parse_args()

"""The following three lines reate a folder in the external
storage device to store voltage values"""

folder_path = args.path + '/battery-voltage/'
if not os.path.exists(folder_path):
    os.makedirs(folder_path)

"""The following 3 lines create a csv file labled as that day's 
date i.e. yyyy-mm-dd"""
t = time_dict()
name_by_date = str(t['tm_year']) + '-' + str(t['tm_mon']) + '-' + str(t['tm_mday'])
file_name_by_date = folder_path + name_by_date + '.csv'


gate_pulse = digitalio.DigitalInOut(board.D18) #Set the GPIO PIN 3 as a d$
gate_pulse.direction = digitalio.Direction.OUTPUT #Set GPIO PIN 3 as an out$



def rpi_shutdown():
    print('The system will shutdown in a few.')
    alarm(args.wake_hour)                                      #Call the al$
    gate_pulse.value = True #Set GPIO pin 18 high to latch the $
    sleep(0.5)
    gate_pulse.value = False
    os.system('sudo shutdown now') #Shutdown the Pi

count = 0 # Initialize count at zero

while True:
    try:
        t = time_dict() #read the rtc time
        if t['tm_hour'] >= args.shutdown:
            rpi_shutdown()
        voltage = volt()
        print(voltage)
        count += 1
        if count%10 == 0:
            voltage_csv(args.path, folder_path, file_name_by_date)  #Call the function to save the voltage in a csv file

        #if voltage > 2.8 and voltage <= 3:
        #    print('Voltage is low')

        if voltage <= args.depth_of_discharge:
            #print('voltage is extremely low!!!')
            sleep(120) #sleep for 2 minutes
            voltage = volt()
            voltage_csv(args.path, folder_path)
            if voltage > args.depth_of_discharge:
                print(voltage,'\nBattery has recovered.')
            elif voltage <= args.depth_of_discharge:
                rpi_shutdown()
        sleep(30)
    except KeyboardInterrupt:
        sys.exit()




