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

    # TODO: Move forwards

    if motor == left_intake:
        intake.open_left()
        left_intake_possessions.update(None, None, False)
    elif motor == right_intake:
        intake.open_right()
        right_intake_possessions.update(None, None, False)

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


def deposit_without_battery(motor: Motor):

    # TODO: Move forwards

    if motor == left_intake:
        intake.open_left()
        left_intake_possessions.update(None, None)
    elif motor == right_intake:
        intake.open_right()
        right_intake_possessions.update(None, None)

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


def collect(motor: Motor, car_color: Color):
    print(1)

    if motor == left_intake:
        intake.open_left()
    elif motor == right_intake:
        intake.open_right()

    if motor == left_intake:
        intake.close_left()
        left_intake_possessions.update(car_color, 1)
    elif motor == right_intake:
        intake.close_right()
        right_intake_possessions.update(car_color, 1)
