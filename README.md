# Acoustic Monitoring of Ecosystems

Acoustic monitoring of ecosystems is an efficient and non-invasive method that allows us to collect data continuously and remotely in the ecosystems. Using this data we can tell a lot about what is happening in our parks, reserves and conservancies. Birds vocalize a lot and also respond quickly to environmental changes making them to be ideal indicator species for acoustic monitoring of the biosphere.

## Acoustic classification of birds
The idea behind the acoustic classification of birds is that birds produce characteristic calls/songs that are unique to their species. We can tell different species of birds by just listening to the sounds they produce. Acoustic data is collected by deploying acoustic sensors in the field. From the analysis of this data, we can assess the state of our ecosystems. A lot of data is collected by the acoustic sensors. Manual classification of this data may turn out to be a difficult task. However, we can automate the process by using acoustic sensors that automatically classify the recordings they capture. These sensors are loaded with machine learning models that have been trained on birds' acoustic data for classification.

## How does it work?

The sound produced by a given bird species sounds differently from sound from another species due to the difference in frequency components of these sounds. If we can extract the frequency components of a sound, we can be able to describe that sound. Sounds produced by birds of the same species will have frequency components that are unique to that species. Therefore, we can differentiate different bird species by analyzing the frequency components of the sounds they produce. A spectrogram ( a plot of frequency against time) is used to visualize the frequency components of sound.

<p align="center">
  <img width="345" height="225" src="/img/grey-backed.png">
  <img width="345" height="225" src="/img/hartlaub's-turacos-spectrogram.png">
  
</p>

<p align="center"> 
  <em>Figure 1: Spectrograms of a Grey-backed Camaroptera (left) and Hartlaub's Turacos (right)</em>
</p>

Figure 1 above shows spectrograms of a Greybacked Camaroptera and a Hartlaub's Turacos. By looking at the two spectrograms, we can see that the frequency composition of the sounds from the two birds is different. We can then treat the spectrograms as images and use them to train machine learning models for classification.

<p align="center">
  <img width="auto" height="300" src="/img/dsp-ml.png"> 
</p>

<p align="center"> 
  <em>Figure 2: A flow diagram of how acoustic classification of bird species is achieved.</em>
</p>

After training a model, we can then deploy it on an acoustic sensor for automatic acoustic classification of birds in the ecosystems.

## Acoustic Data Collection

Acoustic data is required to train machine learning models for the automatic acoustic classification of birds. At [DSAIL](https://dekut-dsail.github.io/), we have developed a Raspberry Pi-based recording system to collect acoustic data of birds ([DSAIL Bioacoustics System](https://kiariegabriel.github.io/dsail-bioacoustics-system.html)). The system is designed to continuously 'listen' while waiting for acoustic activities. Segments of streams that exhibit acoustic activities are saved as audio files in the Raspberry Pi's storage. The program `data_collection.py` enables the Raspberry Pi to make the recordings. The flow chart below shows the workings of the program.

<p align="center">
  <img width="auto" height="300" src="/img/data-collection.png"> 
</p>

<p align="center"> 
  <em>Figure 3: A flow chart of the data collection program.</em>
</p>

## Setting up the Raspberry Pi
The following steps outline how to prepare the Raspberry Pi for data collection.

### Requirements
1. Raspberry Pi 3/4
2. Raspberry Pi power supply
3. USB microphone
4. A microSD Card loaded with Raspberry Pi OS—follow the steps outlined [here](https://github.com/DeKUT-DSAIL/bioacoustics/tree/master/setting-up-a-headless-raspberry) to install Raspberry Pi OS and access its terminal.
5. Access to the internet.
6. Ability to access the Raspberry Pi's terminal.

### Step 1: Access the Raspberry Pi terminal
Power the Raspberry Pi and access its terminal. Ensure the Raspberry Pi is connected to the internet. 

### Step 2: Clone the bioacoustics repository
Let's begin by cloning this repository. Run the following command on the Raspberry Pi's terminal:

```cpp
git clone https://github.com/DeKUT-DSAIL/bioacoustics.git
```

### Step 3: Install requirements
Next, run the following commands to create a virtual environment and install the requirements:

```cpp
/home/pi/bioacoustics/bioacoustics_environment_setup.sh
```

### Step 4: Connect a USB microphone
Connect a USB microphone to the Raspberry Pi to record a sample audio. To test whether the Raspberry Pi detects the USB microphone, run the following command.

```cpp
lsusb
```
A list of connected devices will appear on the screen as shown below. 

[screenshot of pi usb devices list]

Confirm that the USB microphone is detected. For this example, >>List example<< is the USB microphone connected to the Raspberry Pi.

### Step 5: Record sample audio
Let us record a sample 5-second long audio, print the recorded array on the screen and plot it. To plot the audio, ensure you have access to the graphical user interface of the Raspberry Pi using a monitor or VNC viewer. if not, comment the `plt.plot(my_rec)` line in the `sample_rec.py` file.

### Step 6: Audio data collection
To start data collection, run the following command.

```cpp
/home/pi/bioacoustics/audio.sh
```

### Step 7: Scheduling data collection
If you intend for the program to run every time on boot, we will need to schedule it in `crontab`. Run the following command:

```cpp
crontab -e
```
If it is the first time using crontab, you will be prompted to choose an editor. Choose nano editor by entering 1. Copy and paste the following in the crontab:

```cpp
@reboot /home/pi/bioacoustics/audio.sh
```

The system is now ready for data collection.
