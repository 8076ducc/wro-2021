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
from deposit import *
import constants


def start():

    gyro_sensor.reset_angle(0)

    base.run(800, 800)
    intake.close()
    wait(250)
    gyro_turn.turn(-8)
    gyro_straight.move(800, -8, lambda: left_color_sensor.reflection() > 20)
    gyro_straight.move(800, -8, lambda: left_color_sensor.reflection() > 40)
    intake.run(0, 0)
    base.run(800, 800)
    wait(65)

    gyro_turn.turn(-90)

    intake.open()
    base.run(-800, -800)
    wait(600)
    base.stop()
    intake.stop()
    intake.close()
    wait(600)
    intake.stop()
    intake.hold()

    left_intake_possessions.update(battery=True)
    right_intake_possessions.update(battery=True)
    gyro_turn.single_motor_turn(-36, 200, 0)
    gyro_turn.single_motor_turn(-90, 0, 200)

    # 15 31 11


def detect_waiting():

    kp = 0.2
    ki = 0.0003
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
        elif (
            ht_color_sensor.read("RGB")[2] > constants.blue_waiting[2]
            and ht_color_sensor.read("RGB")[1] < constants.blue_waiting[1]
        ):
            color = Color.BLUE
        elif (
            ht_color_sensor.read("RGB")[1] > constants.green_waiting[1]
            and ht_color_sensor.read("RGB")[2] > constants.green_waiting[2]
        ):
            color = Color.GREEN
        else:
            color = None

        if color != None and color != last_color:

            constants.car_order.append(color)
            print(ht_color_sensor.read("RGB"))
            print(color)
            ev3.speaker.beep()

        last_color = color

        loop += 1

    base.stop()
    print(constants.car_order)

    gyro_straight.move(-400, -90, lambda: left_color_sensor.reflection() < 70)

    base.stop()
    wait(50)

    gyro_turn.single_motor_turn(10, 0, 0)
    gyro_turn.single_motor_turn(-90, 0, 0)
    gyro_turn.single_motor_turn(0, 0, 0)

    intake.open()

    left_motor.reset_angle(0)
    gyro_straight.move(-900, 0, lambda: left_motor.angle() > -600)

    intake.close()
    wait(500)
    intake.hold()

    left_intake_possessions.update(constants.car_order[0], 0)
    right_intake_possessions.update(constants.car_order[1], 1)

    wait(50)

    gyro_straight.move(700, 0, lambda: left_color_sensor.reflection() < 70)
    gyro_straight.move(700, 0, lambda: left_color_sensor.reflection() > 20)

    base.stop()


def detect_parking():
    def move():
        line_track.move(
            right_color_sensor, 500, 50, -1, lambda: left_color_sensor.reflection() > 20
        )
        line_track.move(
            right_color_sensor, 500, 50, -1, lambda: left_color_sensor.reflection() < 70
        )
        base.stop()
        wait(50)

    move()
    check_parking_lot(4)

    move()
    check_parking_lot(5)

    move()
    check_parking_lot(6)

    move()
    check_parking_lot(7)

    # TODO: insert 180º turn to go back

    gyro_turn.turn(180)
    base.run(-200, -700)
    base.run(-700, 0)

    wait(1000)

    move()
    check_parking_lot(3)

    move()
    check_parking_lot(2)

    move()
    check_parking_lot(1)

    move()
    check_parking_lot(0)


def check_parking_lot(parking_lot: int):

    reading = ht_color_sensor.read("RGB")

    if reading[3] < 5 or reading[0] == 0 or reading[1] == 0 or reading[2] == 0:
        parked_color = None
    elif reading[3] > 60:
        parked_color = Color.YELLOW
    elif reading[0] > reading[2]:
        parked_color = Color.RED
    elif reading[2] > reading[0]:
        parked_color = Color.BLUE
    elif reading[1] > 10 and reading[0] < 20 and reading[2] < 20:
        parked_color = Color.GREEN

    if parked_color == Color.YELLOW:
        parking_lots[parking_lot].update(None, None, True)
        print("barrier")
    elif parked_color != None:
        parking_lots[parking_lot].update(parked_color, 1, False)
        print(parked_color)
        ev3.speaker.beep()
    else:
        parking_lots[parking_lot].update(None, None, False)

    print(reading)

    if (
        left_intake_possessions.car_color == parking_lots[parking_lot].color
        and left_intake_possessions.car_type == 0
    ):
        deposit(left_intake)
    elif (
        right_intake_possessions.car_color == parking_lots[parking_lot].color
        and right_intake_possessions.car_type == 0
    ):
        deposit(right_intake)
    elif parking_lots[parking_lot].car_type == 1:
        if left_intake_possessions.car_type == None:
            collect(left_motor, parking_lots[parking_lot].color)
        elif right_intake_possessions.car_type == None:
            collect(right_motor, parking_lots[parking_lot].color)


# Write your program here.

# start()
# detect_waiting()
detect_parking()

# while True:
#     print(ht_color_sensor.read("RGB"))

# while True:
# print(left_color_sensor.reflection())

ev3.speaker.beep()
