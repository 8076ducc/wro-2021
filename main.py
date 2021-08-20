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

    declarations.gyro_sensor.reset_angle(0)

    # while declarations.gyro_sensor.angle() > -3:
    #     declarations.right_motor.run(900)
    #     declarations.left_motor.run(300)

    declarations.right_motor.run(800)
    declarations.left_motor.run(800)

    wait(300)

    pid.pid_gyro_straight_color(0, 800, 20)

    pid.pid_gyro_straight_color(0, 800, 40)
    brake()

    declarations.right_motor.run(800)
    declarations.left_motor.run(800)

    wait(40)

    pid.pid_gyro_turn(-90)

    declarations.right_motor.run(-800)
    declarations.left_motor.run(-800)

    wait(300)

    declarations.left_intake.run(800)
    declarations.right_intake.run(800)

    wait(200)

    declarations.left_intake.run(0)
    declarations.right_intake.run(0)


def detect_cars():

    kp = 0.07
    ki = 0.000
    kd = 0.8

    proportional = 0.0
    integral = 0.0
    derivative = 0.0

    last_error = 0.0
    error = 0.0

    threshold = 27
    speed = 450

    color = None
    last_color = None

    while len(declarations.car_order) < 6:

        reading = declarations.right_color_sensor.rgb()[2]

        error = threshold - reading
        proportional = error * kp
        integral += error
        derivative = (error - last_error) * kd

        correction = (integral * ki) + proportional + derivative

        declarations.left_motor.run(speed - (correction * 10))
        declarations.right_motor.run(speed + (correction * 10))

        last_error = error

        if declarations.ht_color_sensor.read("RGB")[0] > declarations.red_waiting[0]:
            color = Color.RED
        elif declarations.ht_color_sensor.read("RGB")[2] > declarations.blue_waiting[2]:
            color = Color.BLUE
        elif (
            declarations.ht_color_sensor.read("RGB")[1] > declarations.green_waiting[1]
        ):
            color = Color.GREEN
        elif declarations.ht_color_sensor.read("RGB")[0] < 10:
            color = None

        if color != None and color != last_color:

            declarations.car_order.append(color)

            print(declarations.ht_color_sensor.read("RGB"))
            print(color)

            # if color == Color.BLUE:
            #     # blue
            #     declarations.ev3.speaker.beep(frequency=600, duration=100)
            # elif color == Color.GREEN:
            #     # green
            #     declarations.ev3.speaker.beep(frequency=700, duration=100)
            # elif color == Color.RED:
            #     # red
            #     declarations.ev3.speaker.beep(frequency=800, duration=100)

        last_color = color

    brake()
    print(declarations.car_order)

    proportional = 0.0
    integral = 0.0
    derivative = 0.0

    last_error = 0.0
    error = 0.0

    threshold = 27
    speed = -450

    color = None
    last_color = None

    if declarations.car_order[0] == declarations.car_order[5]:
        detect_first_color = -1
    else:
        detect_first_color = 0

    while detect_first_color < 2:

        reading = declarations.right_color_sensor.rgb()[2]

        error = threshold - reading
        proportional = error * kp
        integral += error
        derivative = (error - last_error) * kd

        correction = (integral * ki) + proportional + derivative

        declarations.left_motor.run(speed + (correction * 10))
        declarations.right_motor.run(speed - (correction * 10))

        last_error = error

        if declarations.ht_color_sensor.read("RGB")[0] > declarations.red_waiting[0]:
            color = Color.RED
        elif declarations.ht_color_sensor.read("RGB")[2] > declarations.blue_waiting[2]:
            color = Color.BLUE
        elif (
            declarations.ht_color_sensor.read("RGB")[1] > declarations.green_waiting[1]
        ):
            color = Color.GREEN
        elif declarations.ht_color_sensor.read("RGB")[0] < 10:
            color = None

        if color != None and color != last_color and color == declarations.car_order[0]:
            detect_first_color += 1
            print(color)

        last_color = color

    while declarations.gyro_sensor.angle() < 84:
        declarations.left_motor.run(500)
        declarations.right_motor.run(200)

    declarations.gyro_sensor.reset_angle(0)
    pid.pid_gyro_straight_angle(0, -800, -300)

    brake()


def brake():
    declarations.left_motor.brake()
    declarations.right_motor.brake()


# Write your program here.

start()
# pid.pid_gyro_straight_angle(0, 200, 0)

# while True:
#     print(declarations.gyro_sensor.angle())

# detect_cars()

# calibrate.right_color_rgb_cali()

# calibrate.ht_color_cali()
