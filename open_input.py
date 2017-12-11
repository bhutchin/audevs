import pyaudio
import simplejson as json

pa = pyaudio.PyAudio()

dev_count = pa.get_device_count()
i = 0

while i < dev_count:
    dev_info =  pa.get_device_info_by_index(i)
    pretty_dev = json.dumps(dev_info, separators=(':', ','), sort_keys=True, indent=4 * ' ')
    print pretty_dev
    i = i + 1