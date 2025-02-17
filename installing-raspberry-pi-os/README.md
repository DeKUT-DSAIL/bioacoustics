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
  <img width="auto" height="auto" src="/installing-raspberry-pi-os/img/rpi-imager-homepage.png">
  
</p>

<p align="center"> 
  <em>Figure 1: Homepage of the Raspberry Pi Imager.</em>
</p>

### Step 3: Choose device
Click the `CHOOSE DEVICE` button to select the Raspberry Pi version you have. The Raspberry Pi versions will be displayed as shown in Figure 2.    

<p align="center">
  <img width="auto" height="auto" src="/installing-raspberry-pi-os/img/rpi-imager-choose-device.png">
  
</p>

<p align="center"> 
  <em>Figure 2: List of Raspberry Pi versions.</em>
</p>

Choose the device for which you are preparing the microSD card. Let us choose Raspberry Pi 3 for this tutorial. After selecting the Raspberry Pi version, the Raspberry Pi Imager will return to the home page and display the selected device as shown in Figure 3.

<p align="center">
  <img width="auto" height="auto" src="/installing-raspberry-pi-os/img/rpi-imager-rpi3-choice.png">
  
</p>

<p align="center"> 
  <em>Figure 3: Raspberry Pi Imager homepage showing Raspberry Pi 3 as the selected device.</em>
</p>

### Step 4: Choose the operating system
The Raspberry Pi supports numerous operating systems. It features various editions of Raspberry Pi OS, including 64-bit and 32-bit, as well as Lite, Full, and versions with recommended software. Additionally, operating systems like Ubuntu, Alpine Linux, and RISC OS Pi are accessible through the Raspberry Pi Imager. Your choice of operating system should consider factors like the processing power of your Raspberry Pi model, its intended use, and compatibility with the software. 

To choose the operating system, click the `CHOOSE OS` button. Figure 4 shows the variety of operating systems that the Raspberry Pi can run on.

<p align="center">
  <img width="auto" height="auto" src="/installing-raspberry-pi-os/img/rpi-imager-choose-os.png">
  
</p>

<p align="center"> 
  <em>Figure 4: List of operating systems available on the Raspberry Pi imager platform.</em>
</p>

Click the OS edition you intend to install for your Raspberry Pi. Let us choose Raspberry Pi OS (32-bit) for this tutorial. After selecting the Raspberry Pi OS, the Raspberry Pi Imager will return to the home page and display the selected OS as shown in Figure 5.

<p align="center">
  <img width="auto" height="auto" src="/installing-raspberry-pi-os/img/rpi-imager-32-bit-os.png">
  
</p>

<p align="center"> 
  <em>Figure 5: Raspberry Pi Imager homepage showing RASPBERRY PI 0S (32-BIT) as the selected operating system.</em>
</p>


### Step 5: Choosing storage
The next step is to select the microSD to write the Raspberry Pi OS. Click the `CHOOSE STORAGE` button, and a list of devices plugged into the computer will appear, as shown in Figure 6.

<p align="center">
  <img width="auto" height="auto" src="/installing-raspberry-pi-os/img/rpi-imager-storage-list.png">
  
</p>

<p align="center"> 
  <em>Figure 6: Storage device plugged into the computer.</em>
</p>

If multiple storage devices are plugged into the computer, please make sure the right storage device is selected. Figure 7 shows the Raspberry Pi Imager after selecting the storage.

<p align="center">
  <img width="auto" height="auto" src="/installing-raspberry-pi-os/img/rpi-imager-selected-storage.png">
  
</p>

<p align="center"> 
  <em>Figure 7: Raspberry Pi Imager homepage showing the selected storage for OS installation.</em>
</p>

### Step 6: OS customisation
Click the `NEXT` button and a pop-up will appear as shown in Figure 8. 

<p align="center">
  <img width="auto" height="auto" src="/installing-raspberry-pi-os/img/rpi-imager-editing-option.png">
  
</p>

<p align="center"> 
  <em>Figure 8: OS customisation settings pop-up.</em>
</p>

Click `EDIT SETTINGS` to customise the operating system. Check the options and populate the general settings as shown in Figure 9.

<p align="center">
  <img width="auto" height="auto" src="/installing-raspberry-pi-os/img/rpi-imager-general-settings.png">
  
</p>

<p align="center"> 
  <em>Figure 9: General OS customisation settings.</em>
</p>

Customise the settings, such as `username, password, and SSID`, for your use case. Then, click on the `SERVICES` tab to customise the OS further, as shown in Figure 10. 

<p align="center">
  <img width="auto" height="auto" src="/installing-raspberry-pi-os/img/rpi-imager-services-settings.png">
  
</p>

<p align="center"> 
  <em>Figure 10: Enabling SSH.</em>
</p>

*NOTE: Enabling SSH is important for headless access to the Raspberry Pi.*

Click `SAVE` and a pop-up will prompt you to apply customisation settings as shown in Figure 11.

<p align="center">
  <img width="auto" height="auto" src="/installing-raspberry-pi-os/img/rpi-imager-services-settings.png">
  
</p>

<p align="center"> 
  <em>Figure 11: A pop-up prompting the user to apply the OS customisation settings.</em>
</p>

Click `YES` and you will be prompted to confirm if you are sure you want to continue as shown in Figure 12.

<p align="center">
  <img width="auto" height="auto" src="/installing-raspberry-pi-os/img/rpi-imager-write.png">
  
</p>

<p align="center"> 
  <em>Figure 12: A pop-up prompting the user to confirm OS installation.</em>
</p>

Click `YES` and the OS installation will start as shown in Figure 13.

<p align="center">
  <img width="auto" height="auto" src="/installing-raspberry-pi-os/img/rpi-imager-write.png">
  
</p>

<p align="center"> 
  <em>Figure 13: OS installation in progress.</em>
</p>

Once the writing process is done, the user will be notified as shown in Figure 14.

<p align="center">
  <img width="auto" height="auto" src="/installing-raspberry-pi-os/img/rpi-imager-os-installation-complete.png">
  
</p>

<p align="center"> 
  <em>Figure 14: OS installation completed notification.</em>
</p>

Click `CONTINUE`. The microSD card is ready for use with the Raspberry Pi.











```cpp
@reboot /home/pi/bioacoustics/audio.sh
```

The system is now ready for data collection.
