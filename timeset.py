import time
import board
import busio
import logging
import datetime
import subprocess
import adafruit_ds3231


logging.basicConfig(filename='time_set.log', level=logging.DEBUG)

try:

    i2c = busio.I2C(board.SCL, board.SDA)

    rtc = adafruit_ds3231.DS3231(i2c)

    t = rtc.datetime


    days_indx_dict = {0:'Mon',
                        1:'Tue',
                        2:'Wed',
                        3:'Thu',
                        4:'Fri',
                        5:'Sat',
                        6:'Sun'}

    months_indx_dict = {1:'Jan',
                        2:'Feb',
                        3:'Mar',
                        4:'Apr',
                        5:'May',
                        6:'Jun',
                        7:'Jul',
                        8:'Aug',
                        9:'Sep',
                        10:'Oct',
                        11:'Nov',
                        12:'Dec'}


    """ The following line formats the time string to take the form
        of this sample: 'Fri Nov 13 14:09:30 EAT 2020. This is then 
        used to set the Pi's time """


    time = (str(days_indx_dict[t.tm_wday]) +
            ' ' +
            str(months_indx_dict[t.tm_mon]) +
            ' '+
            str(t.tm_mday) +
            ' ' +
            str(t.tm_hour) + ':' +  str(t.tm_min) + ':' +  str(t.tm_sec) +
            ' EAT ' +
            str(t.tm_year))



    subprocess.call(['sudo', 'date', '-s', time]) #set the time

except Exception as time_set_error:
    logging.info(str(time_set_error))

