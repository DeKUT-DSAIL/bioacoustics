import sounddevice as sd
import matplotlib.pyplot as plt

duration = 5 #duration in seconds
fs = 44100
sd.default.channels = 1

print('Recording a 5 seconds long audio...')
my_rec = sd.rec(int(duration * fs))
sd.wait()
print('Done recording. \n')

print(my_rec, '\n', 'Number of samples: ', myrec.shape)

plt.plot(my_rec)
plt.show()
