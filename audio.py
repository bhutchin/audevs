import pyaudio
import struct
import numpy
import wave

CHUNK = 1048
FORMAT = pyaudio.paInt16
CHANNELS = 2
RATE = 44100
p = pyaudio.PyAudio()

def stream():
    stream = p.open(
        format=FORMAT,
        channels=CHANNELS,
        rate=RATE,
        input=True,
        output=True,
        frames_per_buffer=CHUNK
    )

    data = stream.read(CHUNK)


def file_play():
    wf = wave.open('/home/perses/dev/audevs/audio.wav', 'rb')

    stream = p.open(
        format=p.get_format_from_width(wf.getsampwidth()),
        channels=wf.getnchannels(),
        rate=wf.getframerate(),
        output=True,
    )
    data = wf.readframes(CHUNK)
    while data != '':
        stream.write(data)
        decoded = numpy.fromstring(data, dtype=numpy.int8);
        print decoded
        data = wf.readframes(CHUNK)
    stream.close()
    p.terminate()


file_play()
