from matplotlib.mlab import find
import pyaudio
import numpy as np
import math
import wave

chunk = 256
FORMAT = pyaudio.paInt32
CHANNELS = 2
RATE = 44100


def pitch(signal):
    signal = np.fromstring(signal, 'Int16')
    crossing = [math.copysign(1.0, s) for s in signal]
    index = find(np.diff(crossing));
    f0 = round(len(index) * RATE / (2 * np.prod(len(signal))))
    return f0


wf = wave.open('/home/perses/dev/audevs/audio.wav', 'rb')

p = pyaudio.PyAudio()

stream = p.open(
    format= FORMAT,
    channels= CHANNELS,
    rate= RATE,
    input= True,
    output= True,
    frames_per_buffer=chunk,
    input_device_index=6
    )

out_stream = p.open(
    format= FORMAT,
    channels=2,
    rate= RATE,
    input= True,
    output= True,
    frames_per_buffer= chunk,
    input_device_index=6
    )

data = stream.read(chunk)
#for i in range(0, RATE / chunk * RECORD_SECONDS):
while data != '':
    data = stream.read(chunk)
    Frequency = pitch(data)
    print "%f Frequency" %Frequency
    out_stream.write(data)

