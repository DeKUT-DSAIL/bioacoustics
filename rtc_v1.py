"""
First rtc module version
"""

import time
import board
import busio
import datetime
import adafruit_ds3231


i2c = busio.I2C(board.SCL, board.SDA)

rtc = adafruit_ds3231.DS3231(i2c)



def time_dict():
    """ Reads the DS3231 RTC time and converts the 
    resulting tuple into a list
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
    """ Adds 1 to the tm_month element when the number
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


def alarm_time1():
    """ Set the RTC alarm an hour from the present time."""

    t=time_dict()
    t['tm_hour']=t['tm_hour']+1
    t=(t['tm_year'],t['tm_mon'],t['tm_mday'],t['tm_hour'],t['tm_min'],t['tm_sec'],t['tm_mday'],-1,-1)
    rtc.alarm1 = (time.struct_time(t), "daily")
    if rtc.alarm1_status:
        #print("wake up!")
        rtc.alarm1_status = False




def alarm_time2():
    """ Set the alarm at 9.00 am the following day."""

    t=next_day()
    rtc.alarm1 = (time.struct_time(t), "daily")
    if rtc.alarm1_status:
        #print("wake up!")
        rtc.alarm1_status = False

def alarm_time3():
    """ Set the RTC alarm at 9 if the alarm function
    was called past midnight."""

    t=time_dict()
    t['tm_hour']=9
    t['tm_min']=0
    t['tm_sec']=0
    t=(t['tm_year'],t['tm_mon'],t['tm_mday'],t['tm_hour'],t['tm_min'],t['tm_sec'],t['tm_mday'],-1,-1)

    rtc.alarm1 = (time.struct_time(t), "daily")
    if rtc.alarm1_status:
        #print("wake up!")
        rtc.alarm1_status = False

def alarm():


    """ Conditions to determine whether the alarm will
    be set for today or the next day depending on the
    current time."""

    t=time_dict()
    t['tm_hour']=t['tm_hour']+1
    if t['tm_hour']>=8 and t['tm_hour']<17:
        alarm_time1()
    elif t['tm_hour']==17 and t['tm_min']<30:
        alarm_time1()
    elif t['tm_hour']==17 and t['tm_min']>=30:
        alarm_time2()
    elif t['tm_hour']>=18 and t['tm_hour']<24:
        alarm_time2()
    elif t['tm_hour']==24 and t['tm_min']<58:
        alarm_time2()
    elif t['tm_hour']==24 and t['tm_min']>=58:
        time.sleep(125)
        alarm_time3()
    elif t['tm_hour']>=0 and t['tm_hour']<=8:
        alarm_time3()


