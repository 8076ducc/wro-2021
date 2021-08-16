#!/usr/bin/env pybricks-micropython
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
import calibrate.py

car_order = []
        
def brake():
    left_motor.brake()
    right_motor.brake()

# Write your program here.
ev3.speaker.beep()
gyro_sensor.reset_angle(0)

detect_cars()
