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
from constants import *


def start():

    gyro_sensor.reset_angle(0)

    base.move(800, 800)
    intake.close()
    wait(250)
    gyro_turn.turn(-8)
    gyro_straight.move(800, -8, lambda: left_color_sensor.reflection() > 20)
    gyro_straight.move(800, -8, lambda: left_color_sensor.reflection() > 40)
    intake.run(0, 0)
    base.move(800, 800)
    wait(65)

    gyro_turn.turn(-90)

    intake.open()
    base.move(-800, -800)
    wait(600)
    base.brake()
    intake.stop()
    intake.close()
    wait(600)
    intake.stop()
    intake.hold()

    left_intake_possessions.update(battery=True)
    right_intake_possessions.update(battery=True)
    gyro_turn.single_motor_turn(-36, 1, 0)
    gyro_turn.single_motor_turn(-90, 0, 1)

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

    while len(car_order) < 6:

        reading = right_color_sensor.rgb()[2]

        error = threshold - reading
        proportional = error * kp
        integral += error
        derivative = (error - last_error) * kd

        correction = (integral * ki) + proportional + derivative
        if loop < 100:
            base.move(200 - (correction * 10), 200 + (correction * 10))
        else:
            base.move(speed - (correction * 10), speed + (correction * 10))

        last_error = error

        if ht_color_sensor.read("RGB")[0] > red_waiting[0]:
            color = Color.RED
        elif (
            ht_color_sensor.read("RGB")[2] > blue_waiting[2]
            and ht_color_sensor.read("RGB")[1] < blue_waiting[1]
        ):
            color = Color.BLUE
        elif (
            ht_color_sensor.read("RGB")[1] > green_waiting[1]
            and ht_color_sensor.read("RGB")[2] > green_waiting[2]
        ):
            color = Color.GREEN
        else:
            color = None

        if color != None and color != last_color:

            car_order.append(color)
            print(ht_color_sensor.read("RGB"))
            print(color)
            ev3.speaker.beep()

        last_color = color

        loop += 1

    base.brake()
    print(car_order)

    gyro_straight.move(-400, -90, lambda: left_color_sensor.reflection() < 70)

    base.brake()
    wait(50)

    gyro_turn.single_motor_turn(10, 1, 0)
    gyro_turn.single_motor_turn(-95, 0, 1)
    gyro_turn.single_motor_turn(0, 1, 0)

    intake.open()

    base.reset_angle()
    gyro_straight.move(-900, 0, lambda: base.angle() > -600)

    intake.close()
    wait(500)
    intake.hold()

    left_intake_possessions.update(car_order[0], 0)
    right_intake_possessions.update(car_order[1], 1)

    wait(50)

    gyro_straight.move(700, 0, lambda: left_color_sensor.reflection() < 70)
    gyro_straight.move(700, 0, lambda: left_color_sensor.reflection() > 20)

    base.brake()

    gyro_turn.single_motor_turn(110, 1, 0)
    gyro_turn.single_motor_turn(0, 0, 1)


def detect_parking():
    def move():
        line_track.move(
            right_color_sensor,
            500,
            (black_right + white_right / 2),
            -1,
            lambda: left_color_sensor.reflection() > (black_left + 5),
        )
        line_track.move(
            right_color_sensor,
            300,
            (black_right + white_right / 2),
            -1,
            lambda: left_color_sensor.reflection() < (white_left - 5),
        )
        base.brake()
        wait(100)

    move()
    check_parking_lot(4)

    move()
    check_parking_lot(5)

    move()
    check_parking_lot(6)

    move()
    check_parking_lot(7)

    # go back

    gyro_turn.turn(193)
    base.move(-600, -250)
    wait(1300)

    base.brake()
    wait(50)

    check_parking_lot(3)

    move()
    check_parking_lot(2)

    move()
    check_parking_lot(1)

    move()
    check_parking_lot(0)


