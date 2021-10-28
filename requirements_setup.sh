#!/bin/bash


sudo apt install -y software-properties-common
sudo add-apt-repository -y ppa:deadsnakes/ppa
sudo apt-get -y update
sudo apt-get -y upgrade
sudo apt-get install -y python3.7 python3.7-dev python3.7-venv

sudo apt-get install -y llvm-8
sudo ln -s /usr/bin/llvm-config-8 /usr/local/bin/llvm-config
export LLVM_CONFIG=/usr/local/bin/llvm-config

sudo apt-get install -y libasound-dev portaudio19-dev libportaudio2 libportaudiocpp0
sudo apt-get install -y libatlas-base-dev
sudo apt-get install -y libtiff5-dev libjpeg8-dev libopenjp2-7-dev zlib1g-dev
sudo apt-get install -y libfreetype6-dev liblcms2-dev libwebp-dev tcl8.6-dev tk8.6-dev python3-tk
sudo apt-get install -y libharfbuzz-dev libfribidi-dev libxcb1-dev
sudo apt-get install -y gcc gfortran libopenblas-dev liblapack-dev
sudo apt-get install -y nano
sudo apt-get -y autoremove


python3 -m venv bioacoustics-env
source bioacoustics-env/bin/activate


pip3 install --upgrade pip
pip3 install wheel
pip3 install cython
pip3 install RPi.GPIO
pip3 install numpy
pip3 install pandas
pip3 install soundfile
pip3 install scikit-learn==0.24.2
pip3 install matplotlib
pip3 install sounddevice
pip3 install numba==0.48.0
pip3 install scipy
pip3 install librosa
pip3 install tqdm
pip3 install ipython
