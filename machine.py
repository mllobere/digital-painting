#!/usr/bin/python
# -*- coding: iso-8859-15 -*-
import Tkinter
import time
from threading import Thread, RLock
import random
import sys
import Queue
from Adafruit_MotorHAT import Adafruit_MotorHAT, Adafruit_DCMotor, Adafruit_StepperMotor
import atexit
from Queue import Queue

rand = random.Random(  )


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

class Stepper(Thread):

    def __init__(self, stepper, name, direction, speed):
        Thread.__init__(self)
        self.stepper = stepper
        self.pos = 0
	self.newPos = 0
        self.direction = direction
        self.style = Adafruit_MotorHAT.DOUBLE
	self.name = name
	self.speed = speed
	self.stepper.setSpeed(self.speed)
	self.newSpeed = 10
        self.active = 0
	self.speedType = 0
        self.directionType = 0
	self.q = Queue(maxsize=0)

    def reset():
        self.directionType = 0
	self.speedType = 0
	self.speed = 10
        self.pos = 0

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

    def set(self, pos, speed, direction):
	return
	
    def step(self, numbers):
        print("do nothing")
        # stepper.step(numsteps, direction, style)

    def run(self): 
	while not self.q.empty():   
	    active = 0
            #print("newPos " + str(self.newPos))
            #print("newSpeed " + str(self.newSpeed))
            #print("speed " + str(self.speed))
            #print("speedType " + str(self.speedType))
	    #self.directionType = self.getPositionType(self.pos)
            print("pos " + str(self.pos))
            print("directionType " + str(self.directionType))
	    item = self.q.get()            
	    self.pos = item[0]
	    self.direction = item[1]
	    self.speed = item[2]
	    #while(self.newPos > self.pos or self.newSpeed > self.speed or self.newSpeed < self.speed):            
            while(self.pos > 1 or self.speed > 1):
	        print("dir " + str(self.direction))
		if(self.pos > 1):
			self.stepper.step(1, self.direction, self.style)
			self.pos = self.pos - 1	   	
		if(self.speed > 1):
			self.stepper.setSpeed(self.speed)
			self.speed = self.speed - 1	       
			
    
myStepper1 = mh.getStepper(100, 1)    # 200 steps/rev, motor port #1
myStepper2 = mh.getStepper(100, 2)    # 200 steps/rev, motor port #2

# Création des threads
thread_1 = Stepper(myStepper1, "stepper1", Adafruit_MotorHAT.BACKWARD, 10)
thread_2 = Stepper(myStepper2, "stepper2", Adafruit_MotorHAT.BACKWARD, 10)

thread_1.setPosition(100,Adafruit_MotorHAT.BACKWARD)
thread_1.setPosition(50, Adafruit_MotorHAT.FORWARD)
#thread_1.setSpeed(200)
#thread_2.setPosition(80,Adafruit_MotorHAT.FORWARD)
#thread_2.setPosition(80,Adafruit_MotorHAT.BACKWARD)
#thread_2.setSpeed(300)

# Lancement des threads
thread_1.start()
thread_2.start()

# Attend que les threads se terminent
thread_1.join()
thread_2.join()

 #  if(self.newPos > self.pos and self.directionType == 1):
 #                   print("run +" + self.name)
 #                   self.stepper.step(1, self.direction, self.style)
 #                   self.pos = self.pos + 1 
 #		    active = 1
#	        elif(self.newPos < self.pos and self.directionType == 2):
 #                   print("run -" + self.name)
 #                   self.stepper.step(1, self.direction, self.style)
 #                   self.pos = self.pos - 1 
 #		    active = 1