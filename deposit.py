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


def deposit_waiting(motor: Motor, angle: int):

    base.reset_angle()
    line_track.move(right_color_sensor, 200, 50, -1, lambda: base.angle() < 130)
    gyro_turn.turn(angle)

    base.reset_angle()
    gyro_straight.move(-500, angle, lambda: base.angle() > -130)

    if motor == left_intake:
        intake.open_side(left_intake)
        left_intake_possessions.update(None, None, False)
    elif motor == right_intake:
        intake.open_side(right_intake)
        right_intake_possessions.update(None, None, False)

    wait(300)

    line_track.move(
        right_color_sensor, 800, 50, 1, lambda: left_color_sensor.reflection() > 20
    )

    if motor == left_intake:
        intake.close_side(left_intake)
    elif motor == right_intake:
        intake.close_side(right_intake)

    wait(300)

    intake.hold()

    # TODO: Move further back

    gyro_turn.single_motor_turn(angle - 90, 0, 0)


def deposit_waiting_without_battery(motor: Motor, angle: int):

    base.reset_angle()
    line_track.move(right_color_sensor, 200, 50, -1, lambda: base.angle() < 130)
    gyro_turn.turn(angle)

    base.reset_angle()
    gyro_straight.move(-500, angle, lambda: base.angle() > -130)

    if motor == left_intake:
        intake.open_side(left_intake)
        left_intake_possessions.update(None, None)
    elif motor == right_intake:
        intake.open_side(right_intake)
        right_intake_possessions.update(None, None)

    wait(300)

    line_track.move(
        right_color_sensor, 800, 50, 1, lambda: left_color_sensor.reflection() > 20
    )

    if motor == left_intake:
        intake.close_side(left_intake)
    elif motor == right_intake:
        intake.close_side(right_intake)

    wait(300)

    intake.hold()

    # TODO: Move further back

    gyro_turn.single_motor_turn(angle - 90, 0, 0)


def collect_parked(motor: Motor, angle: int, car_color: Color):

    base.reset_angle()

    if motor == left_intake:
        line_track.move(right_color_sensor, 500, 50, -1, lambda: base.angle() < 90)
        sensor = right_color_sensor
    elif motor == right_intake:
        line_track.move(right_color_sensor, 500, 50, -1, lambda: base.angle() < 10)
        sensor = left_color_sensor

    gyro_turn.turn(angle)

    intake.open_side(motor)
    gyro_straight.move(-900, angle, lambda: sensor.reflection() > 30)
    gyro_straight.move(-900, angle, lambda: sensor.reflection() < 70)
    gyro_straight.move(-900, angle, lambda: sensor.reflection() > 30)
    gyro_straight.move(-900, angle, lambda: sensor.reflection() < 70)
    gyro_straight.move(-900, angle, lambda: sensor.reflection() > 30)
    base.brake()
    wait(500)
    intake.close_side(motor)
    wait(800)
    left_intake_possessions.update(car_color, 1)
    gyro_straight.move(900, angle, lambda: sensor.reflection() < 70)
    gyro_straight.move(900, angle, lambda: sensor.reflection() > 20)
    gyro_straight.move(900, angle, lambda: sensor.reflection() < 70)

    gyro_turn.turn(angle - 95)
