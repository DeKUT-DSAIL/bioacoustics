import os
import sys
import queue
import numpy as np
import soundfile as sf
from time import sleep
import sounddevice as sd
from shutil import disk_usage
from datetime import datetime

sleep(30) #sleep for thirty seconds to wait the Pi's time to be set.

CHANNELS = 1

SAMPLERATE = 48000

CALIBRATION_DURATION = 30 #seconds

BLOCK_LENGTH = 20e-3 #20 milliseconds

LENGTH_OF_SAVED_AUDIO = 10 #seconds

PATH = '/home/pi/recordings' #path to store recordings

STORAGE_THRESHOLD = 0.8 #ratio of used to total storage

BLOCKSIZE = int(BLOCK_LENGTH * SAMPLERATE) #number of samples to process

CALIBRATION_BLOCKS = int(CALIBRATION_DURATION / BLOCK_LENGTH) #number of blocks to set the still condition

SAMPLES_SAVED = int((SAMPLERATE / BLOCKSIZE) * LENGTH_OF_SAVED_AUDIO) #number of samples to save as a single file


q = queue.Queue()

t = datetime.now()
date = t.strftime('%Y-%m-%d')
name_by_date = '/' + date

folder_path = PATH + name_by_date

if not os.path.exists(folder_path):
    os.makedirs(folder_path)




def audio_callback(indata, frames, time, status):
    if status:
        print(status)

    q.put(indata.copy())

def calibration():
    """Returns the mean and standard deviation
    of the energies of blocks of sound samples
    for calibration in setting still
    condition for the purpose of activity detection"""

    l = []
    for i in range(CALIBRATION_BLOCKS):
        block = q.get()
        block = block.flatten()
        energy = np.sum(block ** 2)
        l.append(energy)
    std_dev = np.std(l)
    mean = np.mean(l)
    return mean, std_dev


def block_energy():
    """ Returns a block of audio samples and its energy
    The block is fetched from a queue containing the audio blocks"""

    my_block = q.get()
    my_block = my_block.flatten()
    energy = np.sum(my_block ** 2)
    return energy, my_block


def audio_file_save(data):
    """ Saves recorded sound in an external storage.
    It monitors the remaining storage and stops saving
    the files when it is almost full but instead records
    whenever activity is detected in a text file

    Args: data- a numpy array containing audio samples."""

    t = datetime.now()
    current_time = t.strftime('%H:%M:%S')
    usage = disk_usage(PATH)
    usage = dict([('total_space', usage[0]), ('used_space', usage[1])])
    if usage['used_space'] / usage['total_space'] < STORAGE_THRESHOLD:
        file_path = folder_path + '/' +name_by_date + '-' + current_time + '.wav'
        sf.write(file_path , data, SAMPLERATE)

    else:
        name = PATH + name_by_date + '.txt'
        f = open(name, 'a')
        f.write(current_time + '\t Activity Detected \n')
        f.close()

def main():
    try:
        with sd.InputStream(samplerate = SAMPLERATE,
                            blocksize = BLOCKSIZE,
                            channels = CHANNELS,
                            callback = audio_callback):

            mean, std_dev = calibration()
            while True:
                energy, my_block = block_energy()
                std_deviation = energy - mean

                if std_deviation >= 2 * std_dev:
                    print('Activity detected')
                    blocks_of_interest = np.array(my_block)

                    for i in range(SAMPLES_SAVED - 1):
                        my_block = q.get()
                        my_block = my_block.flatten()
                        blocks_of_interest = np.concatenate((blocks_of_interest, my_block))

                    audio_file_save(blocks_of_interest)


    except KeyboardInterrupt:
        sys.exit()

if __name__ == '__main__':
    main()
