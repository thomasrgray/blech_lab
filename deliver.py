# Import necessary libraries
import time
import RPi.GPIO as GPIO
from subprocess import Popen
import easygui
import numpy as np
import os
import random
import ast

# Set GPIO mode to BOARD and suppress warnings
GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)

# Function to clear all GPIO outputs
def clearall():
    # Define GPIO pins for outputs and inputs
    outports = [31, 33, 35, 37, 8, 10, 24, 26, 19, 21]
    inports = [11, 13, 15]
    pokelights = [36, 38, 40]
    houselight = 18
    lasers = [12, 22, 16]

    # Set up GPIO pins and turn off outputs
    for i in outports:
        GPIO.setup(i, GPIO.OUT)
        GPIO.output(i, 0)
    for i in inports:
        GPIO.setup(i, GPIO.IN, GPIO.PUD_UP)
    for i in pokelights:
        GPIO.setup(i, GPIO.OUT)
        GPIO.output(i, 0)
    for i in lasers:
        GPIO.setup(i, GPIO.OUT)
        GPIO.output(i, 0)
    GPIO.setup(houselight, GPIO.OUT)
    GPIO.output(houselight, 0)

# Function to clear tastant lines
def clearout(outports=[31, 33, 35, 37], dur=5):
    # Set GPIO mode and set up output ports
    GPIO.setmode(GPIO.BOARD)
    for i in outports:
        GPIO.setup(i, GPIO.OUT)

    # Activate output ports for specified duration and then turn off
    for i in outports:
        GPIO.output(i, 1)
    time.sleep(dur)
    for i in outports:
        GPIO.output(i, 0)

    print('Tastant line clearing complete.')

# Function to calibrate tastant lines
def calibrate(outports=[31, 33, 35, 37], opentime=0.015, repeats=5):
    # Set GPIO mode and set up output ports
    GPIO.setmode(GPIO.BOARD)
    for i in outports:
        GPIO.setup(i, GPIO.OUT)

    # Perform calibration by activating and deactivating output ports
    for rep in range(repeats):
        for j in outports:
            GPIO.output(j, 1)
        time.sleep(opentime)
        for j in outports:
            GPIO.output(j, 0)
        time.sleep(2)

    print('Calibration procedure complete.')

# Function to open and close output ports for a specified number of repeats
def open_repeats(outports=[31, 33, 35, 37], opentime=0.01, repeats=50):
    # Set GPIO mode and set up output ports
    GPIO.setmode(GPIO.BOARD)
    for i in outports:
        GPIO.setup(i, GPIO.OUT)
    for rep in range(repeats):
        for j in outports:
            GPIO.output(j, 1)
        time.sleep(opentime)
        for j in outports:
            GPIO.output(j, 0)
        time.sleep(0.01)

# Function for passive deliveries
def passive(outports=[31, 33, 35, 37], intaninputs=[24, 26, 19, 21], opentimes=[0.01], itimin=20, itimax=30, trials=30, sponttrls=60):
    # Set GPIO mode and set up output and input ports
    GPIO.setmode(GPIO.BOARD)
    for i in outports:
        GPIO.setup(i, GPIO.OUT)
    for i in intaninputs:
        GPIO.setup(i, GPIO.OUT)
    spontout = 8
    GPIO.setup(spontout, GPIO.OUT)
    time.sleep(5 * 60)

    # Run spontaneous trials before the loop
    for i in range(sponttrls):
        time.sleep(10)
        GPIO.output(spontout, 1)
        time.sleep(0.01)
        GPIO.output(spontout, 0)
        print('spont trial ' + str(i + 1))

    # Set and randomize trial order
    tot_trials = len(outports) * trials
    count = 0
    trial_array = trials * range(len(outports))
    random.shuffle(trial_array)
    time.sleep(15)

    # Loop through trials
    for i in trial_array:
        GPIO.output(outports[i], 1)
        GPIO.output(intaninputs[i], 1)
        time.sleep(opentimes[i])
        GPIO.output(outports[i], 0)
        GPIO.output(intaninputs[i], 0)
        count += 1
        iti = random.randint(itimin, itimax)
        print('Trial ' + str(count) + ' of ' + str(tot_trials) + ' completed. ITI = ' + str(iti) + ' sec.')
        time.sleep(iti)

    # Run spontaneous trials after the loop
    for i in range(sponttrls):
        time.sleep(10)
        GPIO.output(spontout, 1)
        time.sleep(0.01)
        GPIO.output(spontout, 0)
        print('spont trial ' + str(i + 1))

    print('Passive deliveries completed')


# Function for spontaneous H2O deliveries
def spontaneous(intaninputs=[8], sleeptime=[0.01], itimin=17, itimax=20, trials=30):
    # Set GPIO mode and set up output ports
    GPIO.setmode(GPIO.BOARD)
    for i in intaninputs:
        GPIO.setup(i, GPIO.OUT)

    # Set and randomize trial order
    tot_trials = len(intaninputs) * trials
    count = 0
    trial_array = trials * range(len(intaninputs))
    random.shuffle(trial_array)
    time.sleep(15)

    # Loop through trials
    for i in trial_array:
        GPIO.output(intaninputs[i], 1)
        time.sleep(sleeptime[i])
        GPIO.output(intaninputs[i], 0)
        count += 1
        iti = random.randint(itimin, itimax)
        print('Trial ' + str(count) + ' of ' + str(tot_trials) + ' completed. ITI = ' + str(iti) + ' sec.')
        time.sleep(iti)

    print('Spontaneous recording completed')
