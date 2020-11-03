import os
import sys
import queue
import argparse
import numpy as np
import soundfile as sf
from time import sleep
import sounddevice as sd
from rtc import time_dict
from shutil import disk_usage


sleep(60) #sleep for 1 minute to give the pi time to load the external storage drive

q = queue.Queue()

parser = argparse.ArgumentParser(description='Save Audio Recordings')
parser.add_argument('-ch',
                    '--channels',
                    type=int,
                    metavar='',
                    default=1,
                    help='Number of channels (>0) to be recorded')
parser.add_argument('-b',
                    '--blocksize',
                    type=int,
                    metavar='',
                    default=960,
                    help="""Number of samples in a single chunk of audio sample. Preferred 
                            blocksize is of length 20ms at the sampling frequency used""")

parser.add_argument('-fs',
                    '--samplerate',
                    type=int,
                    metavar='',
                    default=48000,
                    help="""The sampling frequency of audio signal. For the 
                    Raspberry pi, only two are known to work i.e. 44100 and 48000kHz""")

parser.add_argument('-s_t',
                    '--storage_threshold',
                    type=float,
                    metavar='',
                    default=0.99,
                    help='Ratio of used to free space in the external storage device')

parser.add_argument('-p',
                    '--path',
                    type=str,
                    metavar='',
                    help='path to the external storage device')

parser.add_argument('-c_s',
                    '--calibration_samples',
                    type=int,
                    metavar='',
                    default=1500,
                    help="""Number of blocks to use in setting the still condition of the system.
                    Preferrably blocks of an audio sample of length 30s""")

parser.add_argument('-s_s',
                    '--samples_saved',
                    type=int,
                    metavar='',
                    default=500,
                    help="""Number of samples to save as a single wav file.
                         This determines the length of the recording depending
                         on the samplerate""")


args = parser.parse_args()

t = time_dict()
name_by_date = '/' + str(t['tm_year']) + '-' + str(t['tm_mon']) + '-' + str(t['tm_mday'])

folder_path = args.path + name_by_date

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
    for i in range(args.calibration_samples):
        block = q.get()
        block = block.flatten()
        energy = np.sum(block ** 2)
        l.append(energy)
    std_dev = np.std(l)
    mean = np.mean(l)
    print('Done calibrating!')
    return mean, std_dev


def block_energy():
    """ Returns a block of 320 audio samples and its energy
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

    t = time_dict()
    current_time =  str(t['tm_hour']) + '-' + str(t['tm_min']) + '-' +str(t['tm_sec'])
    usage = disk_usage(args.path)
    usage = dict([('total_space', usage[0]), ('used_space', usage[1])])
    if usage['used_space'] / usage['total_space'] >= args.storage_threshold:
        file_path = folder_path + '/' +name_by_date + '-' + current_time + '.wav'
        sf.write(file_path , data, args.samplerate)

    else:
        name = args.path + name_by_date + '.txt'
        f = open(name, 'a')
        f.write(current_time + '\t Activity Detected \n')
        f.close()

def main():
    try:
        with sd.InputStream(samplerate = args.samplerate,
                            blocksize = args.blocksize,
                            channels = args.channels,
                            callback = audio_callback):
            mean, std_dev = calibration()
            while True:
                energy, my_block = block_energy()
                std_deviation = energy - mean

                if std_deviation >= 2 * std_dev:
                    print('Activity detected')
                    blocks_of_interest = np.array(my_block)

                    for i in range(args.samples_saved - 1):
                        my_block = q.get()
                        my_block = my_block.flatten()
                        blocks_of_interest = np.concatenate((blocks_of_interest, my_block))

                    audio_file_save(blocks_of_interest)

    except KeyboardInterrupt:
        sys.exit()

if __name__ == '__main__':
    main()