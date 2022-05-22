''' 

20 send
21 sensor receive

19 sensor receive
26 send

13 send 
16 sensor receive

'''

import RPi.GPIO as GPIO
import time

# Set the GPIO naming convention
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

S1SEND = 20 
S2SEND = 26
S3SEND = 13

S1REC = 21
S2REC = 19
S3REC = 16


# Set the three GPIO pins for Send
GPIO.setup(S1SEND, GPIO.OUT)
GPIO.setup(S2SEND, GPIO.OUT)
GPIO.setup(S3SEND, GPIO.OUT)


# Set the three GPIO pins for Receive
GPIO.setup(S1REC, GPIO.IN)
GPIO.setup(S2REC, GPIO.IN)
GPIO.setup(S3REC, GPIO.IN)

def high(pin):
    GPIO.output(pin, GPIO.HIGH)

def low(pin):
    GPIO.output(pin, GPIO.LOW)

def check(pin):
    return GPIO.input(pin)

class Cap():
    def __init__(self, send, rec):
        self.send = send
        self.receive = rec
        GPIO.setup(rec, GPIO.IN)
        GPIO.setup(send, GPIO.OUT)
    def check(self):
        self.on_time = time.time()
        print(self)
        high(self.send)
        self.thread = Thread(self.check)
        self.thread.start()
        while True:
            time.sleep(0.01)
            if check(self.receive):
                self.value = time.time() - self.on_time
                break
        self.thread = None
        return self.value
    def __repr__(self):
        return f"Cap({self.send},{self.receive}: on:{self.on_time}, value:{self.value}, dead:{self.thread is None})"



#GPIO.cleanup()


