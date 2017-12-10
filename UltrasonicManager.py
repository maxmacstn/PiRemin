import RPi.GPIO as GPIO
import time

class Ultrasonic():
    def __init__(self, trig_pin, echo_pin):
        self.trig_pin = trig_pin
        self.echo_pin = echo_pin
        self.lastUpdateTime = 1.5
        self.lastUpdateValue = 30
        self.maxRefreshTime = 100   #100ms

        GPIO.setmode(GPIO.BCM)
        print("Distance Measurement In Progress")

        GPIO.setup(self.trig_pin, GPIO.OUT)
        GPIO.setup(self.echo_pin, GPIO.IN)

        GPIO.output(self.trig_pin, False)

    def getValue(self):

        if(time.time() - self.lastUpdateTime  < (self.maxRefreshTime/1000)):
            return self.lastUpdateValue

        GPIO.output(self.trig_pin, True)
        time.sleep(0.00001)
        GPIO.output(self.trig_pin, False)
        count = 0
        pulse_end = pulse_start = time.time()

        while GPIO.input(self.echo_pin) == 0:
            pulse_start = time.time()
            count += 1
            # print(count)
            if (count >= 70):
                break

        while GPIO.input(self.echo_pin) == 1:
            pulse_end = time.time()

        pulse_duration = pulse_end - pulse_start

        distance = pulse_duration * 17150

        distance = round(distance, 2)

        self .lastUpdateValue = distance
        self.lastUpdateTime = time.time()
        return distance

    def end(self):
        GPIO.cleanup()
