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


def gen_stream():
    import re
    pa = pyaudio.PyAudio()
    dev_count = pa.get_device_count()
    i = 0
    input_index = ''
    output_index = ''
    while i < dev_count:
        dev_info = pa.get_device_info_by_index(i)
        if re.search('Loopback', dev_info['name']):
            input_index = dev_info['index']
        if re.search("\Adefault", dev_info['name']):
            output_index = dev_info['index']
        i = i + 1

    if input_index == '':
        print "No loopback exists exiting"
        exit(1)
    return input_index, output_index


input, output = gen_stream()


stream = p.open(
    format= FORMAT,
    channels= CHANNELS,
    rate= RATE,
    input= True,
    output= True,
    frames_per_buffer=chunk,
    input_device_index=input
    )

out_stream = p.open(
    format= FORMAT,
    channels=2,
    rate= RATE,
    input= True,
    output= True,
    frames_per_buffer= chunk,
    input_device_index=output
    )

data = stream.read(chunk)
#for i in range(0, RATE / chunk * RECORD_SECONDS):
while data != '':
    data = stream.read(chunk)
    out_stream.write(data)
    frequency = pitch(data)
    print "%f Frequency" %frequency
    #try:

    #except exception as e:
    #    pass

