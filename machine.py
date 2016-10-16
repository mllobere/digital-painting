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

#rand = random.Random()

CONST_SPEED_DEFAULT = 50

# create a default object, no changes to I2C address or frequency
mh = Adafruit_MotorHAT()
myStepper1 = mh.getStepper(100, 1)    # 200 steps/rev, motor port #1
myStepper2 = mh.getStepper(100, 2)    # 200 steps/rev, motor port #2

#for i in range(400):
#	myStepper2.oneStep(2, Adafruit_MotorHAT.INTERLEAVE)
#for i in range(500):
#	myStepper1.oneStep(1, Adafruit_MotorHAT.INTERLEAVE)
#sys.exit()

f = open('lines.txt', 'w')
x = 10
xa = 1
oldy= math.sin(math.radians(0)) * 10
for l in range(1):
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



# recommended for auto-disabling motors on shutdown!
def turnOffMotors():
    mh.getMotor(1).run(Adafruit_MotorHAT.RELEASE)
    mh.getMotor(2).run(Adafruit_MotorHAT.RELEASE)
    mh.getMotor(3).run(Adafruit_MotorHAT.RELEASE)
    mh.getMotor(4).run(Adafruit_MotorHAT.RELEASE)

atexit.register(turnOffMotors)

stepstyles = [Adafruit_MotorHAT.SINGLE, Adafruit_MotorHAT.DOUBLE, Adafruit_MotorHAT.INTERLEAVE, Adafruit_MotorHAT.MICROSTEP]

#verrou = RLock()

class Stepper(Thread):

    def __init__(self, stepper, name, direction, speed, id, semaphore):
        Thread.__init__(self)
        self.stepper = stepper
        self.pos = 0
        self.direction = direction
        self.style = Adafruit_MotorHAT.INTERLEAVE
        self.name = name
        self.speed = speed
        self.stepper.setSpeed(self.speed)
        self.q = Queue(maxsize=0)
	self.exit = 0
	self.id = id
	self.semaphore = semaphore
	self.rune = 1

    def exit(self):
	self.rune = 0

    def reset(self):      
        self.q.put((0, self.direction, CONST_SPEED_DEFAULT))

    def getPositionType(self, pos):
        if(self.pos < pos):
            return 1
        else:
            return 2

    def setPosition(self, pos, dir):
	self.rune = 1
        self.q.put((pos, dir, self.speed))

    def getSpeedType(self, speed):
        if(self.speed < speed):
           return 1
        else:
           return 2

    def setSpeed(self, speed):
        self.q.put((self.pos, self.direction, speed))

    def set(self, pos, direction, speed):
	self.rune = 1
        self.q.put((pos, direction, speed))

    def step(self, numbers):
        print("do nothing")

    def run(self):
	while(self.rune == 1):
		while not self.q.empty():
			print("not empty")
			try:
				self.rune = 1
				item = self.q.get()
				self.pos = item[0]
				self.direction = item[1]
				newSpeed = item[2]
				while(self.pos > 1 or newSpeed > self.speed):
					if(self.id == 1) :
						print("   stepper" + self.name + "pos " +  str(self.pos) + " dir " + str(self.direction) + " speed " + str(self.speed))
					else:
						print("stepper" + self.name + "pos " +  str(self.pos) + " dir " + str(self.direction) + " speed " + str(self.speed))
					if(self.pos > 1):
						self.stepper.oneStep(self.direction, self.style)
						self.pos = self.pos - 1
					if(newSpeed > self.speed):
						self.stepper.setSpeed(self.speed)
						self.speed = self.speed + 1
			finally:
				self.semaphore.release()
				self.rune = 0
				self.speed = CONST_SPEED_DEFAULT
		self.semaphore.release()
		time.sleep(0.2)


semaphore = Semaphore(2)

# Création des threads
thread_1 = Stepper(myStepper1, "stepper1", Adafruit_MotorHAT.BACKWARD, CONST_SPEED_DEFAULT, 1, semaphore)
thread_2 = Stepper(myStepper2, "stepper2", Adafruit_MotorHAT.BACKWARD, CONST_SPEED_DEFAULT, 2, semaphore)

#tambour (thread1)
#thread_1.set(200,Adafruit_MotorHAT.FORWARD, CONST_SPEED_DEFAULT)
#thread_2.setPosition(50,Adafruit_MotorHAT.BACKWARD)
#thread_1.reset()
#thread_1.set(20, Adafruit_MotorHAT.FORWARD, CONST_SPEED_DEFAULT)

#thread_2.setPosition(100,Adafruit_MotorHAT.FORWARD)
#thread_1.set(300,Adafruit_MotorHAT.BACKWARD, CONST_SPEED_DEFAULT)
#sys.exit()
#myStepper1.setSpeed(50)
#myStepper2.setSpeed(50)

# Lancement des threads
thread_1.start()
thread_2.start()

x = 200
y = 200
newspeed = 600

loop = 1
for i in range(loop):
	print("loop " + str(loop))
	semaphore.acquire()
	semaphore.acquire()
	thread_1.set(x,Adafruit_MotorHAT.BACKWARD, newspeed)
	thread_2.set(y,Adafruit_MotorHAT.FORWARD, CONST_SPEED_DEFAULT)
	semaphore.acquire()
	semaphore.acquire()
	thread_1.set(x,Adafruit_MotorHAT.FORWARD, newspeed)
	thread_2.set(y,Adafruit_MotorHAT.FORWARD, CONST_SPEED_DEFAULT)
	semaphore.acquire()
	semaphore.acquire()
	thread_1.set(x,Adafruit_MotorHAT.FORWARD, newspeed)
	thread_2.set(y,Adafruit_MotorHAT.BACKWARD, CONST_SPEED_DEFAULT)
	semaphore.acquire()
	semaphore.acquire()
	thread_1.set(x,Adafruit_MotorHAT.BACKWARD, newspeed)
	thread_2.set(y,Adafruit_MotorHAT.BACKWARD, CONST_SPEED_DEFAULT)

thread_1.join()
thread_2.join()
sys.exit()

megaloop = 0
for j in range(megaloop):
	loop = 10
	#glissiere (thread 2)
	for i in range(loop):	
		thread_1.set(20,Adafruit_MotorHAT.FORWARD, CONST_SPEED_DEFAULT)
		thread_2.set(40,Adafruit_MotorHAT.BACKWARD, CONST_SPEED_DEFAULT)
		thread_1.set(20,Adafruit_MotorHAT.FORWARD, CONST_SPEED_DEFAULT)
		thread_2.set(40,Adafruit_MotorHAT.FORWARD, CONST_SPEED_DEFAULT)	
	thread_1.set(160,Adafruit_MotorHAT.BACKWARD, CONST_SPEED_DEFAULT)
	thread_2.set(40,Adafruit_MotorHAT.FORWARD, CONST_SPEED_DEFAULT)
	megaloop = megaloop - 1


thread_1.join()
thread_2.join()
sys.exit()

 #  if(self.newPos > self.pos and self.directionType == 1):
 #                   print("run +" + self.name)
 #                   self.stepper.step(1, self.direction, self.style)
 #                   self.pos = self.pos + 1
 #          active = 1
#           elif(self.newPos < self.pos and self.directionType == 2):
 #                   print("run -" + self.name)
 #                   self.stepper.step(1, self.direction, self.style)
 #                   self.pos = self.pos - 1
 #          active = 1
