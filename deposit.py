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
from devices import *
from pid import *
import constants


def deposit(motor: Motor):
    if motor == left_intake:
        intake.open_left()
    elif motor == right_intake:
        intake.open_right()

    wait(300)

    if motor == left_intake:
        intake.close_left()
    elif motor == right_intake:
        intake.close_right()

    line_track.move(
        right_color_sensor, 800, 50, 1, lambda: left_color_sensor.reflection() > 20
    )

    intake.hold()
    
    # TODO: Move further back


def deposit_without_battery(motor: Motor):
    if motor == left_intake:
        intake.open_left()
    elif motor == right_intake:
        intake.open_right()

    wait(300)

    line_track.move(
        right_color_sensor, 800, 50, 1, lambda: left_color_sensor.reflection() > 20
    )
    
    if motor == left_intake:
        intake.close_left()
    elif motor == right_intake:
        intake.close_right()
    
    wait(300)

    intake.hold()
    
    # TODO: Move further back
