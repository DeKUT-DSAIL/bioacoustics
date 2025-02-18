# SSH Into Raspberry Pi
The steps outlined here are a guide to accessing the terminal of a headless Raspberry Pi (without a monitor, keyboard, and mouse) using SSH. For this exercise to be successful, ensure you install the operating system on a microSD card using the procedure outlined [here](https://github.com/DeKUT-DSAIL/bioacoustics/tree/master/setting-up-a-headless-raspberry/headless-raspberry-pi-access). 

## Requirements
1. Raspberry Pi zero/2/3/4/5—for Raspberry Pi 2, a Wi-Fi dongle is required to connect to a wireless network.
2. Raspberry Pi power supply.
3. MicroSD card—with Raspberry Pi OS installed using the steps outlined [here](https://github.com/DeKUT-DSAIL/bioacoustics/tree/master/setting-up-a-headless-raspberry/headless-raspberry-pi-access).
4. A computer with internet access.
5. Wireless network or ethernet cable—the Raspberry Pi Zero does not have an ethernet port so a wireless network will be needed. When using a wireless network to SSH into a headless Raspberry Pi, ensure the SSID and password of the network are keyed in their respective places during the OS customisation step in the installation guide mentioned above. 

## Steps for SSH into Raspberry Pi
Follow the following steps to SSH into the Raspberry Pi.

### Step 1: Install the necessary software
Download and install PuTTy for Windows [here](https://www.putty.org/) and VNC viewer for Windows, macOS, and Linux [here](https://www.realvnc.com/en/connect/download/viewer/) on your computer.

### Step 2: Establish a connection
Connect your computer to the wireless network specified during the OS installation process. Alternatively, you can connect your computer and the Raspberry Pi with an ethernet cable. Insert the microSD card loaded with the OS onto the Raspberry Pi and power it on. After a few minutes (about 5 minutes), check if the Raspberry Pi has connected to the wireless network or if the ethernet port is blinking to show a connection has been established. If the Raspberry Pi has connected to  the wireless network or the ethernet is blinking, we can now SSH into the Raspberry Pi.

*NOTE: If you have no way of determining whether the Raspberry Pi has connected to the wireless network, give it about 5 minutes and start executing the step that follows.*

### Step 3: SSH into Raspberry Pi
#### Method 1: Windows users—using PuTTy.
For Windows users, open PuTTy and enter the hostname set during the general OS customisation step, as shown in Figure 1.

<p align="center">
  <img width="auto" height="auto" src="/setting-up-a-headless-raspberry/ssh-into-raspberry-pi/img/putty-raspi-local.png">
  
</p>

<p align="center"> 
  <em>Figure 1: SSH into the Raspberry Pi using the hostname.</em>
</p>

*NOTE: If you can obtain the IP address assigned to the Raspberry Pi by the wireless network you can use it in the place of the hostname.* 

Next, click `Open` and the window shown in Figure 2 will appear.

<p align="center">
  <img width="auto" height="auto" src="/setting-up-a-headless-raspberry/ssh-into-raspberry-pi/img/putty-potential-security-breach.png">
  
</p>

<p align="center"> 
  <em>Figure 2: PuTTy security alert.</em>
</p>

Click `Accept` and a console will appear as shown in Figure 3.

<p align="center">
  <img width="auto" height="auto" src="/setting-up-a-headless-raspberry/ssh-into-raspberry-pi/img/putty-login-as.png">
  
</p>

<p align="center"> 
  <em>Figure 3: PuTTy security alert.</em>
</p>

#### Method 2: Windows, Linux, and macOS users—using CMD or terminal
Open CMD or terminal and enter either `ssh username@hostname.local` or `ssh username@IP address`. Replace `username` and `hostname` or `IP address` with the details of your Raspberry Pi. Let us use Window's command prompt (CMD) to show how we can SSH into the Raspberry. The same steps will be used in Linux or macOS terminal. In CMD, enter the details as shown in Figure 6.

<p align="center">
  <img width="auto" height="auto" src="/setting-up-a-headless-raspberry/ssh-into-raspberry-pi/img/cmd-ssh-access.png">
  
</p>

<p align="center"> 
  <em>Figure 6: Entering Raspberry Pi details on CMD.</em>
</p>

Press ENTER and you will be prompted as shown in Figure 7.

<p align="center">
  <img width="auto" height="auto" src="/setting-up-a-headless-raspberry/ssh-into-raspberry-pi/img/cmd-ssh-access.png">
  
</p>

<p align="center"> 
  <em>Figure 7: Security alert.</em>
</p>

Enter `yes` and press ENTER and you will be prompted to enter the password as shown in Figure 8.

<p align="center">
  <img width="auto" height="auto" src="/setting-up-a-headless-raspberry/ssh-into-raspberry-pi/img/cmd-ssh-password.png">
  
</p>

<p align="center"> 
  <em>Figure 6: Entering Raspberry Pi details on CMD.</em>
</p>

Once the process is successful, you will get a console similar to Figure 7.

<p align="center">
  <img width="auto" height="auto" src="/setting-up-a-headless-raspberry/ssh-into-raspberry-pi/img/cmd-ssh-successful.png">
  
</p>

<p align="center"> 
  <em>Figure 7: Raspberry Pi terminal.</em>
</p>








```cpp
@reboot /home/pi/bioacoustics/audio.sh
```

The system is now ready for data collection.
