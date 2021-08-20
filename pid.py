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
        target_sensor = declarations.right_color_sensor
    elif sensor == 3:
        target_sensor = declarations.left_color_sensor

    loop = 0

    while target_sensor.reflection() != target:
        # while True:

        if sensor == 2:
            reading = declarations.left_color_sensor.reflection()
        elif sensor == 3:
            reading = declarations.right_color_sensor.reflection()

        error = threshold - reading
        proportional = error * kp
        integral += error
        derivative = (error - last_error) * kd

        correction = (integral * ki) + proportional + derivative

        if loop <= 400:
            declarations.left_motor.run(200 + (correction * 10))
            declarations.right_motor.run(200 - (correction * 10))
        else:
            declarations.left_motor.run(speed + (correction * 10))
            declarations.right_motor.run(speed - (correction * 10))

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

    declarations.left_motor.reset_angle(0)
    declarations.right_motor.reset_angle(0)

    while declarations.right_motor.angle() < target:

        error = threshold - declarations.gyro_sensor.angle()
        # speed_percentage = 1 - (right_motor.angle() / target)
        proportional = error * kp
        integral += error
        derivative = (error - last_error) * kd

        correction = (integral * ki) + proportional + derivative
        declarations.left_motor.run(speed + (correction * 10))
        declarations.right_motor.run(speed - (correction * 10))

        last_error = error

        print(declarations.gyro_sensor.angle())

    brake()


def gyro_straight_color_lower(
    threshold: float, speed: float, target_sensor: int, target: int
):
    kp = 0.7
    ki = 0.0
    kd = 0.0

    proportional = 0.0
    integral = 0.0
    derivative = 0.0

    last_error = 0.0
    error = 0.0

    if target_sensor == 2:
        sensor = declarations.left_color_sensor
    elif target_sensor == 3:
        sensor = declarations.right_color_sensor

    while sensor.reflection() > target:

        error = threshold - declarations.gyro_sensor.angle()
        proportional = error * kp
        integral += error
        derivative = (error - last_error) * kd

        correction = (integral * ki) + proportional + derivative
        declarations.left_motor.run(speed + (correction * 10))
        declarations.right_motor.run(speed - (correction * 10))

        last_error = error

    brake()


def gyro_straight_color_higher(
    threshold: float, speed: float, target_sensor: int, target: int
):
    kp = 0.7
    ki = 0.0
    kd = 0.0

    proportional = 0.0
    integral = 0.0
    derivative = 0.0

    last_error = 0.0
    error = 0.0

    if target_sensor == 2:
        sensor = declarations.left_color_sensor
    elif target_sensor == 3:
        sensor = declarations.right_color_sensor

    while sensor.reflection() < target:

        error = threshold - declarations.gyro_sensor.angle()
        proportional = error * kp
        integral += error
        derivative = (error - last_error) * kd

        correction = (integral * ki) + proportional + derivative
        declarations.left_motor.run(speed + (correction * 10))
        declarations.right_motor.run(speed - (correction * 10))

        last_error = error

    brake()


def pid_gyro_turn(threshold: float):

    # kp = 0.7
    # ki = 0.002
    # kd = 0.05

    kp = 0.92
    ki = 0.00
    kd = 3.0

    proportional = 0.0
    integral = 0.0
    derivative = 0.0

    last_error = 0.0
    error = 0.0

    while declarations.gyro_sensor.angle() != threshold:
        error = threshold - declarations.gyro_sensor.angle()
        proportional = error * kp
        integral += error
        derivative = (error - last_error) * kd

        correction = (integral * ki) + proportional + derivative

        # if -25 < (correction * 10) < 0:
        #     declarations.left_motor.run(-25)
        #     declarations.right_motor.run(25)
        # elif 0 < (correction * 10) < 25:
        #     declarations.left_motor.run(25)
        #     declarations.right_motor.run(-25)
        # else:
        #     declarations.left_motor.run(correction * 10)
        #     declarations.right_motor.run(-(correction * 10))

        declarations.left_motor.run(correction * 10)
        declarations.right_motor.run(-(correction * 10))

        last_error = error


def brake():
    declarations.left_motor.brake()
    declarations.right_motor.brake()
