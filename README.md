# Acoustic Monitoring of Ecosystems

Acoustic monitoring of ecosystems is an efficient and non invasive method that allow us to collect data continuously and remotely. Birds vocalize a lot and also respond quickly to enviromental changes making them to be an ideal indicator species for acoustic monitoring of the biosphere.

## What is the idea?
The idea behind automatic acoustic classification is that birds produce characteristic calls/songs that are unique to their species. We can tell different species of birds by just listening to the sound they produce. Acoustic data is collected by deploying acoustic sensors in the field. From analysis of this data, we can assess the state of our ecosystems. A lot of data is collected by the acoustic sensors. Manual classification of this data may turn to be a difficult task. However, we can automate the process by using acoustic sensors that automatically classify the recordings they capture. These sensors are loaded with machine learning models that have been pretrained on birds acoustic data for the classification.

## How does it work?

Sound produced by a given bird species sounds differently from sound from another species due to difference in frequency components of these sounds. If we can extract the frequency components of a sound, we can be able to describe that sound and also differentiate it from another sound by comparing their frequency components. Sounds produced by birds of the same species will have frequency components that are unique to that species. We can visualize the frequency components of a sound using a spectrogram. A spectrogram is a plot of frequency against time.

<p align="center">
  <img width="230" height="150" src="/img/grey-backed.png">
  <img width="230" height="150" src="/img/hartlaub's-turacos-spectrogram.png">
  
</p>

<p align="center"> 
  <em>Figure 1: SpectrogramS of a Grey-backed Camaroptera (left) and Hartlaub's Turacos (right)</em>
</p>

Figure 1 above shows spectrograms of a Greybacked Camaroptera and Hartlaub's Turacos. By looking at the two spectrograms, we can see that the spectrum of the sounds from the two birds are different. We can then treat the spectrograms as images and feed them to a machine learning model for classification. Therefore, by computing spectrograms of different bird species' sounds we can train a machine learning model that will be used for acoustic classification of birds. 

<p align="center">
  <img width="auto" height="300" src="/img/dsp-ml.png"> 
</p>

<p align="center"> 
  <em>Figure 2: A flow diagram of how acoustic classification of bird species is acheived.</em>
</p>

After training a model, we can then deploy it on an acoustic sensor (a Raspberry Pi based acoustic sensor will be used for our case) for automatic acoustic classification of birds in the ecosystems.

## Acoustic Data Collection

Acoustic data is required to train machine learning models for automatic acoustic classification of birds. At [DSAIL](https://dekut-dsail.github.io/), we have developed a Raspberry Pi based recording system to collect acoustic data of birds ([DSAIL Bioacoustics System](https://kiariegabriel.github.io/dsail-bioacoustics-system.html)). The system is designed to continuously 'listen' waiting for acoustic activities. Segments of stream that exhibit acoustic activities are saved as audio files in the Raspberry Pi's storage. The program `data_collection.py` enables the Raspberry Pi to make the recordings. The flow chart below shows the working of the program.

<p align="center">
  <img width="auto" height="300" src="/img/data-collection.png"> 
</p>

<p align="center"> 
  <em>Figure 3: A flow chart of the data collection program.</em>
</p>
