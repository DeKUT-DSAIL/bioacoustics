# Accessing the Raspberry Pi using SSHSSH
The steps outlined here are a guide to accessing the terminal of a headless Raspberry Pi (without a monitor, keyboard, and mouse) using SSH. For this exercise to be successful, ensure you install the operating system on a microSD card using the procedure outlined [here](https://github.com/DeKUT-DSAIL/bioacoustics/tree/master/setting-up-a-headless-raspberry/headless-raspberry-pi-access). 

## Requirements
1. Raspberry Pi zero/2/3/4/5—for Raspberry Pi 2, a Wi-Fi dongle is required to connect to a wireless network.
2. Raspberry Pi power supply.
3. MicroSD card—with Raspberry Pi OS installed using the steps outlined [here](https://github.com/DeKUT-DSAIL/bioacoustics/tree/master/setting-up-a-headless-raspberry/headless-raspberry-pi-access).
4. A computer with internet access.
5. Wireless network or ethernet cable—the Raspberry Pi Zero does not have an ethernet port so a wireless network will be needed. When using a wireless network to SSH into a headless Raspberry Pi, ensure the SSID and password of the network are keyed in their respective places during the OS customisation step in the installation guide mentioned above. 

## Steps for connecting to the Raspberry Pi via SSH
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

Enter the Raspberry Pi username set during OS installation as shown in Figure 4.

<p align="center">
  <img width="auto" height="auto" src="/setting-up-a-headless-raspberry/ssh-into-raspberry-pi/img/putty-login-as-pi.png">
  
</p>

<p align="center"> 
  <em>Figure 4: Entering the username.</em>
</p>

Press ENTER and you will be prompted to enter the password as shown in Figure 5—the password will not appear on the screen as you type.

<p align="center">
  <img width="auto" height="auto" src="/setting-up-a-headless-raspberry/ssh-into-raspberry-pi/img/putty-login-password.png">
  
</p>

<p align="center"> 
  <em>Figure 5: Entering the password.</em>
</p>

Press ENTER after entering the password and you will get a console similar to the one in Figure 6 once the process is successful.

<p align="center">
  <img width="auto" height="auto" src="/setting-up-a-headless-raspberry/ssh-into-raspberry-pi/img/putty-first-log-in.png">
  
</p>

<p align="center"> 
  <em>Figure 6: Raspberry Pi terminal.</em>
</p>


#### Method 2: Windows, Linux, and macOS users—using CMD or terminal
Open CMD or terminal and enter either `ssh username@hostname.local` or `ssh username@IP address`. Replace `username` and `hostname` or `IP address` with the details of your Raspberry Pi. Let us use Window's command prompt (CMD) to show how we can SSH into the Raspberry. The same steps will be used in Linux or macOS terminal. In CMD, enter the details as shown in Figure 7.

<p align="center">
  <img width="auto" height="auto" src="/setting-up-a-headless-raspberry/ssh-into-raspberry-pi/img/cmd-ssh-access.png">
  
</p>

<p align="center"> 
  <em>Figure 7: Entering Raspberry Pi details on CMD.</em>
</p>

Press ENTER and you will be prompted as shown in Figure 8.

<p align="center">
  <img width="auto" height="auto" src="/setting-up-a-headless-raspberry/ssh-into-raspberry-pi/img/cmd-ssh-security-alert.png">
  
</p>

<p align="center"> 
  <em>Figure 8: Security alert.</em>
</p>

Enter `yes` and press ENTER and you will be prompted to enter the password as shown in Figure 9.

<p align="center">
  <img width="auto" height="auto" src="/setting-up-a-headless-raspberry/ssh-into-raspberry-pi/img/cmd-ssh-password.png">
  
</p>

<p align="center"> 
  <em>Figure 9: Entering Raspberry Pi details on CMD.</em>
</p>

Once the process is successful, you will get a console similar to Figure 10.

<p align="center">
  <img width="auto" height="auto" src="/setting-up-a-headless-raspberry/ssh-into-raspberry-pi/img/cmd-ssh-successful.png">
  
</p>

<p align="center"> 
  <em>Figure 10: Raspberry Pi terminal.</em>
</p>

### Step 4: Configuring the Raspberry Pi
Let us configure the interfaces of the Raspberry Pi. The interfaces are essential for connecting the Raspberry Pi with peripherals. Run the following commands on the Raspberry Pi terminal.

```cpp
clear
```
```cpp
sudo raspi-config
```
The last command opens the Raspberry Pi software configuration tool as shown in Figure 11.

<p align="center">
  <img width="auto" height="auto" src="/setting-up-a-headless-raspberry/ssh-into-raspberry-pi/img/putty-sudo-raspi-config.png">
  
</p>

<p align="center"> 
  <em>Figure 11: Raspberry Pi software configuration tool.</em>
</p>

Use the navigation keys to navigate through the tool. Scroll to `Interface Options` and press ENTER. A list of interfaces will be presented as shown in Figure 12.

<p align="center">
  <img width="auto" height="auto" src="/setting-up-a-headless-raspberry/ssh-into-raspberry-pi/img/putty-interface.png">
  
</p>

<p align="center"> 
  <em>Figure 12: A list of Raspberry Pi interface options.</em>
</p>

Enable every interface by scrolling through each of them and pressing ENTER. Figures 13 and 14 show the process of enabling VNC server. 

<p align="center">
  <img width="auto" height="auto" src="/setting-up-a-headless-raspberry/ssh-into-raspberry-pi/img/putty-sudo-raspi-config.png">
  
</p>

<p align="center"> 
  <em>Figure 13: Prompt to enable VNC server.</em>
</p>


<p align="center">
  <img width="auto" height="auto" src="/setting-up-a-headless-raspberry/ssh-into-raspberry-pi/img/putty-sudo-raspi-config.png">
  
</p>

<p align="center"> 
  <em>Figure 14: VNC server enabled.</em>
</p>

Press ESC to exit the configuration tool after completing the configuration.

### Step 5: Obtain the IP address of the Raspberry Pi
You can obtain the IP address of the Raspberry Pi by running the following command on its terminal.

```cpp
hostname -I
```

### Step 6: Accessing the Raspberry Pi GUI
We will use VNC viewer to access the GUI of the Raspberry Pi. For this step to be successful, ensure the VNC server is enabled as shown in Figure 14 and you have the IP address of the Raspberry Pi. Open the VNC viewer and enter the IP address as shown in Figure 15.

<p align="center">
  <img width="auto" height="auto" src="/setting-up-a-headless-raspberry/ssh-into-raspberry-pi/img/vnc-viewer-ip-address.png">
  
</p>

<p align="center"> 
  <em>Figure 15: Entering Raspberry Pi IP address on VNC viewer.</em>
</p>

Press ENTER and an identity check pop-up will appear as shown in Figure 16.

<p align="center">
  <img width="auto" height="auto" src="/setting-up-a-headless-raspberry/ssh-into-raspberry-pi/img/vnc-viewer-ip-address-popup.png">
  
</p>

<p align="center"> 
  <em>Figure 16: VNC viewer identity check pop-up.</em>
</p>

Click `Continue` and an authentication pop-up will appear as shown in Figure 17.

<p align="center">
  <img width="auto" height="auto" src="/setting-up-a-headless-raspberry/ssh-into-raspberry-pi/img/vnc-viewer-password.png">
  
</p>

<p align="center"> 
  <em>Figure 16: VNC viewer authentication pop-up.</em>
</p>

Enter the username and password and click ok. The GUI of the Raspberry Pi will appear as shown in Figure 17.

<p align="center">
  <img width="auto" height="auto" src="/setting-up-a-headless-raspberry/ssh-into-raspberry-pi/img/vnc-viewer-gui.png">
  
</p>

<p align="center"> 
  <em>Figure 16: Raspberry Pi GUI.</em>
</p>
