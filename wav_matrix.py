import wave
from struct import unpack
import alsaaudio as aa
import numpy as np


WAV_FILE = wave.open('/home/perses/dev/audevs/audio.wav', 'r')
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
    # Convert raw data (ASCII string) to numpy array
    data = unpack("%dh" % (len(data)/2), data)
    data = np.array(data, dtype='h')
    width = 8
    matrix = [0 for x in range(width)]

    # Apply FFT - real data
    fourier = np.fft.rfft(data)
    # Remove last element in array to make it the same size as chunk
    fourier = np.delete(fourier, len(fourier)-1)
    # Find average 'amplitude' for specific frequency ranges in Hz
    power = np.abs(fourier)

    matrix[0] = int(np.mean(power[piff(0):piff(156):1]))
    matrix[1] = int(np.mean(power[piff(156):piff(313):1]))
    matrix[2] = int(np.mean(power[piff(313):piff(625):1]))
    matrix[3] = int(np.mean(power[piff(625):piff(1250):1]))
    matrix[4] = int(np.mean(power[piff(1250):piff(2500):1]))
    matrix[5] = int(np.mean(power[piff(2500):piff(5000):1]))
    matrix[6] = int(np.mean(power[piff(5000):piff(10000):1]))
    matrix[7] = int(np.mean(power[piff(10000):piff(20000):1]))

    # Tidy up column values for the LED matrix
    matrix = np.divide(np.multiply(matrix, 1), 1000000)
    matrix = matrix.clip(0, 8)
    return matrix


RAW_DATA = WAV_FILE.readframes(CHUNK)
# Loop while audio data present
while RAW_DATA != '':
    """
    """
    output.write(RAW_DATA)
    display = calculate_levels(RAW_DATA, CHUNK, SAMPLE_RATE)
    print "X" * display[0]
    print "X" * display[1]
    print "X" * display[2]
    print "X" * display[3]
    print "X" * display[4]
    print "X" * display[5]
    print "X" * display[6]
    print "X" * display[7]
    #print "X" * display[8]
    RAW_DATA = WAV_FILE.readframes(CHUNK)
