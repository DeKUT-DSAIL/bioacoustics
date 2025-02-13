import logging


logging.basicConfig(filename='data.log',
                    level=logging.INFO,
                    format='%(asctime)s:%(levelname)s:%(message)s')



try:
    import os
    import csv
    import sys
    import queue
    import argparse
    import subprocess
    import numpy as np
    import soundfile as sf
    from time import sleep
    from gpiozero import LED
    import sounddevice as sd
    from shutil import disk_usage
    from datetime import datetime
    import librosa

    #sleep(30) #sleep for thirty seconds to wait the Pi's time to be set.


    parser = argparse.ArgumentParser(description='Detect audio activity and save 10s long audio files')
    parser.add_argument('-c',
                            '--channels',
                            type=int,
                            default=1,
                            metavar='',
                            help='Number of channels (>=1)')

    parser.add_argument('-d',
                            '--deviceID',
                            type=int,
                            required=True,
                            metavar='',
                            help='Default device ID')

    parser.add_argument('-rs',
                            '--recording_samplerate',
                            type=int,
                            required=True,
                            metavar='',
                            help='The sampling rate in Hertz')

    parser.add_argument('-rr',
                            '--resampling_rate',
                            type=int,
                            required=True,
                            metavar='',
                            help='Resampling rate')

    parser.add_argument('-r',
                            '--resampling',
                            type=bool,
                            required=True,
                            metavar='',
                            help='Whether to resample audio or not.')

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


    activity_led = LED(24) #activity LED blink pin

    BLOCKSIZE = int((args.block_length / 1e3) * args.recording_samplerate) #number of samples to process

    NUM_OF_CALIBRATION_BLOCKS = int(args.calibration_duration / (args.block_length / 1e3)) #number of blocks to set the still condition

    NUM_OF_BLOCKS_TO_SAVE = int((args.recording_samplerate / BLOCKSIZE) * args.length_of_saved_audio) #number of blocks to save as a single file
    print(NUM_OF_BLOCKS_TO_SAVE)
    #sd.default.device = args.deviceID

    q = queue.Queue()

    def audio_callback(indata, frames, time, status):
        if status:
            print(status)

        q.put(indata.copy())

    def calibration(date):
        """Returns the mean and standard deviation
        of the energies of blocks of sound samples
        for calibration in setting still
        condition for the purpose of activity detection"""

        l = []
        for _ in range(NUM_OF_CALIBRATION_BLOCKS):
            block = q.get()
            block = block.flatten()
            energy = np.sum(block ** 2)
            l.append(energy)
        std_dev = np.std(l)
        mean = np.mean(l)
        l = []
        l.extend((date, mean, std_dev))

        with open('calibration.csv', mode = 'a') as file:
            create = csv.writer(file)
            create.writerow(l)
        print(mean, std_dev)
        return mean, std_dev


    def block_energy():
        """ Returns a block of audio samples and its energy
        The block is fetched from a queue containing the audio blocks"""

        my_block = q.get()
        my_block = my_block.flatten()
        energy = np.sum(my_block ** 2)
        return energy, my_block

    def sd_card():
        """Returns a string which is the path to store recordings in the SD card.
        Called when there is no external storage, or when the system
        can't writ to the external storage"""

        folder_path = os.path.join('/home/pi/', args.directory_name)
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)

        return folder_path


    def external_storage():
        """Returns a string which is the path to store recordings in the external storage.
        Called when the user plugs in an external storage device and parse its name in
        command line"""

        folder_path = os.path.join('/media/pi/', args.storage_name, args.directory_name)
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)
        return folder_path

    def audio_resampling(data):
        """Resamples audio
        Args: data- audio samples array
        Returns resampled audio array"""

        if args.channels != 1:
            channels_samples = np.array([])
            for i in range(args.channels):
                channels_samples = np.concatenate((channels_samples, librosa.resample(data[:,i], args.recording_samplerate, args.resampling_rate)))

            resampled_data = channels_samples.reshape((int(args.length_of_saved_audio * args.resampling_rate), args.channels))
        else:
            resampled_data = librosa.resample(data, orig_sr=args.recording_samplerate, target_sr=args.resampling_rate)

        return resampled_data


    def audio_file_save(folder_path, current_time, data, name_by_date):
        """ Saves recorded sound in the available storage.
        It monitors the remaining storage and stops saving
        the files when it is almost full but instead records
        whenever activity is detected in a text file

        Args: data- a numpy array containing audio samples.
              folder_path- path to save recording
              current_time- current time
              name_by_dat- timestamp name"""

        name_by_time = current_time + '.wav' #timestamp for the audio file name
        usage = disk_usage(folder_path)
        if usage.used / usage.total < args.storage_threshold:
            file_path = os.path.join(folder_path, name_by_time)

            if args.resampling:
                sampling_rate = args.resampling_rate
                audio = audio_resampling(data)
            else:
                sampling_rate = args.recording_samplerate
                audio = data

            sf.write(file_path , audio, sampling_rate)

        else:
            name = os.path.join(folder_path, name_by_date + '.txt')
            f = open(name, 'a')
            f.write(current_time + '\t Activity Detected \n')
            f.close()

    def main():
        try:
            with sd.InputStream(samplerate = args.recording_samplerate,
                                blocksize = BLOCKSIZE,
                                channels = args.channels,
                                callback = audio_callback):
                t = datetime.now()
                date = t.strftime('%Y-%m-%d')
                mean, std_dev = calibration(date)
                while True:
                    t = datetime.now()
                    energy, my_block = block_energy()
                    std_deviation = energy - mean

                    if std_deviation >= 2 * std_dev:
                        print('Activity detected', (energy, std_deviation))
                        activity_led.on()
                        blocks_of_interest = np.array(my_block)


                        for _ in range(NUM_OF_BLOCKS_TO_SAVE - 1):
                            my_block = q.get()
                            my_block = my_block.flatten()
                            blocks_of_interest = np.concatenate((blocks_of_interest, my_block))


                        if args.channels != 1:
                            audio = blocks_of_interest.reshape((int(args.recording_samplerate * args.length_of_saved_audio), args.channels))
                        else:
                            audio = blocks_of_interest

                        current_time = t.strftime('%Y-%m-%d-%H-%M-%S')
                        name_by_date = t.strftime('%Y-%m-%d')

                        try:
                            if args.storage_name != 'none':
                                folder_path = external_storage()
                                audio_file_save(folder_path, current_time, audio, name_by_date)

                            else:
                                folder_path = sd_card()
                                audio_file_save(folder_path, current_time, audio, name_by_date)

                        except Exception as storage_error:
                            logging.info(str(storage_error))
                            folder_path = sd_card()
                            audio_file_save(folder_path, current_time, audio, name_by_date)
                        activity_led.off()


        except KeyboardInterrupt:
            sys.exit()

    if __name__ == '__main__':
        main()

except Exception as er:
    print(er)
    logging.info(str(er))
