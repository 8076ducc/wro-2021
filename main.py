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


gyro_straight = PID_GyroStraight(gyro_sensor)
gyro_turn = PID_GyroTurn(gyro_sensor)
line_track = PID_LineTrack()
sensors = Sensors(ht_color_sensor, left_color_sensor, right_color_sensor, gyro_sensor)


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
    wait(400)
    base.stop()
    intake.stop()
    intake.close()
    wait(600)
    intake.stop()
    intake.hold()

    # left_intake_possessions.update(battery=True)
    # right_intake_possessions.update(battery=True)

    gyro_straight.move(800, -90, lambda: left_color_sensor.reflection() < 90)
    gyro_turn.turn(-65)
    gyro_straight.move(00, -65, lambda: right_color_sensor.color() != Color.GREEN)
    gyro_straight.move(00, -65, lambda: right_color_sensor.color() != Color.WHITE)

    gyro_turn.turn(-90)

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

    threshold = 27
    speed = 450

    color = None
    last_color = None

    while len(constants.car_order) < 6:

        reading = right_color_sensor.rgb()[2]

        error = threshold - reading
        proportional = error * kp
        integral += error
        derivative = (error - last_error) * kd

        correction = (integral * ki) + proportional + derivative

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

            print(ht_color_sensor.read("RGB"))
            print(color)

        last_color = color

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

    while detect_first_color < 2:

        reading = right_color_sensor.rgb()[2]

        error = threshold - reading
        proportional = error * kp
        integral += error
        derivative = (error - last_error) * kd

        correction = (integral * ki) + proportional + derivative

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
        parking_lots[parking_lot].update(True, None, None)
    elif parked_color != None:
        parking_lots[parking_lot].update(False, parked_color, 0)


# Write your program here.

start()
detect_waiting()

# gyro_sensor.reset_angle(0)
# gyro_straight.move(800, 0, lambda: True)

# line_track.move(left_color_sensor, 500, 50)

# while True:
#     print(right_color_sensor.rgb())

# gyro_sensor.reset_angle(0)
# gyro_turn.single_motor_turn(-90, 200, 500)
# gyro_turn.turn(-65)


ev3.speaker.beep()
