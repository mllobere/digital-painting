Digital Painting!
===================

Intro
--------
I am starting this project which has been in my head for a long time now. I like drawing/painting, and am also a software developper, I always thought it could be a good idea to combine the real world of painting with the electronic/mechanic side of the computer world. 

Ideas behind 
------------------

This project is going to be built along a certain line of action :

 - I'd like the result to be graphically attractive (to my own definition of 'attractive')
 - I'd like the result to be easily repeatable. Meaning that I should be able to reproduce a result I like, this way I can create series of paints.
 - I'd like to build stuff. A drawing machine of some sort should be used.
 
Existing
-----------
Drawing machines are quite common around the web, so it is not in the frame of this project to be unique. I would like to avoid any kind of "flat" 2/3 axes machine whether that be on a horizontal or vertical plane. 

Some thoughts/ideas
------------------------------

 - The machine could be connected to internet. This way, we could create a community painting. A person could give and order to the machine via a website, after X orders, the painting would be finish.  
 - We could potentially create multiple machines that would give different results
 - Various sources of input : API (GPS, google search, weather), Video/Audio flow (e.g Movie), user
 - Machine learning ?

Machine 1
------------

#### - Material
 - Raspberry Pi 
 - Nema 17
 - HAT
 - Wooood

For this machine, we are using the Adafruit DC Hat to control 2 steppers motors. Raspberry Pi is running rasbian and we are coding in python. The machine is using a drum made in metal and a linear axis. For now, I am only using 2 axis, but I might need to add a third axis later on. A belt is running around the drum to make it turn, also another belt is driving the linear axis. 

#### - Flow

```flow
st=>start: Internet
e=>end: Result
op=>operation: Raspberry
op2=>operation: Machine

st->op->op2->e
```
