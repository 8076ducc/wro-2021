#!/usr/bin/env pybricks-micropython
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
import pid
import calibrate


def start():

    while declarations.gyro_sensor.angle() > -28:
        declarations.right_motor.run(800)

    brake()

    pid.pid_color(50, 800, 2, 10)


def detect_cars():

    declarations.right_motor.reset_angle(0)

    kp = 0.07
    ki = 0.000
    kd = 0.8

    proportional = 0.0
    integral = 0.0
    derivative = 0.0

    last_error = 0.0
    error = 0.0

    loop = 0

    threshold = 32
    speed = 200

    while len(declarations.car_order) < 5:

        reading = declarations.left_color_sensor.reflection()

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

        if declarations.right_motor.angle() > 120:

            color = None

            if 60 < declarations.ht_color_sensor.read("RGB")[0]:
                print(declarations.ht_color_sensor.read("RGB"))
                color = Color.RED
            elif 60 < declarations.ht_color_sensor.read("RGB")[2]:
                print(declarations.ht_color_sensor.read("RGB"))
                color = Color.BLUE
            else:
                print(declarations.ht_color_sensor.read("RGB"))
                color = Color.GREEN

            declarations.car_order.append(color)

            print(color)

            if color == Color.BLUE:
                # blue
                declarations.ev3.speaker.beep(frequency=600, duration=100)
            elif color == Color.GREEN:
                # green
                declarations.ev3.speaker.beep(frequency=700, duration=100)
            elif color == Color.RED:
                # red
                declarations.ev3.speaker.beep(frequency=800, duration=100)

            declarations.right_motor.reset_angle(0)

    brake()
    print(declarations.car_order)


def brake():
    declarations.left_motor.brake()
    declarations.right_motor.brake()


# Write your program here.
declarations.ev3.speaker.beep()
declarations.gyro_sensor.reset_angle(0)

# start()
detect_cars()
