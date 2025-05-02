#!/bin/bash

cd bioacoustics

source bioacoustics-env/bin/activate

python data_collection.py --recording_samplerate 44100 --resampling_rate 16000 --resampling True --deviceID 2 
