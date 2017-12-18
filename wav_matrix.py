from struct import unpack
import pyaudio
import numpy as np

CHUNK = 256
FORMAT = pyaudio.paInt32
CHANNELS = 2
RATE = 44100
P = pyaudio.PyAudio()


def gen_device():
    """
    Returns:
         input_index(int):
         output_index(int):
    """
    import re
    dev_count = P.get_device_count()
    i = 0
    input_index = ''
    output_index = ''
    while i < dev_count:
        dev_info = P.get_device_info_by_index(i)
        if re.search('Loopback', dev_info['name']):
            input_index = dev_info['index']
        if re.search("\Adefault", dev_info['name']):
            output_index = dev_info['index']
        i = i + 1

    if input_index == '':
        print "No loopback exists exiting"
        exit(1)
    return input_index, output_index


def gen_stream(input_device, output_device):
    """

    :param input_device:
    :param output_device:
    :return:
    """
    in_stream = P.open(
        format=FORMAT,
        channels=CHANNELS,
        rate=RATE,
        input=True,
        output=True,
        frames_per_buffer=CHUNK,
        input_device_index=input_device
        )

    out_stream = P.open(
        format=FORMAT,
        channels=2,
        rate=RATE,
        input=True,
        output=True,
        frames_per_buffer=CHUNK,
        input_device_index=output_device
        )
    return in_stream, out_stream


def piff(val):
    """
    Var:
        val:
    Returns:

    """
    return int(2 * CHUNK * val / (RATE / (1024 / CHUNK)))
    #return int(2 * CHUNK * val / (RATE / 4))


def calculate_levels(data):
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
    matrix[0] = int(np.mean(power[piff(0):piff(30):1]))
    matrix[1] = int(np.mean(power[piff(30):piff(80):1]))
    matrix[2] = int(np.mean(power[piff(80):piff(190):1]))
    matrix[3] = int(np.mean(power[piff(190):piff(350):1]))
    matrix[4] = int(np.mean(power[piff(350):piff(800):1]))
    matrix[5] = int(np.mean(power[piff(800):piff(5000):1]))
    matrix[6] = int(np.mean(power[piff(5000):piff(10000):1]))
    matrix[7] = int(np.mean(power[piff(10000):piff(20000):1]))
    #print matrix
    matrix = [x / 16000 for x in matrix]
    #matrix = np.divide(np.multiply(matrix, 1), 1000000)
    matrix = np.array(matrix)
    #print matrix
    matrix = matrix.clip(0, 8)
    #print matrix
    return matrix


def draw_matrix():
    """

    :return:
    """
    data = in_stream.read(CHUNK)
    while data != '':
        data = in_stream.read(CHUNK)
        out_stream.write(data)
        display = calculate_levels(data)
        rows = [[], [], [], [], [], [], [], []]
        j = 0
        for i in display:
            k = 0
            while k < int(i):
                rows[j].append("X")
                k = k + 1
            while len(rows[j]) < 8:
                rows[j].append(" ")
            j = j + 1
            rotate = reversed(zip(*rows[::1]))
            for l in rotate:
                print l


if __name__ == '__main__':
    input_device, output_device = gen_device()
    in_stream, out_stream = gen_stream(input_device, output_device)
    draw_matrix()
