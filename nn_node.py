from pyaudio import PyAudio
import math
import time

p = PyAudio()
BITRATE = 16000 #number of frames per second/frameset.
LENGTH = 3 #seconds to play sound
THRESHOLD = -1.0

def play_tone(frequency, delay):
    SILENCEFRAMES = int(BITRATE * LENGTH * delay)
    NUMBEROFFRAMES = int(BITRATE * LENGTH)
    RESTFRAMES = (SILENCEFRAMES + NUMBEROFFRAMES) % BITRATE
    WAVEDATA = ''

    for x in xrange(SILENCEFRAMES):
        WAVEDATA = WAVEDATA+chr(128)

    for x in xrange(NUMBEROFFRAMES):
        WAVEDATA = WAVEDATA+chr(int(math.sin(x/((BITRATE/frequency)/math.pi))*127+128))

    for x in xrange(RESTFRAMES):
        WAVEDATA = WAVEDATA+chr(128)

    return WAVEDATA

def actually_play(wavedatas):
    wavedatas = [data for data in wavedatas if data]
    n_datas = len(wavedatas)
    actual_data = ''
    for data in zip(*wavedatas):
        actual_data += chr(int(sum([ord(x) for x in data]) / n_datas))
    stream = p.open(format = p.get_format_from_width(1),
                    channels = 1,
                    rate = BITRATE,
                    output = True)

    stream.write(actual_data)
    stream.stop_stream()
    stream.close()
    return [data[len(actual_data):] for data in wavedatas if len(data) > len(actual_data)]

class NetworkNode(object):
    def __init__(self, frequency, delay = 0, connection_map = None):
        self.frequency = frequency
        self.delay = delay
        self.connection_map = connection_map or {}
        self.current_potential = 0
        self.next_potential = 0

    def step(self):
        if self.current_potential > THRESHOLD:
            self.current_data = play_tone(self.frequency, self.delay)
        self.next_potential = 0

    def transmit(self):
        for other_node, strength in self.connection_map.items():
            other_node.next_potential += self.current_potential * strength
        self.current_potential = 0

    def next(self):
        self.current_potential = self.next_potential

    def update_weight(self, other, adjustment):
        pass

if __name__ == '__main__':
    n1 = NetworkNode(261.63, 0)
    n2 = NetworkNode(440, 0)
    n3 = NetworkNode(392, 1)
    n1.current_potential = 5
    n2.current_potential = 5
    n3.current_potential = 5
    n1.step()
    n2.step()
    n3.step()
    print len(n1.current_data)
    print len(n2.current_data)
    print len(n3.current_data)
    wavedatas = actually_play([n1.current_data, n2.current_data, n3.current_data])
    print len(wavedatas)
    wavedatas = actually_play(wavedatas)
    print len(wavedatas)
    p.terminate()
