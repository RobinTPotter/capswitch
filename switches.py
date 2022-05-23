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
from threading import Thread

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
    return GPIO.input(pin)==1



print("check {}".format(check(S1REC)))

import sys
#sys.exit(0)


class Cap():
    def __init__(self, send, rec):
        self.send = send
        self.receive = rec
        GPIO.setup(rec, GPIO.IN)
        GPIO.setup(send, GPIO.OUT)
        self.on_time=-1
        self.samples = 1
        self.value=-1
        low(self.send)
        self.thread = None
    def start(self):
        self.thread = Thread(None, self.check)
        self.thread.start()

    def check(self):
        self.on_time = time.time()
        #print(self)
        #high(self.send)
        self.running = True
        self.state = True
        #high(self.send)
        while self.running:
            print(self)
            self.samples = 0
            self.value = 0
            for _ in range(500):
                self.on_time = time.time()
                if self.state:
                    high(self.send)
                else:
                    low(self.send)
                self.state = not self.state
                rec= check(self.receive)
                #print("rec {} state {}".format(rec,self.state))
                if rec!=self.state:
                    #print("ding")
                    self.value += int( 100000000 * ( time.time() - self.on_time ) )
                    self.samples += 1
                    #self.running = False
                #else:
                    #print("dong")
                time.sleep(0.0001)

        #print(dir(self.thread))

        #low(self.send)
        #if self.thread.is_alive: self.thread.join()    
        self.thread = None
        return self.value
    def __repr__(self):
        return "Cap({},{} value:{}, dead:{})".format(
                self.send, self.receive, int(self.value/self.samples), self.thread is None)


c = Cap(S1SEND, S1REC)
#c2 = Cap(S2SEND, S2REC)
#c3 = Cap(S3SEND, S3REC)

c.start()
#c2.start()
#c3.start()

time.sleep(30)

c.running = False
#c2.running = False
#c3.running = False


#GPIO.cleanup()


