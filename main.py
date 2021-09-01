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
from devices import *
from pid import *
from localise import *
import constants


def start():

    gyro_sensor.reset_angle(0)

    base.run(800, 800)
    intake.close()
    wait(250)
    gyro_straight.move(800, -12, lambda: left_color_sensor.reflection() > 20)
    gyro_straight.move(800, -12, lambda: left_color_sensor.reflection() > 40)
    intake.run(0, 0)
    base.run(800, 800)
    wait(45)

    gyro_turn.turn(-90)

    intake.open()
    base.run(-800, -800)
    wait(500)
    base.stop()
    intake.stop()
    intake.close()
    wait(600)
    intake.stop()
    intake.hold()

    left_intake_possessions.update(battery=True)
    right_intake_possessions.update(battery=True)
    gyro_turn.single_motor_turn(-38, 500, 0)
    gyro_turn.single_motor_turn(-90, 0, 500)

    # 15 31 11


def detect_waiting():

    kp = 0.07
    ki = 0.000
    kd = 0.8

    proportional = 0.0
    integral = 0.0
    derivative = 0.0

    last_error = 0.0
    error = 0.0

    threshold = 25
    speed = 400

    color = None
    last_color = None

    loop = 0

    while len(constants.car_order) < 6:

        reading = right_color_sensor.rgb()[2]

        error = threshold - reading
        proportional = error * kp
        integral += error
        derivative = (error - last_error) * kd

        correction = (integral * ki) + proportional + derivative
        if loop < 100:
            base.run(200 - (correction * 10), 200 + (correction * 10))
        else:
            base.run(speed - (correction * 10), speed + (correction * 10))

        last_error = error

        if ht_color_sensor.read("RGB")[0] > constants.red_waiting[0]:
            color = Color.RED
        elif ht_color_sensor.read("RGB")[2] > constants.blue_waiting[2]:
            color = Color.BLUE
        elif ht_color_sensor.read("RGB")[1] > constants.green_waiting[1]:
            color = Color.GREEN
        elif ht_color_sensor.read("RGB")[0] < 10:
            color = None

        if color != None and color != last_color:

            constants.car_order.append(color)
            print(color)

        last_color = color

        loop += 1

    base.stop()
    print(constants.car_order)

    proportional = 0.0
    integral = 0.0
    derivative = 0.0

    last_error = 0.0
    error = 0.0

    threshold = 27
    speed = -450

    color = None
    last_color = None

    if constants.car_order[0] == constants.car_order[5]:
        detect_first_color = -1
    else:
        detect_first_color = 0

    loop = 0

    while detect_first_color < 2:

        reading = right_color_sensor.rgb()[2]

        error = threshold - reading
        proportional = error * kp
        integral += error
        derivative = (error - last_error) * kd

        correction = (integral * ki) + proportional + derivative

        if loop < 100:
            base.run(-200 + (correction * 10), -200 - (correction * 10))
        else:
            base.run(speed + (correction * 10), speed - (correction * 10))

        last_error = error

        if ht_color_sensor.read("RGB")[0] > constants.red_waiting[0]:
            color = Color.RED
        elif ht_color_sensor.read("RGB")[2] > constants.blue_waiting[2]:
            color = Color.BLUE
        elif ht_color_sensor.read("RGB")[1] > constants.green_waiting[1]:
            color = Color.GREEN
        elif ht_color_sensor.read("RGB")[0] < 10:
            color = None

        if color != None and color != last_color and color == constants.car_order[0]:
            detect_first_color += 1
            print(color)

        last_color = color

        loop += 1

    gyro_turn.turn(-45)

    gyro_straight.move(800, -45, lambda: left_color_sensor.reflection() < 70)
    gyro_straight.move(800, -45, lambda: left_color_sensor.reflection() > 20)
    gyro_straight.move(800, -45, lambda: left_color_sensor.reflection() < 70)
    gyro_straight.move(800, -45, lambda: left_color_sensor.reflection() > 40)

    gyro_turn.single_motor_turn(0, -500, 0)
    intake.open()

    left_motor.reset_angle(0)
    gyro_straight.move(-900, 0, lambda: left_motor.angle() > -500)

    intake.close()
    intake.hold()

    base.stop()


def detect_parking():
    line_track.move(
        right_color_sensor, 800, 50, -1, lambda: left_color_sensor.reflection() > 20
    )
    check_parking_lot(4)

    line_track.move(
        right_color_sensor, 800, 50, -1, lambda: left_color_sensor.reflection() > 20
    )
    check_parking_lot(5)

    line_track.move(
        right_color_sensor, 800, 50, -1, lambda: left_color_sensor.reflection() > 20
    )
    check_parking_lot(6)

    line_track.move(
        right_color_sensor, 800, 50, -1, lambda: left_color_sensor.reflection() > 20
    )
    check_parking_lot(7)

    # TODO: insert 180º turn to go back

    line_track.move(
        right_color_sensor, 800, 50, -1, lambda: left_color_sensor.reflection() > 20
    )
    check_parking_lot(3)

    line_track.move(
        right_color_sensor, 800, 50, -1, lambda: left_color_sensor.reflection() > 20
    )
    check_parking_lot(2)

    line_track.move(
        right_color_sensor, 800, 50, -1, lambda: left_color_sensor.reflection() > 20
    )
    check_parking_lot(1)

    line_track.move(
        right_color_sensor, 800, 50, -1, lambda: left_color_sensor.reflection() > 20
    )
    check_parking_lot(0)


def check_parking_lot(parking_lot: int):
    if ht_color_sensor.read("RGB")[2] < constants.red_parked[2]:
        parked_color = Color.RED
    elif ht_color_sensor.read("RGB")[2] > constants.blue_parked[2]:
        parked_color = Color.BLUE
    elif ht_color_sensor.read("RGB")[1] > constants.green_parked[1]:
        parked_color = Color.GREEN
    elif ht_color_sensor.read("RGB")[1] > constants.barrier[1]:
        parked_color = Color.YELLOW
    elif ht_color_sensor.read("RGB")[0] < 5:
        parked_color = None

    if parked_color == Color.YELLOW:
        parking_lots[parking_lot].update(True)
    elif parked_color != None:
        parking_lots[parking_lot].update(False, parked_color, 0)
    else:
        parking_lots[parking_lot].update(False)


# Write your program here.

start()
detect_waiting()

# gyro_sensor.reset_angle(0)
# gyro_straight.move(800, 0, lambda: True)

# line_track.move(left_color_sensor, 500, 50)

# gyro_sensor.reset_angle(0)
# gyro_turn.single_motor_turn(-90, 200, 500)
# gyro_turn.turn(-90)


ev3.speaker.beep()
