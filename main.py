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


def start():

    declarations.gyro_sensor.reset_angle(0)

    right_motor.run(800)
    left_motor.run(800)

    left_intake.run(-500)
    right_intake.run(-500)

    wait(250)

    pid.gyro_straight_color_lower(-10, 800, 2, 20)
    pid.gyro_straight_color_lower(-10, 800, 2, 40)

    left_intake.run(0)
    right_intake.run(0)

    brake()

    right_motor.run(800)
    left_motor.run(800)

    wait(45)

    pid.pid_gyro_turn(-90)

    left_intake.run(1000)
    right_intake.run(1000)

    right_motor.run(-800)
    left_motor.run(-800)

    wait(300)

    left_motor.run(0)
    right_motor.run(0)
    left_intake.run(0)
    right_intake.run(0)

    left_intake.run(-800)
    right_intake.run(-800)

    wait(600)

    left_intake.run(0)
    right_intake.run(0)

    left_intake.hold()
    right_intake.hold()

    pid.gyro_straight_color_higher(-90, 800, 2, 70)
    pid.pid_gyro_turn(-60)
    # pid.gyro_straight_color_higher(-60, 800, 2, 90)
    # pid.gyro_straight_color_lower(-60, 800, 3, 20)


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

        reading = right_color_sensor.rgb()[2]

        error = threshold - reading
        proportional = error * kp
        integral += error
        derivative = (error - last_error) * kd

        correction = (integral * ki) + proportional + derivative

        left_motor.run(speed - (correction * 10))
        right_motor.run(speed + (correction * 10))

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

        reading = right_color_sensor.rgb()[2]

        error = threshold - reading
        proportional = error * kp
        integral += error
        derivative = (error - last_error) * kd

        correction = (integral * ki) + proportional + derivative

        left_motor.run(speed + (correction * 10))
        right_motor.run(speed - (correction * 10))

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
        left_motor.run(500)
        right_motor.run(200)

    declarations.gyro_sensor.reset_angle(0)
    pid.pid_gyro_straight_angle(0, -800, -300)

    brake()


def brake():
    left_motor.brake()
    right_motor.brake()


# Write your program here.

start()

# gyro_sensor.reset_angle(0)
# pid.pid_gyro_turn(90)
# brake()
# gyro_sensor.reset_angle(0)
# pid.pid_gyro_turn(90)
# gyro_sensor.reset_angle(0)
# pid.pid_gyro_turn(90)
# gyro_sensor.reset_angle(0)
# pid.pid_gyro_turn(90)

# while True:
#     print(gyro_sensor.angle())

# calibrate.right_color_cali()

# pid.pid_gyro_straight_angle(0, 200, 0)

# while True:
#     print(declarations.gyro_sensor.angle())

# detect_cars()

# calibrate.right_color_rgb_cali()

# calibrate.ht_color_cali()
