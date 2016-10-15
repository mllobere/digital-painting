#!/usr/bin/python
# -*- coding: iso-8859-15 -*-
import Tkinter
import time
from threading import Thread, RLock
from random import randint
import sys
import Queue
from Adafruit_MotorHAT import Adafruit_MotorHAT, Adafruit_DCMotor, Adafruit_StepperMotor
import atexit
from Queue import Queue

#rand = random.Random()

CONST_SPEED_DEFAULT = 50

# create a default object, no changes to I2C address or frequency
mh = Adafruit_MotorHAT()

# recommended for auto-disabling motors on shutdown!
def turnOffMotors():
    mh.getMotor(1).run(Adafruit_MotorHAT.RELEASE)
    mh.getMotor(2).run(Adafruit_MotorHAT.RELEASE)
    mh.getMotor(3).run(Adafruit_MotorHAT.RELEASE)
    mh.getMotor(4).run(Adafruit_MotorHAT.RELEASE)

atexit.register(turnOffMotors)

stepstyles = [Adafruit_MotorHAT.SINGLE, Adafruit_MotorHAT.DOUBLE, Adafruit_MotorHAT.INTERLEAVE, Adafruit_MotorHAT.MICROSTEP]

verrou = RLock()

class Stepper(Thread):

    def __init__(self, stepper, name, direction, speed, id):
        Thread.__init__(self)
        self.stepper = stepper
        self.pos = 0
        #self.newPos = 0
        self.direction = direction
        self.style = Adafruit_MotorHAT.DOUBLE
        self.name = name
        self.speed = speed
        self.stepper.setSpeed(self.speed)
        #self.newSpeed = 10
        #self.active = 0
        #self.speedType = 0
        #self.directionType = 0
        self.q = Queue(maxsize=0)
	self.exit = 0
	self.id = id

    def exit(self):
	self.exit = 1

    def reset(self):
        #self.directionType = 0
        #self.speedType = 0
        self.q.put((0, self.direction, CONST_SPEED_DEFAULT))
        #self.speed = CONST_SPEED_DEFAULT
        #self.pos = 0

    def getPositionType(self, pos):
        if(self.pos < pos):
            return 1
        else:
            return 2

    def setPosition(self, pos, dir):
        self.q.put((pos, dir, self.speed))
        #self.newPos = pos
        #self.active = 1

    def getSpeedType(self, speed):
        if(self.speed < speed):
           return 1
        else:
           return 2

    def setSpeed(self, speed):
        self.q.put((self.pos, self.direction, speed))
        #self.seepdType = getSpeedType(speed)
        #self.newSpeed = speed
        #self.active = 1

    def set(self, pos, direction, speed):
        self.q.put((pos, direction, speed))
        return

    def step(self, numbers):
        print("do nothing")
        # stepper.step(numsteps, direction, style)

    def run(self):

	while not self.q.empty():
		#active = 0
		#print("newPos " + str(self.newPos))
		#print("newSpeed " + str(self.newSpeed))
		#print("speed " + str(self.speed))
		#print("speedType " + str(self.speedType))
		#self.directionType = self.getPositionType(self.pos)
		#print("pos " + str(self.pos))
		#print("directionType " + strself.directionType))
		item = self.q.get()
		self.pos = item[0]
		self.direction = item[1]
		newSpeed = item[2]
		with verrou:
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



myStepper1 = mh.getStepper(100, 1)    # 200 steps/rev, motor port #1
myStepper2 = mh.getStepper(100, 2)    # 200 steps/rev, motor port #2

# Création des threads
thread_1 = Stepper(myStepper1, "stepper1", Adafruit_MotorHAT.BACKWARD, CONST_SPEED_DEFAULT, 1)
thread_2 = Stepper(myStepper2, "stepper2", Adafruit_MotorHAT.BACKWARD, CONST_SPEED_DEFAULT, 2)

#tambour (thread1)
#thread_1.set(200,Adafruit_MotorHAT.FORWARD, CONST_SPEED_DEFAULT)
#thread_2.setPosition(50,Adafruit_MotorHAT.BACKWARD)
#thread_1.reset()
#thread_1.set(20, Adafruit_MotorHAT.FORWARD, CONST_SPEED_DEFAULT)

#thread_2.setPosition(100,Adafruit_MotorHAT.FORWARD)
#thread_1.set(300,Adafruit_MotorHAT.BACKWARD, CONST_SPEED_DEFAULT)
#sys.exit()
myStepper1.setSpeed(50)
myStepper2.setSpeed(50)

megaloop = 1
while(megaloop):
	loop = 10
	#glissiere (thread 2)
	while(loop):
		myStepper1.step(2, Adafruit_MotorHAT.FORWARD, Adafruit_MotorHAT.DOUBLE)
		myStepper2.step(randint(30,150), Adafruit_MotorHAT.BACKWARD, Adafruit_MotorHAT.DOUBLE)
		myStepper1.step(2, Adafruit_MotorHAT.FORWARD, Adafruit_MotorHAT.DOUBLE)
		myStepper2.step(randint(30,150), Adafruit_MotorHAT.FORWARD, Adafruit_MotorHAT.DOUBLE)
		#thread_1.set(20,Adafruit_MotorHAT.FORWARD, CONST_SPEED_DEFAULT)
		#thread_2.set(40,Adafruit_MotorHAT.BACKWARD, CONST_SPEED_DEFAULT)
		#thread_1.set(20,Adafruit_MotorHAT.FORWARD, CONST_SPEED_DEFAULT)
		#thread_2.set(40,Adafruit_MotorHAT.FORWARD, CONST_SPEED_DEFAULT)
		loop = loop-1
	#myStepper1.step(32, Adafruit_MotorHAT.BACKWARD, Adafruit_MotorHAT.DOUBLE)
	#myStepper2.step(40, Adafruit_MotorHAT.FORWARD, Adafruit_MotorHAT.DOUBLE)
	#thread_1.set(160,Adafruit_MotorHAT.BACKWARD, CONST_SPEED_DEFAULT)
	#thread_2.set(40,Adafruit_MotorHAT.FORWARD, CONST_SPEED_DEFAULT)
	megaloop = megaloop - 1

# Lancement des threads
thread_1.start()
thread_2.start()

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
