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
from ast import literal_eval as make_tuple

sleep(90) #delay for 90 seconds to have the pi's time set

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

    parser.add_argument('-w',
                            '--windows',
                            default="((5,11),)",
                            metavar='',
                            help='a tuple of tuples containing time intervals of active hours.')


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


    gate_pulse = digitalio.DigitalInOut(board.D18) #Set the GPIO PIN 18 as a digital pin
    gate_pulse.direction = digitalio.Direction.OUTPUT #Set GPIO PIN 18 as an output pin

    gate_pulse2 = digitalio.DigitalInOut(board.D23)  #set GPIO pin 23 as a digital pin
    gate_pulse2.direction = digitalio.Direction.OUTPUT #set GPIO pin as an output pin

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


    def rpi_shutdown(message, rtc_wake_hour, next_day_flag):
        print('The system will shutdown in a few.')
        rtc.alarm(rtc_wake_hour, next_day_flag)                                      #Call the al$
        gate_pulse.value = True #Set GPIO pin 18 high to gate trigger the timer circuit thyristor
        sleep(0.5)
        gate_pulse.value = False
        logging.info(message)
        subprocess.call(['sudo', 'shutdown' ,'now']) #Shutdown the Pi



    

    def alarm_hour_generator(current_hour, windows):
        """Generates the hour to set the RTC alarm
        Args: current_hour: current hour
            windows: a tuple of tuples containing time intervals of active hours
        Returns: shutdown_hour-time to shutdown the system
                rtc_wake_hour-time to wake the system
                next_day_flag-a flag that is true if the wake hour is the following day
        """
        
        hours = [hour for hour in range(0,24)]
        
        next_day_flag = True #initialize a flag to take care of days transition as True
        
        if len(windows) == 1:
            shutdown_hour = windows[0][1]
            rtc_wake_hour = windows[0][0]
            
        else:

            active_hours = []

            for window in windows:

                #takes care of a case when there is a window that transitions to the following day
                if window[0] < window[1]:
                    for hour in range(window[0], window[1]):
                        active_hours.append(hour)
                else:
                    for hour in range(window[0], 24):
                        active_hours.append(hour)
                    for hour in range(0, window[1]):
                        active_hours.append(hour)

                    next_day_flag = False #set day transition as false

            wake_up_hours = [window[0] for window in windows]
            shutdown_hours = [window[1] for window in windows]

            inactive_hours = list(set(hours) - set(active_hours))
            active_hours, inactive_hours, wake_up_hours, shutdown_hours



            #case 1: system wakes during an active window
            #case 2: system wakes during inactive hours

            #system wakes during an active window
            if current_hour in active_hours:
                #search for shutdown time
                for indx, window in enumerate(windows):

                    #takes care of a case when there is a window that transitions to the following day
                    if window[0] < window[1]:
                        window_hours = [hour for hour in range(window[0], window[1])]


                    else:

                        window_hours = []
                        for hour in range(window[0], 24):
                            window_hours.append(hour)
                        for hour in range(0, window[1]):
                            window_hours.append(hour)



                    if current_hour in window_hours:
                        shutdown_hour = windows[indx][1]

                        #incase it's not the last window
                        if indx +1 < len(windows):
                            next_day_flag = False #set day transition as false
                            rtc_wake_hour = windows[indx + 1][0]


                        #incase it is the last window
                        else:
                            print('last window')
                            rtc_wake_hour = windows[0][0]

            #system wakes during inactive hours
            #incase it's past the last shutdown hour
            else:
                if current_hour > max(active_hours):
                    shutdown_hour = current_hour
                    rtc_wake_hour = windows[0][0]


                else:
                    hours_of_interest = [(indx, wake_hour) for indx, wake_hour in enumerate(wake_up_hours)
                                        if (wake_hour - current_hour > 0)]
                    print(hours_of_interest)
                    shutdown_hour = current_hour
                    rtc_wake_hour = hours_of_interest[0][1]
                    next_day_flag = False

        return shutdown_hour, rtc_wake_hour, next_day_flag

    count = 0 # Initialize count at zero

    windows = make_tuple(args.windows)

    while True:
        try:
            current_time = datetime.now() #get the current time of the pi
            current_hour = int(current_time.strftime('%H'))
            shutdown_hour, rtc_wake_hour, next_day_flag = alarm_hour_generator(current_hour, windows)
            
            
            if current_hour >= shutdown_hour:
                message = 'Shutting down time'
                rpi_shutdown(message, rtc_wake_hour, next_day_flag)
            voltage = adc.volt()
            print(voltage)
            count += 1

            if count % 10 == 0:
                gate_pulse2.value = True #Set GPIO pin 23 high to refresh the stored charge in power supply board capacitor
                sleep(0.5)
                gate_pulse2.value = False #Set GPIO pin 23 high to low
                name_by_date = current_time.strftime('%Y-%m-%d') + '.csv'
                current_time = current_time.strftime('%H-%M-%S')
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
                    rtc_wake_hour = args.windows[0][0]
                    next_day_flag = True
                    rpi_shutdown(message, rtc_wake_hour, next_day_flag)
            sleep(30)
        except KeyboardInterrupt:
            sys.exit()

except Exception as err:
    logging.info(str(err))

