"""
This program sets the ds3231 rtc alarm to wake
the raspberrypi everyday at 5.00 am. In this program,
.struct_time Class of the python time module is used
to setting the alarm. An example of the time.struct_time Class
object takes the form:

time.struct_time(tm_year=2020, tm_mon=10, tm_mday=7, 
                tm_hour=11, tm_min=44, tm_sec=49, 
                tm_wday=2, tm_yday=-1, tm_isdst=-1)


"""




import time
import board
import busio
import datetime
import adafruit_ds3231

i2c = busio.I2C(board.SCL, board.SDA)

rtc = adafruit_ds3231.DS3231(i2c)


def time_dict():
    """ Reads the DS3231 RTC time and store the time.struct_time
     object in a dictionary.
    """

    t=rtc.datetime
    time_dict={'tm_year':t.tm_year,
           'tm_mon':t.tm_mon,
           'tm_mday':t.tm_mday,
           'tm_hour':t.tm_hour,
           'tm_min':t.tm_min,
           'tm_sec':t.tm_sec,
           'tm_wday':t.tm_wday,
           'tm_yday':t.tm_yday,
           'tm_isdst':t.tm_isdst}

    return time_dict


def weekdays_shift():
    """ Shifts the weekdays by one and reset to zero
     when day of the week goes beyond six
     Monday=0, Tuesday=1 ... Saturday=5, Sunday=6"""

    t=time_dict()
    t['tm_wday']+=1
    if t['tm_wday']>6:
        t['tm_wday']=0
    return t['tm_wday']


def year_shift():
    """ Adds one to the tm_year element if
    it is 31st December and the alarm needs to be set
    for the following day which will be a new year"""

    t=time_dict()
    t['tm_year']+=1
    return t

def months_shift():
    """ Adds 1 to the tm_month element when
    it is the end of a month and the alarm needs to be set
    for the following day which will be a new month"""

    t=time_dict()
    t['tm_mon']+=1
    if t['tm_mon']>12:
        t=year_shift()
        t['tm_mon']=1
    return t

def next_day():
    """ Sets the alarm at 5.00 am the following day"""

    t=time_dict()
    days = {1:31, 2:28, 3:31, 4:30, 5:31, 6:30, 7:31, 8:31, 9:30, 10:31, 11:30, 12:31}
    t['tm_mday']+=1
    t['tm_wday']=weekdays_shift()
    if t['tm_mday']<=days[t['tm_mon']]:
        t=(t['tm_year'],t['tm_mon'],t['tm_mday'],5,0,0,t['tm_wday'],-1,-1)
    elif t['tm_mday']>days[t['tm_mon']]:
        t=months_shift()
        t['tm_wday']=weekdays_shift()
        t['tm_mday']=1
        t=(t['tm_year'],t['tm_mon'],t['tm_mday'],5,0,0,t['tm_wday'],-1,-1)
    return t

def alarm():
    """ Set the alarm at 5.00 am the following day."""

    t=next_day()
    rtc.alarm1 = (time.struct_time(t), "daily")
    if rtc.alarm1_status:
        #print("wake up!")
        rtc.alarm1_status = False



