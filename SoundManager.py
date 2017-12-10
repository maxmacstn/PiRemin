import threading
import math
import pyaudio
import wave
import sys

import time


class SoundManager(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.p = pyaudio.PyAudio()
        self.stream = self.p.open(format=self.p.get_format_from_width(1),
                                  channels=1,
                                  rate=44000,
                                  input=True,
                                  output=True)
        self.soundOn = True
        self.bitRate = 8800;
        self.volume = 0.1
        self.pitch = 440.0
        self.numberOfFrames = int(self.bitRate)
        self.restFrames = self.numberOfFrames % self.bitRate
        self.waveData = ''

    def run(self):
        print("Playing sound")
        while True:
            self.playSound(self.soundOn)

    def playSound(self, sndOn):
        if (sndOn):
            # code for sound generation
            self.waveData = ''
            for x in range(self.numberOfFrames):
                self.waveData = self.waveData + chr(int(math.sin(x / ((self.bitRate / self.pitch) / math.pi)) * 127 + 128))
            for x in range(self.restFrames):
                self.waveData = self.waveData + chr(128)
            self.stream.write(self.waveData)

    def updateSound(self, newPitch, newVolume):
        self.pitch = newPitch
        self.volume = newVolume

    def shutDownSystem(self):
        self.stream.stop_stream()
        self.stream.close()
        self.p.terminate()

'''
def main():
    test = SoundManager()
    test.start()
    time.sleep(5)
    test.updateSound(test.pitch + 1000, 1.0)

main()
'''
