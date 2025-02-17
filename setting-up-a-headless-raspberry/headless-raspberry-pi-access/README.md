# Installing Raspberry Pi OS
**NOTE: THESE INSTRUCTIONS WERE PREPARED IN FEBRUARY 2025. THE MATERIALS CONTAINED HERE COULD BE OUT OF DATE. CHECK ON THE OFFICIAL RASPBERRY PI WEBSITE FOR UPDATED INSTALLATION INSTRUCTIONS IF THE ONES OUTLINED HERE DON'T WORK** 

## Requirements
1. Raspberry Pi zero/2/3/4/5
2. MicroSD card- at least 8 GB
3. MicroSD card reader
4. A computer with internet access

## Steps for Installing Raspberry Pi OS
Follow the following steps to install the Raspberry Pi OS on a microSD card.

### Step 1: Mount the microSD card
Mount the microSD card on a computer that has internet access.

### Step 2: Install Raspberry Pi Imager
Raspberry Pi Imager is a tool for installing Raspberry Pi OS and other operating systems on a microSD card. Download and install the Raspberry Pi Imager (here)[https://www.raspberrypi.com/software/]. Once you’ve installed Imager, launch the application by clicking the Raspberry Pi Imager icon or running rpi-imager on the terminal.

<p align="center">
  <img width="auto" height="auto" src="/setting-up-a-headless-raspberry/headless-raspberry-pi-access/img/putty-raspi-local.png">
  
</p>

<p align="center"> 
  <em>Figure 1: Homepage of the Raspberry Pi Imager.</em>
</p>











```cpp
@reboot /home/pi/bioacoustics/audio.sh
```

The system is now ready for data collection.
