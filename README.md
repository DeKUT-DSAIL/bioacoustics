# DSAIL Bioacoustics System
This repository contains the code used to run the DSAIL Bioacoustics System. The system is based on the Raspberry Pi 3 single board computer and is used to collect acoustic data of birds.

## System Development
The DSAIL Bioacoustics System can be divided into hardware and software. Both the hardware and the software were developed to enable the Raspberry Pi to record audio data while performing optimally. More about the hardware can be found [here](https://dekut-dsail.github.io/assets/documents/technical-reports/bioacoustics/Kiarie-DSAIL-2020-001.pdf). In the following sections, we will look at the codes used to run the system.

### 1. Power management program
The [power management program](https://github.com/DeKUT-DSAIL/bioacoustics/blob/master/power-management.py) enables the Raspberry Pi to monitor the state of charge of the battery used in the system. This is to ensure that the Raspberry Pi does not shut down due to depletion of charge in the battery since this may lead to corruption of data in the storage. Also, this should protect the battery from being over discharged hence lengthen its lifespan. 
