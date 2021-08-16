from pybricks.hubs import EV3Brick
import pybricks.ev3devices
from pybricks.ev3devices import (Motor, TouchSensor,
                                 InfraredSensor, UltrasonicSensor, GyroSensor)
import pybricks.nxtdevices
from pybricks.parameters import Port, Stop, Direction, Button, Color
from pybricks.tools import wait, StopWatch, DataLog
from pybricks.robotics import DriveBase
from pybricks.media.ev3dev import SoundFile, ImageFile
from pybricks.iodevices import Ev3devSensor

import declarations.py

# calibrate left color sensor
def left_color_cali():
    while True:
        ev3.screen.print(left_color_sensor.reflection(), sep='', end='\n')
        
# calibrate right color sensor
def right_color_cali():
    while True:
        ev3.screen.print(right_color_sensor.reflection(), sep='', end='\n')

# calibrate hitechnic color sensor
def ht_color_cali():
    while True:
        r, g, b, a = ht_color_sensor.read('RGB')
        ev3.screen.print('R: {0}\t G: {1}\t B: {2}'.format(r, g, b), sep='', end='\n')
