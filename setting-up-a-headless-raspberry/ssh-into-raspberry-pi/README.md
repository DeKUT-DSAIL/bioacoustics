# SSH Into Raspberry Pi
The steps outlined here are a guide to accessing the terminal of a headless Raspberry Pi (without a monitor, keyboard, and mouse) using SSH. For this exercise to be successful, ensure you install the operating system on a microSD card using the procedure outlined [here](https://github.com/DeKUT-DSAIL/bioacoustics/tree/master/setting-up-a-headless-raspberry/headless-raspberry-pi-access). 

## Requirements
1. Raspberry Pi zero/2/3/4/5—for Raspberry Pi 2, a Wi-Fi dongle is required to connect to a wireless network.
2. Raspberry Pi power supply.
3. MicroSD card—with Raspberry Pi OS installed using the steps outlined [here](https://github.com/DeKUT-DSAIL/bioacoustics/tree/master/setting-up-a-headless-raspberry/headless-raspberry-pi-access).
4. A computer with internet access.
5. Wireless network or ethernet cable—the Raspberry Pi Zero does not have an ethernet port so a wireless network will be needed. When using a wireless network to SSH into a headless Raspberry Pi, ensure the SSID and password of the network are keyed in their respective places during the OS customisation step in the installation guide mentioned above. 

## Steps for Installing Raspberry Pi OS
Follow the following steps to install the Raspberry Pi OS on a microSD card.

### Step 1: Mount the microSD card
Mount the microSD card on a computer that has internet access.

### Step 2: Install Raspberry Pi Imager
Raspberry Pi Imager is a tool for installing Raspberry Pi OS and other operating systems on a microSD card. Download and install the Raspberry Pi Imager (here)[https://www.raspberrypi.com/software/]. Once you’ve installed Imager, launch the application by clicking the Raspberry Pi Imager icon or running rpi-imager on the terminal.

<p align="center">
  <img width="auto" height="auto" src="/setting-up-a-headless-raspberry/ssh-into-raspberry-pi/img/putty-raspi-local.png">
  
</p>

<p align="center"> 
  <em>Figure 1: Homepage of the Raspberry Pi Imager.</em>
</p>











```cpp
@reboot /home/pi/bioacoustics/audio.sh
```

The system is now ready for data collection.
