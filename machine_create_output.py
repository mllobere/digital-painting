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

while True:
	input_state = GPIO.input(21)
	if input_state == False:
		for i in range(50):
			myStepper2.oneStep(1, Adafruit_MotorHAT.INTERLEAVE)
sys.exit()

for i in range(50):
	myStepper2.oneStep(1, Adafruit_MotorHAT.INTERLEAVE)
for i in range(50):
	myStepper1.oneStep(2, Adafruit_MotorHAT.INTERLEAVE)
sys.exit()



# recommended for auto-disabling motors on shutdown!
def turnOffMotors():
    mh.getMotor(1).run(Adafruit_MotorHAT.RELEASE)
    mh.getMotor(2).run(Adafruit_MotorHAT.RELEASE)
    mh.getMotor(3).run(Adafruit_MotorHAT.RELEASE)
    mh.getMotor(4).run(Adafruit_MotorHAT.RELEASE)

atexit.register(turnOffMotors)

stepstyles = [Adafruit_MotorHAT.SINGLE, Adafruit_MotorHAT.DOUBLE, Adafruit_MotorHAT.INTERLEAVE, Adafruit_MotorHAT.MICROSTEP]


f = open('lines.txt', 'w')
x = 1
xa = 1
oldy= math.sin(math.radians(0)) * 10
for l in range(5):
	for o in range(30):
		f.write('1,30,2\n'); 
	xa = 1
	for i in range(360):	
		y = int((abs(math.sin(math.radians(xa))) - oldy) * 10)
	        oldy= int(abs(math.sin(math.radians(xa))))
		xa = xa + 1
		#f.write(str(xa) + ':  x : ' + str(x) + ' y : ' + str(y) +'\n')
		for j in range(x):
			if(i>180): #tambour
				f.write('1,30,2\n'); 
			else:
				f.write('1,30,1\n'); 
		for k in range(y): #axe
			if(i>90 and i < 270):
				f.write('2,30,1\n');	
			else:
				f.write('2,30,2\n');	
f.close()
time.sleep(0.5)

f = open('lines.txt', 'r')
for line in f:
	a = line.split(',') # line format is stepperNumber, speed, direction
	stepNb = int(a[0])
	speed = int(a[1])
	direction = int(a[2]) #1 forward 2 backward

	if(direction == 1):
		direction = Adafruit_MotorHAT.BACKWARD
	elif(direction ==2):
		direction = Adafruit_MotorHAT.FORWARD

	if(stepNb == 1):
		myStepper1.oneStep(direction, Adafruit_MotorHAT.INTERLEAVE)
	elif(stepNb == 2):	
		myStepper2.oneStep(direction, Adafruit_MotorHAT.INTERLEAVE)
f.close()
sys.exit()