from pybricks.hubs import EV3Brick
import pybricks.ev3devices
from pybricks.ev3devices import (
    Motor,
    TouchSensor,
    InfraredSensor,
    UltrasonicSensor,
    GyroSensor,
)
import pybricks.nxtdevices
from pybricks.parameters import Port, Stop, Direction, Button, Color
from pybricks.tools import wait, StopWatch, DataLog
from pybricks.robotics import DriveBase
from pybricks.media.ev3dev import SoundFile, ImageFile
from pybricks.iodevices import Ev3devSensor

import declarations


ev3 = declarations.ev3

left_motor = declarations.left_motor
right_motor = declarations.right_motor
left_intake = declarations.left_intake
right_intake = declarations.right_intake

# nxt_color_sensor = pybricks.nxtdevices.ColorSensor(Port.S1)
ht_color_sensor = declarations.ht_color_sensor
left_color_sensor = declarations.left_color_sensor
right_color_sensor = declarations.right_color_sensor
gyro_sensor = declarations.gyro_sensor
