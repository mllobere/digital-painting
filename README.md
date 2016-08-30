Digital Painting!
===================

Intro
--------
I am starting this project which has been in my head for a long time now. I like drawing/painting, and am also a software developper, I always thought it could be a good idea to combine the real world of painting with the quite mechanic side of the computer world. 

Ideas behind 
------------------

This project is going to be built along a certain line of action :

 - I'd like the result to be graphically attractive (to my own definition of 'attractive')
 - I'd like the result to be easily repeatable. Meaning that I should be able to reproduce a result I like, this way I can create series of paints.
 - I'd like to build stuff. A drawing machine of some sort should be used.
 
Existing
-----------
Drawing machines are quite common around the web, it is not in the frame of this project to be unique. I would like to avoid any kind of 2/3 axes machine whether that be on a horizontal or vertical plane. 

Some thoughts/ideas
------------------------------

 - The machine could be connected to internet. This way, we could create a community painting. A person could give and order to the machine via a website, after X orders, the painting would be finish.  
 - We could potentially create multiple machines that would give different results
 - Various sources of input : API (GPS, google search, weather), Video/Audio flow (e.g Movie), user

Machine 1
------------

#### - Material
 - Raspberry Pi 
 - Nema 17
 - HAT
 - Wooood

#### - Flow

```flow
st=>start: Internet
e=>end: Result
op=>operation: Raspberry
op2=>operation: Machine

st->op->op2->e
```
