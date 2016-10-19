#!/usr/bin/python
# -*- coding: iso-8859-15 -*-
import Tkinter
import time
from threading import Thread, RLock, Semaphore
from random import randint
import sys
import Queue
from Adafruit_MotorHAT import Adafruit_MotorHAT, Adafruit_DCMotor, Adafruit_StepperMotor
import atexit
import math
from Queue import Queue
import RPi.GPIO as GPIO

CONST_SPEED_DEFAULT = 50
GPIO.setmode(GPIO.BCM)
GPIO.setup(21, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# create a default object, no changes to I2C address or frequency
mh = Adafruit_MotorHAT()
myStepper1 = mh.getStepper(CONST_SPEED_DEFAULT, 1)    # 200 steps/rev, motor port #1
myStepper2 = mh.getStepper(CONST_SPEED_DEFAULT, 2)    # 200 steps/rev, motor port #2

input_state = GPIO.input(21)

#while True:
#	input_state = GPIO.input(21)
#	if input_state == False:
#		for i in range(50):
#			myStepper2.oneStep(1, Adafruit_MotorHAT.INTERLEAVE)
#sys.exit()

#for i in range(50):
#	myStepper1.oneStep(2, Adafruit_MotorHAT.INTERLEAVE)
#sys.exit()


# recommended for auto-disabling motors on shutdown!
def turnOffMotors():
    mh.getMotor(1).run(Adafruit_MotorHAT.RELEASE)
    mh.getMotor(2).run(Adafruit_MotorHAT.RELEASE)
    mh.getMotor(3).run(Adafruit_MotorHAT.RELEASE)
    mh.getMotor(4).run(Adafruit_MotorHAT.RELEASE)

atexit.register(turnOffMotors)

stepstyles = [Adafruit_MotorHAT.SINGLE, Adafruit_MotorHAT.DOUBLE, Adafruit_MotorHAT.INTERLEAVE, Adafruit_MotorHAT.MICROSTEP]

#curve (does not work)
curve = 0
if(curve):
	myStepper1.setSpeed(50)
	myStepper2.setSpeed(50)
	x = 1
	y = 1
	for i in range(10):	
		x = i
		y = x*x
		for j in range(x):	
			myStepper1.step(1, Adafruit_MotorHAT.BACKWARD, Adafruit_MotorHAT.MICROSTEP)
		#for k in range(y):
		#	myStepper2.step(1, Adafruit_MotorHAT.BACKWARD, Adafruit_MotorHAT.MICROSTEP)
	sys.exit()

#jer
myStepper1.setSpeed(200) #tambour
myStepper2.setSpeed(50) #axe
	
i = 1
j = 50

for k in range(50):
	
	print("k " + str(k))

	for n in range(j):
		myStepper1.oneStep(Adafruit_MotorHAT.BACKWARD, Adafruit_MotorHAT.MICROSTEP)

	for m in range(i):
		myStepper2.oneStep(Adafruit_MotorHAT.BACKWARD, Adafruit_MotorHAT.MICROSTEP)	
 
	i = i + 1
	j = j - 1
i = 1
j = 50
for k in range(50):
	
	print("k " + str(k))

	for n in range(j):
		myStepper1.oneStep(Adafruit_MotorHAT.FORWARD, Adafruit_MotorHAT.MICROSTEP)

	for m in range(i):
		myStepper2.oneStep(Adafruit_MotorHAT.FORWARD, Adafruit_MotorHAT.MICROSTEP)	
 
	i = i + 1
	j = j - 1
i = 1
j = 50
for k in range(50):
	
	print("k " + str(k))

	for n in range(j):
		myStepper1.oneStep(Adafruit_MotorHAT.FORWARD, Adafruit_MotorHAT.MICROSTEP)

	for m in range(i):
		myStepper2.oneStep(Adafruit_MotorHAT.FORWARD, Adafruit_MotorHAT.MICROSTEP)	
 
	i = i + 1
	j = j - 1
i = 1
j = 50
for k in range(50):
	
	print("k " + str(k))

	for n in range(j):
		myStepper1.oneStep(Adafruit_MotorHAT.BACKWARD, Adafruit_MotorHAT.MICROSTEP)

	for m in range(i):
		myStepper2.oneStep(Adafruit_MotorHAT.BACKWARD, Adafruit_MotorHAT.MICROSTEP)	
 
	i = i + 1
	j = j - 1
sys.exit()

#diagonale
myStepper1.setSpeed(50) #tambour
myStepper2.setSpeed(50) #axe
for i in range(10):	
	for j in range(200):
		myStepper1.step(1, Adafruit_MotorHAT.BACKWARD, Adafruit_MotorHAT.SINGLE)
		myStepper2.step(1, Adafruit_MotorHAT.BACKWARD, Adafruit_MotorHAT.SINGLE)
	myStepper2.step(25, Adafruit_MotorHAT.BACKWARD, Adafruit_MotorHAT.SINGLE)
	for j in range(200):
		myStepper1.step(1, Adafruit_MotorHAT.FORWARD, Adafruit_MotorHAT.SINGLE)
		myStepper2.step(1, Adafruit_MotorHAT.FORWARD, Adafruit_MotorHAT.SINGLE)
	myStepper2.step(25, Adafruit_MotorHAT.BACKWARD, Adafruit_MotorHAT.SINGLE)
for i in range(10):	
	myStepper1.step(15, Adafruit_MotorHAT.BACKWARD, Adafruit_MotorHAT.SINGLE)
	myStepper2.step(200, Adafruit_MotorHAT.FORWARD, Adafruit_MotorHAT.SINGLE)
	myStepper1.step(15, Adafruit_MotorHAT.BACKWARD, Adafruit_MotorHAT.SINGLE)
	myStepper2.step(200, Adafruit_MotorHAT.BACKWARD, Adafruit_MotorHAT.SINGLE)
sys.exit()

#quadrillage
myStepper1.setSpeed(50)
myStepper2.setSpeed(50)
for i in range(10):	
	myStepper1.step(200, Adafruit_MotorHAT.BACKWARD, Adafruit_MotorHAT.SINGLE)
	myStepper2.step(15, Adafruit_MotorHAT.BACKWARD, Adafruit_MotorHAT.SINGLE)
	myStepper1.step(200, Adafruit_MotorHAT.FORWARD, Adafruit_MotorHAT.SINGLE)
	myStepper2.step(15, Adafruit_MotorHAT.BACKWARD, Adafruit_MotorHAT.SINGLE)
for i in range(10):	
	myStepper1.step(15, Adafruit_MotorHAT.BACKWARD, Adafruit_MotorHAT.SINGLE)
	myStepper2.step(200, Adafruit_MotorHAT.FORWARD, Adafruit_MotorHAT.SINGLE)
	myStepper1.step(15, Adafruit_MotorHAT.BACKWARD, Adafruit_MotorHAT.SINGLE)
	myStepper2.step(200, Adafruit_MotorHAT.BACKWARD, Adafruit_MotorHAT.SINGLE)
sys.exit()
