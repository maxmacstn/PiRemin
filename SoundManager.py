import threading
import pyaudio
import numpy

# for test running
import time

# Audio playback bitrate (44100 is standard HD audio playback)
BITRATE = 44100

# Sound manager extends Thread
class SoundManager(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.p = pyaudio.PyAudio()
        self.stream = self.p.open(format=pyaudio.paFloat32,
                                  channels=1,
                                  rate=BITRATE,
                                  input=True,
                                  output=True)
        self.soundOn = True
        self.amplitude = 1.0
        self.frequency = 440.0
        self.waveData = numpy.float32

    # start the sound synthesis thread
    def run(self):
        print("Playing sound")
        while self.soundOn:
            self.playSound()
        print("Sound terminated")

    # code for sound generation
    def playSound(self):
        if (self.soundOn):
            waveData = (numpy.sin(2*numpy.pi*numpy.arange(BITRATE*0.1)*self.frequency/BITRATE)).astype(numpy.float32)
            if (self.soundOn):
                self.stream.write(self.amplitude * waveData)
        else:
            self.stream.stop_stream()

    # update the frequency and amplitude for sound generation
    def updateSound(self, newFrequency, newAmplitude):
        self.frequency = newFrequency
        if newAmplitude > 1.0:
            self.amplitude = 1.0
        elif newAmplitude < 0.0:
            self.amplitude = 0.0
        self.amplitude = newAmplitude

    # cleanup and shutdown the manager
    def shutDownSystem(self):
        print("Terminating sound")
        self.soundOn = False
        self.stream.stop_stream()
        self.stream.close()
        self.p.terminate()