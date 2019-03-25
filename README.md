# picademy

In this repository you will find some examples of Python scripts for Raspberry Pi 3.
These are examples of my hands-on training for Raspberry.

gpio
--------

Some simple examples for GPIO programming. Detecting button press, LED, some play with pull_up/pull_down GPIO pin state,...
Simply speaking, nothing advanced, just basics.

sensehat
--------

Here are examples for Sense HAT for Raspberry Pi 3, divided into two categories: simple and advanced. 

**simple** 

like the name suggests, some basic things...good for the start and first touch with Sense HAT. 
You can find here examples for LED matrix, text scrolling, reading data from sensors, joystick manipulation.
 
**advanced** 

since I get familiar with the basics, I wanted to do something more complex, more object oriented. 
When your project gets more and more complex, you will notice that having everything handled in single loop in main
is a problem. This is the point when you start thinking about dividing your project into smaller, self managed 
components. Now the only job of the main loop in your program is push the machinery to life :)
The goal was to write simple game displayed on the LED matrix and as the input for movement I wanted to use gyroscope (IMU sensors).
In this folder you will find some examples of trying different things: bouncing pixels reflecting from the edge of the screen,
collision detection, the first try for the game...     
 
