import csv
from rtc import *
import digitalio
import adafruit_mcp3xxx.mcp3008 as MCP
from adafruit_mcp3xxx.analog_in import AnalogIn


spi = busio.SPI(clock=board.SCK, MISO=board.MISO, MOSI=board.MOSI)
cs = digitalio.DigitalInOut(board.D5)

mcp = MCP.MCP3008(spi, cs)

# Reads the analog input at pin 0 of the MCP3008 and returns the corresponding voltage
def volt():
    channel = AnalogIn(mcp, MCP.P0)
    voltage=round(channel.voltage*2,1)
    return voltage

#This function saves the time and voltage readings in a CSV file format
#The file is saved with that specific day's date as the name
def voltage_csv():
    t=rtc.datetime
    name_by_date =str(t.tm_year)+'-'+str(t.tm_mon)+'-'+str(t.tm_mday)
    name_by_date='/home/pi/VoltageData/'+name_by_date+'.csv'
    l1=[]
    t=rtc.datetime
    voltage=volt()
    current_time =str(t.tm_hour)+'.'+str(t.tm_min)+'.'+str(t.tm_sec)
    l1.extend((current_time,voltage))
    with open(name_by_date,mode='a') as file:
        create=csv.writer(file)
        create.writerow(l1)
