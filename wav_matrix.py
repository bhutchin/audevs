import wave
from struct import unpack
import alsaaudio as aa
import numpy as np


WAV_FILE = wave.open('/home/rhea/dev/audevs/feelin.wav', 'r')
SAMPLE_RATE = WAV_FILE.getframerate()
NO_CHANNELS = WAV_FILE.getnchannels()
CHUNK = 2048

output = aa.PCM(aa.PCM_PLAYBACK, aa.PCM_NORMAL)
output.setchannels(NO_CHANNELS)
output.setrate(SAMPLE_RATE)
output.setformat(aa.PCM_FORMAT_S16_LE)
output.setperiodsize(CHUNK)


def piff(val):
    """
    Var:
        val:
    Returns:

    """
    return int(2 * CHUNK * val / SAMPLE_RATE)


def calculate_levels(data, chunk, sample_rate):
    """
    Var:
        data:
        chunk:
        sample_rate:
    Returns:
        matrix:
    """
    data = unpack("%dh" % (len(data)/2), data)
    data = np.array(data, dtype='h')
    width = 8
    matrix = [0 for x in range(width)]
    fourier = np.fft.rfft(data)
    fourier = np.delete(fourier, len(fourier)-1)
    power = np.abs(fourier)

    matrix[0] = int(np.mean(power[piff(0):piff(100):1]))
    matrix[1] = int(np.mean(power[piff(100):piff(250):1]))
    matrix[2] = int(np.mean(power[piff(250):piff(400):1]))
    matrix[3] = int(np.mean(power[piff(400):piff(800):1]))
    matrix[4] = int(np.mean(power[piff(800):piff(2500):1]))
    matrix[5] = int(np.mean(power[piff(2500):piff(5000):1]))
    matrix[6] = int(np.mean(power[piff(5000):piff(10000):1]))
    matrix[7] = int(np.mean(power[piff(10000):piff(20000):1]))
    matrix = np.divide(np.multiply(matrix, 1), 1000000)
    matrix = matrix.clip(0, 8)
    #col_to_row(matrix)
    return matrix


def col_to_row(columns):
    rows = [0 for x in range(8)]
    j = 0
    for i in columns:
        rows[j] = " " * i + "X"
        print rows[j]
        j = j + 1

RAW_DATA = WAV_FILE.readframes(CHUNK)
while RAW_DATA != '':
    """
    """
    output.write(RAW_DATA)
    display = calculate_levels(RAW_DATA, CHUNK, SAMPLE_RATE)
    for i in display:
        print "XX" * i
        print "XX" * i
    #print "XX" * display[0]
    #print "XX" * display[1]
    #print "XX" * display[2]
    #print "XX" * display[3]
    #print "XX" * display[4]
    #print "XX" * display[5]
    #print "XX" * display[6]
    #print "XX" * display[7]
    #print "X" * display[8]
    RAW_DATA = WAV_FILE.readframes(CHUNK)
