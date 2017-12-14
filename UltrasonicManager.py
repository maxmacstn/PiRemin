import time
import hcsr04sensor.sensor as ultrasonic
import threading



class Ultrasonic(threading.Thread):
    def __init__(self, trig_pin, echo_pin, max_range = 40):
        threading.Thread.__init__(self)
        self.trig_pin = trig_pin
        self.echo_pin = echo_pin
        self.max_range = max_range
        self.lastUpdateTime = time.time()
        self.lastUpdateValue = 0.0
        self.maxRefreshTime = 100   #100ms
        self.distance = 0.0
        self.isTerminate  = False
        self.sensor = ultrasonic.Measurement(trig_pin, echo_pin)

    def getValue(self):
        #print("getValue = ",self.distance)
        return self.distance

    def run(self):
        # lock = threading.Lock()
        # lock.acquire()
        while not self.isTerminate:
            # print("Ultrasonic ",self.isTerminate)
            if (time.time() - self.lastUpdateTime < (self.maxRefreshTime / 1000) and self.lastUpdateValue != 0.0):
                self.distance = self.lastUpdateValue

            #get new value
            else:
                distance_val = self.sensor.raw_distance(1, 0.1)
                self.lastUpdateValue = distance_val
                self.lastUpdateTime = time.time()
                if (distance_val > self.max_range or distance_val < 0.0):
                    self.distance = 0.0
                #print("Distance_val = ", distance_val)
                self.distance = distance_val

        print("Ultrasonic is stopped")



    def end(self):
        self.isTerminate == True
