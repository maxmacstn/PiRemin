import time
import hcsr04sensor.sensor as ultrasonic


class Ultrasonic():
    def __init__(self, trig_pin, echo_pin):
        self.trig_pin = trig_pin
        self.echo_pin = echo_pin
        self.lastUpdateTime = 1.5
        self.lastUpdateValue = 0
        self.maxRefreshTime = 100   #100ms
        self.sensor = ultrasonic.Measurement(trig_pin, echo_pin)

    def getValue(self):

        if(time.time() - self.lastUpdateTime  < (self.maxRefreshTime/1000) and self.lastUpdateValue != 0 ):
            return self.lastUpdateValue

        distance = self.sensor.raw_distance(1,0.0)

        self.lastUpdateValue = distance
        self.lastUpdateTime = time.time()
        return distance

    def end(self):
        GPIO.cleanup()
