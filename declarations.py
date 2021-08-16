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

ev3 = EV3Brick()

left_motor = Motor(Port.B)
right_motor = Motor(Port.C, Direction.COUNTERCLOCKWISE)
left_intake = Motor(Port.A)
right_intake = Motor(Port.D)

# nxt_color_sensor = pybricks.nxtdevices.ColorSensor(Port.S1)
ht_color_sensor = Ev3devSensor(Port.S1)
left_color_sensor = pybricks.ev3devices.ColorSensor(Port.S2)
right_color_sensor = pybricks.ev3devices.ColorSensor(Port.S3)
gyro_sensor = GyroSensor(Port.S4)