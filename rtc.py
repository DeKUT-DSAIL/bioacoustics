import time
import board
import busio
import datetime
import adafruit_ds3231


i2c = busio.I2C(board.SCL, board.SDA)

rtc = adafruit_ds3231.DS3231(i2c)



def time_list():
    """ Reads the DS3231 RTC time and converts the 
    resulting tuple into a list
    """

    t=rtc.datetime
    t=list(t)
    return t


def weekdays_shift():
    """ Shifts the weekdays by one and reset to zero
     when day of the week goes beyond six
     Monday=0, Tuesday=1 ... Saturday=5, Sunday=6"""

    t=time_list()
    t[6]+=1
    if t[6]>6:
        t[6]=0
    return t[6]


def year_shift():
    """ Adds one to the tm_year element if 
    it is 31st December and the alarm needs to be set 
    for the following day which will be a new year"""

    t=time_list()
    t[0]+=1
    return t


def months_shift():
    """ Adds 1 to the tm_month element when the number
    it is the end of a month and the alarm needs to be set 
    for the following day which will a new month"""

    t=time_list()
    t[1]+=1
    if t[1]>12:
        t=year_shift()
        t[1]=1
    return t


def next_day():
    """ Sets the alarm at 9.00 am the following day"""

    t=time_list()
    days = {1:31, 2:28, 3:31, 4:30, 5:31, 6:30, 7:31, 8:31, 9:30, 10:31, 11:30, 12:31}
    t[2]+=1
    t[6]=weekdays_shift()
    if t[2]<=days[t[1]]:
        t=(t[0],t[1],t[2],9,0,0,t[6],-1,-1)
    elif t[2]>days[t[1]]:
        t=months_shift()
        t[6]=weekdays_shift()
        t[2]=1
        t=(t[0],t[1],t[2],9,0,0,t[6],-1,-1)
    return t


def alarm_time1():
    """ Set the RTC alarm an hour from the present time."""

    t=time_list()
    t[3]=t[3]+1
    t=tuple(t)
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

    t=time_list()
    t[3]=9
    t[4]=0
    t[5]=0
    t=tuple(t)
    rtc.alarm1 = (time.struct_time(t), "daily")
    if rtc.alarm1_status:
        #print("wake up!")
        rtc.alarm1_status = False

def alarm():
    """ Conditions to determine whether the alarm will 
    be set for today or the next day depending on the 
    current time."""

    t=time_list()
    t[3]=t[3]+1
    if t[3]>=8 and t[3]<17:
        alarm_time1()
    elif t[3]==17 and t[4]<30:
        alarm_time1()
    elif t[3]==17 and t[4]>=30:
        alarm_time2()
    elif t[3]>=18 and t[3]<24:
        alarm_time2()
    elif t[3]==24 and t[4]<58:
        alarm_time2()
    elif t[3]==24 and t[4]>=58:
        time.sleep(125)
        alarm_time3()
    elif t[3]>=0 and t[3]<=8:
        alarm_time3()
