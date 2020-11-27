import os
import sys
import board
import busio
import logging
import argparse
import digitalio
import subprocess
from time import sleep
from datetime import datetime

sleep(30) #delay for thirty seconds to have the pi's time set

logging.basicConfig(filename='power.log',
                    level=logging.DEBUG,
                    format='%(asctime)s:%(levelname)s:%(message)s')



try:

    import adc
    import rtc

    parser = argparse.ArgumentParser(description='Monitors the batter voltage and control wake up and shutdown of the system')

    parser.add_argument('-d_d',
                            '--depth_of_discharge',
                            type=int,
                            default=2.8,
                            metavar='',
                            help='The cut off voltage.')

    parser.add_argument('-w_h',
                            '--wake_hour',
                            type=int,
                            default=5,
                            metavar='',
                            help='The hour (24 hour clock system) the pi should wake up.')


    parser.add_argument('-s_h',
                            '--shutdown_hour',
                            type=int,
                            default=11,
                            metavar='',
                            help='The hour in 24 hour clock system the pi should shutdown.')

    parser.add_argument('-s_n',
                            '--storage_name',
                            type=str,
                            default='none',
                            metavar='',
                            help="""Name of the external storage. Default is 'none'. If no storage
                            name is passed the program will store the voltage reading csv files in
                            the SD card. The external device should not be named as 'none'!!!""")

    parser.add_argument('-d_n',
                            '--directory_name',
                            type=str,
                            default='battery-voltage',
                            metavar='',
                            help='Name of directory to store datestamped voltage readings csv files')

    args = parser.parse_args()


    gate_pulse = digitalio.DigitalInOut(board.D18) #Set the GPIO PIN 3 as a d$
    gate_pulse.direction = digitalio.Direction.OUTPUT #Set GPIO PIN 3 as an out$

    def sd_card():
        """Returns a string which is the path to store the voltage reading csv
        in the SD card. Called when there is no external storage, or when the
        system can't write to the external storage"""

        folder_path = os.path.join('/home/pi/', args.directory_name)
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)
        path = os.path.join(folder_path, name_by_date)
        return path


    def external_storage():
        """Returns a string which is the path to store the voltage reading csv in
        the external storage. Called when the user plugs in an external storage
        device and parse its name in command line"""

        folder_path = os.path.join('/media/pi/', args.storage_name, args.directory_name)
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)
        path = os.path.join(folder_path, name_by_date)
        return path


    def rpi_shutdown(message):
        print('The system will shutdown in a few.')
        rtc.alarm(hour)                                      #Call the al$
        gate_pulse.value = True #Set GPIO pin 18 high to gate trigger the timer circuit thyristor
        sleep(0.5)
        gate_pulse.value = False
        logging.info(message)
        subprocess.call(['sudo', 'shutdown' ,'now']) #Shutdown the Pi

    count = 0 # Initialize count at zero

    while True:
        try:

            t = datetime.now() #get the current time of the pi
            hour = int(t.strftime('%H'))
            if hour >= args.shutdown_hour:
                message = 'Shutting down time'
                rpi_shutdown(message)
            voltage = adc.volt()
            print(voltage)
            count += 1

            if count % 10 == 0:
                name_by_date = t.strftime('%Y-%m-%d') + '.csv'
                current_time = t.strftime('%H-%M-%S')
                try:
                    if args.storage_name != 'none':
                        path = external_storage()
                        adc.voltage_csv(path, current_time, voltage)  #Call the function to save the voltage in a csv file

                    else:
                        path = sd_card()
                        adc.voltage_csv(path, current_time, voltage)  #Call the function to save the voltage in a csv file

                except Exception as storage_error:
                    logging.info(str(storage_error))
                    path = sd_card()
                    adc.voltage_csv(path, current_time, voltage)  #Call the function to save the voltage in a csv file

            if voltage <= args.depth_of_discharge:
                sleep(120) #sleep for 2 minutes
                voltage = adc.volt()
                if voltage > args.depth_of_discharge:
                    print(voltage,'\nBattery has recovered.')
                elif voltage <= args.depth_of_discharge:
                    message = 'Shutting down due to low battery voltage'
                    rpi_shutdown(message)
            sleep(30)
        except KeyboardInterrupt:
            sys.exit()

except Exception as err:
    logging.info(str(err))
