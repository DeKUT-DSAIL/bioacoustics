import os
import csv
import board
import busio
import digitalio
from rtc import time_dict
import adafruit_mcp3xxx.mcp3008 as MCP
from adafruit_mcp3xxx.analog_in import AnalogIn


spi = busio.SPI(clock=board.SCK, MISO=board.MISO, MOSI=board.MOSI)
cs = digitalio.DigitalInOut(board.D5)

mcp = MCP.MCP3008(spi, cs)


def volt():
    """ Reads the analog input at pin 0 of the MCP3008 and
    returns the voltage reading"""

    channel = AnalogIn(mcp, MCP.P0)
    voltage = round(channel.voltage * 2, 2)
    return voltage


def voltage_csv(path, folder_path, file_name_by_date):
    """ This function saves the time and voltage readings in a CSV file format
    The file is saved with that specific day's date as the name."""

    l = []
    t = time_dict()
    voltage = volt()
    current_time = str(t['tm_hour']) + '.' + str(t['tm_min']) + '.' + str(t['tm_sec'])
    l.extend((current_time, voltage))
    with open(file_name_by_date, mode = 'a') as file:
        create = csv.writer(file)
        create.writerow(l)
