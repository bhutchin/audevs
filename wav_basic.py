from scikits.audiolab import wavread
import pylab

signal, fs, enc = wavread('/home/perses/dev/audevs/leftchannel.wav')

#print signal
for i in signal:
    print i * 100
        #pylab.specgram(int(i))
        #pylab.show()
