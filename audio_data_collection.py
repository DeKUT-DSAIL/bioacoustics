import os
import sys
import queue
import logging
import argparse
import subprocess
import numpy as np
import soundfile as sf
from time import sleep
import sounddevice as sd
from shutil import disk_usage
from datetime import datetime

sleep(30) #sleep for thirty seconds to wait the Pi's time to be set.

logging.basicConfig(filename='data.log', level=logging.DEBUG)

try:

    

    parser = argparse.ArgumentParser(description='Detect audio activity and save 10s long audio files')
    parser.add_argument('-c',
                            '--channels',
                            type=int,
                            default=1,
                            metavar='',
                            help='Number of channels (>=1)')

    parser.add_argument('-sr',
                            '--samplerate',
                            type=int,
                            default=48000,
                            metavar='',
                            help='The sampling rate in Hertz (use 48000/41000Hz only)')

    parser.add_argument('-b_l',
                            '--block_length',
                            default=20,
                            metavar='',
                            help="""Length in milliseconds the stream passes to the callback
                            function. These blocks are used in setting the still condition
                            and also are the blocks we check for acoustic activity.""")

    parser.add_argument('-c_d',
                            '--calibration_duration',
                            type=int,
                            default=30,
                            metavar='',
                            help='The length of recording in seconds to use in setting the still condition')

    parser.add_argument('-l_a',
                            '--length_of_saved_audio',
                            type=int,
                            default=10,
                            metavar='',
                            help='The length of recording in seconds to save as an audio file')

    parser.add_argument('-s_n',
                            '--storage_name',
                            type=str,
                            default='none',
                            metavar='',
                            help="""Name of the external storage. Default is 'none'. If no storage
                            name is passed the program will store the recordings in the SD card. The 
                            external device should not be named as 'none'!!!""")

    parser.add_argument('-s_t',
                            '--storage_threshold',
                            type=float,
                            default=0.99,
                            metavar='',
                            help='Ratio of used to total space of external storage or SD card')

    parser.add_argument('-d_n',
                            '--directory_name',
                            type=str,
                            default='recordings',
                            metavar='',
                            help='Name of directory to store datestamped folders containing recordings')

    args = parser.parse_args()



    BLOCKSIZE = int((args.block_length / 1e3) * args.samplerate) #number of samples to process

    CALIBRATION_BLOCKS = int(args.calibration_duration / (args.block_length / 1e3)) #number of blocks to set the still condition

    SAMPLES_SAVED = int((args.samplerate / BLOCKSIZE) * args.length_of_saved_audio) #number of samples to save as a single file


    t = datetime.now()
    name_by_date = t.strftime('%Y-%m-%d')


    def sd_card():
        """Returns a string which is the path to store recordings in the SD card.
        Called when there is no external storage, or when the system
        can't writ to the external storage"""

        folder_path = os.path.join('/home/pi/', args.directory_name, name_by_date)
        return folder_path


    def external_storage():
        """Returns a string which is the path to store recordings in the external storage.
        Called when the user plugs in an external storage device and parse its name in 
        command line"""

        folder_path = os.path.join('/media/pi/', args.storage_name, args.directory_name, name_by_date)
        return folder_path


    if args.storage_name != 'none':
        try:
            folder_path = external_storage()
            if not os.path.exists(folder_path):
                os.makedirs(folder_path)
        except Exception as storage_error:
            logging.info(str(storage_error))
            folder_path = sd_card()
            if not os.path.exists(folder_path):
                os.makedirs(folder_path)

    else:
        folder_path = sd_card()
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)


    q = queue.Queue()

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
        for _ in range(CALIBRATION_BLOCKS):
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
        name_by_time = t.strftime('%H:%M:%S') + '.wav'
        usage = disk_usage(folder_path)
        if usage.used / usage.total < args.storage_threshold:
            file_path = os.path.join(folder_path, name_by_time)
            sf.write(file_path , data, args.samplerate)

        else:
            name = os.path.join(folder_path, name_by_date+'.txt')
            f = open(name, 'a')
            f.write(t.strftime('%H:%M:%S') + '\t Activity Detected \n')
            f.close()

    def main():
        try:
            with sd.InputStream(samplerate = args.samplerate,
                                blocksize = BLOCKSIZE,
                                channels = args.channels,
                                callback = audio_callback):

                mean, std_dev = calibration()
                while True:
                    energy, my_block = block_energy()
                    std_deviation = energy - mean

                    if std_deviation >= 2 * std_dev:
                        print('Activity detected')
                        blocks_of_interest = np.array(my_block)

                        for _ in range(SAMPLES_SAVED - 1):
                            my_block = q.get()
                            my_block = my_block.flatten()
                            blocks_of_interest = np.concatenate((blocks_of_interest, my_block))

                        audio_file_save(blocks_of_interest)


        except KeyboardInterrupt:
            sys.exit()

    if __name__ == '__main__':
        main()

except Exception as er:
    logging.info(str(er))
