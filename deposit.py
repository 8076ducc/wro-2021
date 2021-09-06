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


def deposit(motor: Motor, angle: int):

    base.reset_angle()
    line_track.move(right_color_sensor, 200, 50, -1, lambda: base.angle() < 130)
    gyro_turn.turn(angle)

    base.reset_angle()
    gyro_straight.move(-500, angle, lambda: base.angle() < 130)

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

    gyro_turn.single_motor_turn(angle - 90, 0, 0)


def deposit_without_battery(motor: Motor, angle: int):

    base.reset_angle()
    line_track.move(right_color_sensor, 200, 50, -1, lambda: base.angle() < 130)
    gyro_turn.turn(angle)

    base.reset_angle()
    gyro_straight.move(-500, angle, lambda: base.angle() < 130)

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

    gyro_turn.single_motor_turn(angle - 90, 0, 0)


def collect(motor: Motor, angle: int, car_color: Color):

    base.reset_angle()

    if motor == left_intake:
        line_track.move(right_color_sensor, 500, 50, -1, lambda: base.angle() < 170)
    elif motor == right_intake:
        line_track.move(right_color_sensor, 500, 50, -1, lambda: base.angle() < 90)

    gyro_turn.turn(angle)

    if motor == left_intake:
        intake.open_left()
        gyro_straight.move(-500, angle, lambda: right_color_sensor.reflection() > 30)
        base.brake()
        intake.close_left()
        left_intake_possessions.update(car_color, 1)
        gyro_straight.move(800, angle, lambda: right_color_sensor.reflection() < 70)
        gyro_straight.move(800, angle, lambda: right_color_sensor.reflection() > 20)
    elif motor == right_intake:
        intake.open_right()
        gyro_straight.move(-500, angle, lambda: left_color_sensor.reflection() > 30)
        base.brake()
        intake.close_right()
        right_intake_possessions.update(car_color, 1)
        gyro_straight.move(800, angle, lambda: left_color_sensor.reflection() < 70)
        gyro_straight.move(800, angle, lambda: left_color_sensor.reflection() > 20)

    gyro_turn.single_motor_turn(angle - 90, 0, 0)
