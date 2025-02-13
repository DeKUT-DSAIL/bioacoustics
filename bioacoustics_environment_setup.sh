#!/bin/bash


sudo apt -y update
sudo apt -y full-upgrade

sudo apt-get install -y portaudio19-dev


python3 -m venv bioacoustics-env
source bioacoustics-env/bin/activate


pip install --upgrade pip
pip install wheel
pip install cython
pip install gpiozero
pip install lgpio
pip install numpy
pip install scipy
pip install pandas
pip install soundfile
pip install scikit-learn
pip install matplotlib
pip install sounddevice
pip install PyAudio
pip install llvmlite
pip install numba
pip install scipy
pip install librosa
pip install ipython
