#The most basic code for testing the nosepoke IR Beam

import RPi.GPIO as GPIO
import os
import time

GPIO.setwarnings(False)
GPIO.cleanup()
GPIO.setmode(GPIO.BOARD)

time0 =time.time()
timef = time0+30

#GPIOs
ir1 = 11
led1 = 7

GPIO.setup(ir1, GPIO.IN)
GPIO.setup(led1, GPIO.OUT)

while time.time() < timef:
  GPIO.output(led1,1)
  cross1 = GPIO.input(ir1)
  print (cross1)
  time.sleep(0.1)
  GPIO.output(led1,0)
  time.sleep(0.1)
  
GPIO.cleanup()
  
