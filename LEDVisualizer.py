import threading
from neopixel import *
import time


# LED Visualizer extends Thread
class LEDVisualizer(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

        # LED strip configuration:
        LED_COUNT = 6  # Number of LED pixels.
       # LED_PIN = 18  # GPIO pin connected to the pixels (18 uses PWM!).
        LED_PIN = 21 # GPIO pin connected to the pixels (21 = PCM)
        # LED_PIN        = 10      # GPIO pin connected to the pixels (10 uses SPI /dev/spidev0.0).
        LED_FREQ_HZ = 800000  # LED signal frequency in hertz (usually 800khz)
        LED_DMA = 5  # DMA channel to use for generating signal (try 5)
        LED_BRIGHTNESS = 255  # Set to 0 for darkest and 255 for brightest
        LED_INVERT = False  # True to invert the signal (when using NPN transistor level shift)
        LED_CHANNEL = 0  # set to '1' for GPIOs 13, 19, 41, 45 or 53
        LED_STRIP = ws.WS2811_STRIP_GRB  # Strip type and colour ordering
        # Create NeoPixel object with appropriate configuration.
        self.strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS,
                                       LED_CHANNEL, LED_STRIP)
        self.ultrasonicDist = [255, 255, 255, 255, 255, 255, 255, 255, 255, 255]
        self.ultrasonicDistPos = 0
        self.ultrasonicAVGvalue = 0;

        self.stopLight = False
        self.mode = 0
        # Intialize the library (must be called once before other functions).
        self.strip.begin()

    def wheel(self, pos):
        """Generate rainbow colors across 0-255 positions."""
        if pos < 85:
            return Color(pos * 3, 255 - pos * 3, 0)
        elif pos < 170:
            pos -= 85
            return Color(255 - pos * 3, 0, pos * 3)
        else:
            pos -= 170
            return Color(0, pos * 3, 255 - pos * 3)

    def run(self):
        # for i in range(self.strip.numPixels()):
        #    self.strip.setPixelColor(i, self.wheel((i ) & 255))
        # self.strip.show()
        while (self.stopLight == False):

            if (self.mode == 0):
                self.led_off()
            if (self.mode == 1):
                self.rainbow()
            if (self.mode == 2):
                self.vu()
            if (self.mode == -1):
                self.led_off()
                break

        print("LED is stopped")

    def getTransformedVal(self, rawVal):
        rawVal + 2
        if rawVal < 2:
            rawVal = 0
        if rawVal > 50:
            rawVal = 0
        inputLowVal = 0
        inputHighVal = 50
        outputLowVal = 0
        outputHighVal = 255

        transformedVal = (rawVal - inputLowVal) / (inputHighVal - inputLowVal) * (outputHighVal - outputLowVal) + outputLowVal

        self.ultrasonicDist[self.ultrasonicDistPos] = transformedVal
        self.ultrasonicDistPos += 1
        if self.ultrasonicDistPos == len(self.ultrasonicDist):
            self.ultrasonicDistPos = 0

        avgVal = sum(self.ultrasonicDist) / len(self.ultrasonicDist)
        #print(avgVal)
        return avgVal

    def rainbow(self, wait_ms=20, iterations=1):
        """Draw rainbow that fades across all pixels at once."""
        for j in range(256 * iterations):
            for i in range(self.strip.numPixels()):
                if (self.mode != 1):
                    return
                self.strip.setPixelColor(i, self.wheel((i + j) & 255))
            self.strip.show()
            time.sleep(wait_ms / 1000.0)

    def updateLEDEffects(self, ultrasonicVal):
        if(self.mode == 1):
            self.setBrightness(ultrasonicVal)

    def updateBrightness(self):

        #print("avgval : ", self.ultrasonicAVGvalue)
        if (self.mode != 1):
            self.strip.setBrightness(255)
            self.strip.show()
            return
        brightness = self.ultrasonicAVGvalue
        self.strip.setBrightness(brightness)
        self.strip.show()

    def receiveUltrasonicValue(self,rawVal):
        self.ultrasonicAVGvalue = int(self.getTransformedVal(rawVal))
        if self.ultrasonicAVGvalue > 255:
            print("Brightness Error at : receiveUltrasonicValue()")
            return


    def vu(self):

        level = self.ultrasonicAVGvalue
        for i in range(self.strip.numPixels()):
            self.strip.setPixelColorRGB(i, 0, 0, 0)
        if level > 20:
            self.strip.setPixelColorRGB(0, 0, 255, 0)
        if level > 50:
            self.strip.setPixelColorRGB(1, 0, 255, 0)
        if level > 80:
            self.strip.setPixelColorRGB(2, 0, 255, 0)
        if level > 110:
            self.strip.setPixelColorRGB(3, 0, 255, 0)
        if level > 150:
            self.strip.setPixelColorRGB(4, 255, 255, 0)
        if level > 200:
            self.strip.setPixelColorRGB(5, 255, 0, 0)

        self.strip.show()

    def changeMode(self):
        self.mode += 1
        self.mode = self.mode % 3
        print("LED Mode = ", self.mode)

    def led_off(self):
        for i in range(self.strip.numPixels()):
            self.strip.setPixelColorRGB(i, 0, 0, 0)
        self.strip.show()

    # stop the visualizer thread
    def end(self):
        self.mode = -1
        self.stopLight = True

