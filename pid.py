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

import declarations.py


def pid_color(threshold: int, speed: int, sensor: int, target: int):
    kp = 0.07
    ki = 0.000
    kd = 0.8

    proportional = 0.0
    integral = 0.0
    derivative = 0.0

    last_error = 0.0
    error = 0.0

    if sensor == 2:
        target_sensor = right_color_sensor
    elif sensor == 3:
        target_sensor = left_color_sensor

    loop = 0

    # while target_sensor.reflection() != target:
    while True:

        if sensor == 2:
            reading = left_color_sensor.reflection()
        elif sensor == 3:
            reading = right_color_sensor.reflection()

        error = threshold - reading
        proportional = error * kp
        integral += error
        derivative = (error - last_error) * kd

        correction = (integral * ki) + proportional + derivative

        if loop <= 400:
            left_motor.run(200 - (correction * 10))
            right_motor.run(200 + (correction * 10))
        else:
            left_motor.run(speed - (correction * 10))
            right_motor.run(speed + (correction * 10))

        last_error = error

        loop += 1


def pid_gyro_straight_angle(threshold: float, speed: float, target: int):
    kp = 0.7
    ki = 0.0
    kd = 0.0

    proportional = 0.0
    integral = 0.0
    derivative = 0.0

    last_error = 0.0
    error = 0.0

    left_motor.reset_angle(0)
    right_motor.reset_angle(0)

    while right_motor.angle() < target:

        error = threshold - gyro_sensor.angle()
        # speed_percentage = 1 - (right_motor.angle() / target)
        proportional = error * kp
        integral += error
        derivative = (error - last_error) * kd

        correction = (integral * ki) + proportional + derivative
        left_motor.run(speed - (correction * 10))
        right_motor.run(speed + (correction * 10))

        last_error = error

    brake()


def brake():
    left_motor.brake()
    right_motor.brake()
