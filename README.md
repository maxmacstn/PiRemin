# PiRemin
A simple digital Theremin made with a Raspberry Pi 3.

![PyRemin](https://raw.githubusercontent.com/maxmacstn/PiRemin/master/image/25401007_1315512725261800_1709378387_o.jpg?token=AS27ie08lYi54f9JURXos3gUuV-4BCFVks5aPIjewA%3D%3D)

## Features
- Real time frequency and amplitude adjustment using the distance between your hands and the sensors. 
- Real time adjustment through GUI as well.
- Real time sensor value display.
- LED Visualizer displays current output frequency.

## Developers
- [MaxMac_STN](https://github.com/maxmacstn) - GUI design/code and hardware developer.
- [Tobalation](https://github.com/Tobalation) - Sound generator code and some GUI/main application code.

## Hardware
 ![Wiring Diagram](https://raw.githubusercontent.com/maxmacstn/PiRemin/master/Documents/Wiring_diagram.jpg?token=AS27iTipPu10rgxhW6AnryV6pd5lf5zOks5aPIoUwA%3D%3D)
- 2 HC-SR04 Ultra-sonic sensor
- WS2812b RGB Strip + Logic level converter
- Raspberry Pi 3

## Software
 ![GUI Screenshot](https://raw.githubusercontent.com/maxmacstn/PiRemin/master/image/25353382_10210475680120549_1177331904_o.png?token=AS27ifzOrwcOUgBJHtLnM4jYbMHcGoUOks5aPIrxwA%3D%3D)
- Python 3 + TKInter
- ARM v7 Assembly (For ultrasonic status LED)

## Dependencies
- LEDVisualizer controller - [rpi_ws281x](https://github.com/jgarff/rpi_ws281x)
- Sound Generator - [PyAudio](https://people.csail.mit.edu/hubert/pyaudio/)
- Sound Generator - [NumPy](http://www.numpy.org/)
- Ultrasonic sensor library - [hcsr04sensor](https://github.com/alaudet/hcsr04sensor)

## Video
- [Youtube Link](https://youtu.be/xfLoMbNUBvE)
