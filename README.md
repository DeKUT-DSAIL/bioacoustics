# DSAIL Bioacoustics System
This repository contains the code used to run the DSAIL Bioacoustics System. The system is based on the Raspberry Pi 3 single board computer and is used to collect acoustic data of birds.

## System Development
The DSAIL Bioacoustics System can be divided into hardware and software. Both the hardware and the software were developed to enable the Raspberry Pi to record audio data of birds while performing optimumly. More about the hardware can be found [here](https://dekut-dsail.github.io/assets/documents/technical-reports/bioacoustics/Kiarie-DSAIL-2020-001.pdf). In the following sections, we will look at the codes used to run the system. A python environment is created and some libraries are installed to enable the programs to run. This is done by first updating the Raspbian of the Raspberry Pi by running the [Raspbian update bash file](https://github.com/DeKUT-DSAIL/bioacoustics/blob/master/raspi-update-bash) and then running the [environment setup bash file](https://github.com/DeKUT-DSAIL/bioacoustics/blob/master/env-setup-bash) that installs all the required libraries for this project.

### 1. Power management program
The [power management program](https://github.com/DeKUT-DSAIL/bioacoustics/blob/master/power-management.py) enables the Raspberry Pi to monitor the state of charge (SOC) of the battery used in the system. This is to ensure that the Raspberry Pi does not shut down due to depletion of charge in the battery since this may lead to corruption of data in the storage. Also, this should protect the battery from being over discharged hence lengthen its lifespan. The programs enables the Raspberry Pi to make an informed decision of shutting down when the battery reaches the cut off voltage. Also, due to power constraint, our system is designed to work for a given number of hours in a day. The program is responsible for shutting down the system when the time matches the specified shutdown time.

The program is written in Python and uses both standard python libraries and third party libraries from [Adafruit](https://www.adafruit.com/) which are **board**, **busio**, and **digitalio**. The program reads the battery voltage after every 30 seconds and compares it with the predetermined cut off voltage. Whenever the voltage goes below the specified cut off voltage, the program initiates the shutdown of the Raspberry Pi and the entire system. The program uses our own made modules to achieve this. The modules are [rtc.py](https://github.com/DeKUT-DSAIL/bioacoustics/blob/master/rtc.py) and [adc.py](https://github.com/DeKUT-DSAIL/bioacoustics/blob/master/adc.py) that we will look into in the following two sections.

### 2. Rtc.py module
The [rtc.py module](https://github.com/DeKUT-DSAIL/bioacoustics/blob/master/rtc.py) is used by the power management program to set the alarm of a [DS3231 Real Time Clock (RTC) board](https://learn.adafruit.com/adafruit-ds3231-precision-rtc-breakout/overview) to schedule the wake up of the system. The program is written in Python and uses standard Python libraries and third party libraries from [Adafruit](https://www.adafruit.com/) that were written to help in controlling the RTC in boards that use Python like the Raspberry Pi. These libraries are **board**, **busio**, and **adafruit_ds3231**. The alarm function of the rtc.py module is called to set the RTC's alarm to schedule wake up of the system whenever the Raspberry Pi has "decided" to shut down.

### 3. Adc.py module
The [adc.py module](https://github.com/DeKUT-DSAIL/bioacoustics/blob/master/adc.py) is used by the power management program to read the voltage of the battery used in the system. The Raspberry Pi lacks an onboard analog to digital converter (ADC) and hence has to use an external ADC to read the battery voltage which is an analog quantity. In our system, we used the [MCP3008 i/p ADC](https://learn.adafruit.com/raspberry-pi-analog-to-digital-converters/mcp3008) to enable our system to read the battery voltage. The program is written in Python and uses both standard python libraries and third party libraries from [Adafruit](https://www.adafruit.com/) which are **board**, **busio**, **digitalio**, **adafruit_mcp3xxx.mcp3008** and **adafruit_mcp3xxx.analog_in** that enables us to control the ADC using the Raspberry Pi. The power management program calls the volt function from this module after every thirty seconds to read the battery voltage. After every five minutes, the voltage reading at that moment is saved in a datestamped CSV file alongside with the time at that moment using the volt_csv function from this module.

### Audio data collection program
The [audio data collection program](https://github.com/DeKUT-DSAIL/bioacoustics/blob/master/audio_data_collection.py) is used to record audio data of birds. The program is written in Python and uses both standard python libraries and third party libraries like [*numpy*](https://numpy.org/), [*soundfile*](https://pypi.org/project/SoundFile/) and [*sounddevice*](https://www.sounddevices.com/). The program records continously but saves sections of the stream that countain acoustic activties. This is done by comparing energy of audio blocks with a preset still condition. The program saves 10 seconds long timestamped audio files in its storage or an external storage.

### 5. Time set program
The [time set program](https://github.com/DeKUT-DSAIL/bioacoustics/blob/master/time-set.py) program is  used to set time of the Raspberry Pi every time on wake up since the Raspberry Pi lacks an onboard RTC.