def check_parking_lot(parking_lot: int):

    parked_color = None

    norm_reading = ht_color_sensor.read("NORM")
    raw_reading = ht_color_sensor.read("RAW")
    rgb_reading = ht_color_sensor.read("RGB")
    color_reading = ht_color_sensor.read("COLOR")

    if raw_reading[0] > 3000 and color_reading[0] != 0:
        parked_color = Color.YELLOW
        ev3.speaker.beep(frequency=500, duration=100)
    elif (
        color_reading[0] == 1
        or color_reading[0] == 5
        or color_reading[0] == 7
        or color_reading[0] == 14
    ):
        parked_color = Color.RED
        ev3.speaker.beep(frequency=600, duration=100)
    elif color_reading[0] == 2 or color_reading[0] == 3 or color_reading[0] == 11:
        parked_color = Color.BLUE
        ev3.speaker.beep(frequency=700, duration=100)
    elif color_reading[0] == 4 or color_reading[0] == 12 or color_reading[0] == 13:
        parked_color = Color.GREEN
        ev3.speaker.beep(frequency=800, duration=100)

    print(parked_color)
    print(norm_reading)
    print(raw_reading)
    print(rgb_reading)
    print(color_reading)
    print(" ")

    if parked_color == Color.YELLOW:
        parking_lots[parking_lot].update(None, None, True)
    elif parked_color != None:
        parking_lots[parking_lot].update(parked_color, 1, False)
    else:
        parking_lots[parking_lot].update(None, None, False)

    if 4 <= parking_lot <= 11:
        angle = 90
    elif 0 <= parking_lot <= 3:
        angle = 270

    if (
        parking_lots[parking_lot].parked_color == None
        and parking_lots[parking_lot].barrier == False
    ):
        if (
            left_intake_possessions.car_color == parking_lots[parking_lot].color
            and left_intake_possessions.car_type == 0
        ):
            if (
                left_intake_possessions.car_color == Color.RED
                and left_intake_possessions.battery == True
            ):
                deposit_waiting_without_battery(left_intake, angle)
            else:
                deposit_waiting(left_intake, angle)
        elif (
            right_intake_possessions.car_color == parking_lots[parking_lot].color
            and right_intake_possessions.car_type == 0
        ):
            if (
                right_intake_possessions.car_color == Color.RED
                and right_intake_possessions.battery == True
            ):
                deposit_waiting_without_battery(right_intake, angle)
            else:
                deposit_waiting(right_intake, angle)
    elif (
        parking_lots[parking_lot].parked_type == 1
        and parking_lots[parking_lot].barrier == False
    ):
        if left_intake_possessions.car_type == None:
            collect_parked(left_intake, angle, parking_lots[parking_lot].color)
        elif right_intake_possessions.car_type == None:
            collect_parked(right_intake, angle, parking_lots[parking_lot].color)


def deposit_parked():
    line_track.move(
        right_color_sensor,
        800,
        (black_right + white_right / 2),
        -1,
        lambda: right_color_sensor.reflection() < 30,
    )
    gyro_turn.single_motor_turn(260, 1, 0)

    line_track.move(
        right_color_sensor, 800, 50, -1, lambda: left_color_sensor.reflection() > 20
    )
    gyro_turn.single_motor_turn(360, 0, 1)
    gyro_straight.move(
        -800, 360, lambda: left_color_sensor.reflection() < (white_left - 5)
    )
    gyro_straight.move(
        -800, 360, lambda: left_color_sensor.reflection() > (black_left + 5)
    )
    gyro_straight.move(
        -800, 360, lambda: left_color_sensor.reflection() < (white_left - 5)
    )
    intake.open_side(left_intake)
    wait(800)
    gyro_straight.move(
        800, 360, lambda: left_color_sensor.reflection() > (black_left + 5)
    )
    left_intake_possessions.update(None, None)

    gyro_turn.single_motor_turn(240, 0, 1)

    gyro_turn.single_motor_turn(360, 1, 0)
    gyro_straight.move(
        -800, 360, lambda: left_color_sensor.reflection() < (white_left - 5)
    )
    gyro_straight.move(
        -800, 360, lambda: left_color_sensor.reflection() > (black_left + 5)
    )
    gyro_straight.move(
        -800, 360, lambda: left_color_sensor.reflection() < (white_left - 5)
    )
    intake.open_side(right_intake)
    wait(800)
    gyro_straight.move(
        800, 360, lambda: left_color_sensor.reflection() > (black_left + 5)
    )
    right_intake_possessions.update(None, None)


# Write your program here.

start()
detect_waiting()
detect_parking()
deposit_parked()

# while True:
#     print(right_color_sensor.reflection())

ev3.speaker.beep()
