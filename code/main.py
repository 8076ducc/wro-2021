#!/usr/bin/env pybricks-micropython
from pybricks.parameters import Color, Button
from pybricks.tools import wait
from devices import *
from pid import *
from localise import *
from deposit import *
from constants import *

car_order = [Color.GREEN, Color.RED, Color.BLUE, Color.RED, Color.BLUE, Color.GREEN]


def start():

    gyro_sensor.reset_angle(0)

    intake.open()
    gyro_turn.turn(-10)
    gyro_straight.move(
        800,
        -10,
        lambda: left_color_sensor.rgb()[0] < (WHITE_RGB_LEFT[0] - 5),
    )
    gyro_straight.move(
        800,
        -10,
        lambda: left_color_sensor.rgb()[0] > (BLACK_RGB_LEFT[0] + 5),
        False,
    )
    gyro_straight.move(
        600,
        -10,
        lambda: left_color_sensor.rgb()[0] < (WHITE_RGB_LEFT[0] - 5),
        False,
    )
    ev3.speaker.beep()
    base.brake()

    # gyro_turn.turn(-90)

    base.run_target(-800, 800, -134, 134)

    base.run(-1500, -1500)
    wait(400)
    base.brake()
    intake.stop()
    intake.close()
    wait(200)
    intake.update_left_possessions(number_of_batteries=1)
    intake.update_right_possessions(number_of_batteries=1)

    gyro_turn.single_motor_turn(-9, 1, 0)
    gyro_turn.single_motor_turn(-90, 0, 1)
    intake.open()
    wait(200)
    base.run(-1500, -1500)
    wait(600)
    base.brake()
    intake.stop()
    intake.close()
    wait(200)
    intake.update_left_possessions(number_of_batteries=2)
    intake.update_right_possessions(number_of_batteries=2)
    gyro_turn.single_motor_turn(-38, 1, 0)
    gyro_turn.single_motor_turn(-90, 0, 1)
    intake.hold()


def collect_waiting_1():

    kp = 0.2
    ki = 0.0003
    kd = 0.8

    proportional = 0.0
    integral = 0.0
    derivative = 0.0

    last_error = 0.0
    error = 0.0

    threshold = 25
    speed = 500

    color = None
    last_color = None

    loop = 100

    while len(car_order) < 11:
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

        if ht_color_sensor.read("RGB")[0] > RED_WAITING[0]:
            color = Color.RED
        elif (
            ht_color_sensor.read("RGB")[2] > BLUE_WAITING[2]
            and ht_color_sensor.read("RGB")[1] < BLUE_WAITING[1]
        ):
            color = Color.BLUE
        elif (
            ht_color_sensor.read("RGB")[1] > GREEN_WAITING[1]
            and ht_color_sensor.read("RGB")[2] > GREEN_WAITING[2]
        ):
            color = Color.GREEN
        else:
            color = None

        if color is not None and color != last_color:

            car_order.append(color)
            print(ht_color_sensor.read("RGB"))
            print(color)
            print("")
            ev3.speaker.beep()

        last_color = color

        loop += 1

    base.brake()
    print(car_order)

    # TODO: make into computed value
    gyro_straight.move(
        -500, -90, lambda: left_color_sensor.rgb()[2] < WHITE_RGB_LEFT[2], True, 0.8
    )

    base.hold()

    gyro_turn.single_motor_turn(6, 1, 0)
    gyro_turn.single_motor_turn(-112, 0, 1)
    gyro_turn.single_motor_turn(0, 1, 0)

    base.hold()

    intake.open()

    base.reset_angle()

    while base.angle() > -550:
        base.run(-900, -1500)

    base.brake()

    intake.close()
    wait(400)

    intake.update_left_possessions(car_order[0], 0)
    intake.update_right_possessions(car_order[1], 0)

    gyro_straight.move(
        1400,
        0,
        lambda: left_color_sensor.rgb()[0] < (WHITE_RGB_LEFT[0] - 5),
    )
    gyro_straight.move(
        1400,
        0,
        lambda: left_color_sensor.rgb()[0] > (BLACK_RGB_LEFT[0] + 5),
        False,
    )

    base.brake()
    intake.hold()

    gyro_turn.single_motor_turn(97, 1, 0)
    gyro_turn.single_motor_turn(0, 0, 1)


def deposit_waiting_1():
    def move():
        line_track.rgb_move(
            right_color_sensor,
            500,
            [
                ((BLACK_RGB_RIGHT[0] + WHITE_RGB_RIGHT[0]) / 2),
                ((BLACK_RGB_RIGHT[0] + WHITE_RGB_RIGHT[0]) / 2),
                ((BLACK_RGB_RIGHT[0] + WHITE_RGB_RIGHT[0]) / 2),
            ],
            -1,
            lambda: left_color_sensor.rgb()[0] > (BLACK_RGB_LEFT[0] + 5),
            200,
        )

        line_track.rgb_move(
            right_color_sensor,
            500,
            [
                ((BLACK_RGB_RIGHT[0] + WHITE_RGB_RIGHT[0]) / 2),
                ((BLACK_RGB_RIGHT[0] + WHITE_RGB_RIGHT[0]) / 2),
                ((BLACK_RGB_RIGHT[0] + WHITE_RGB_RIGHT[0]) / 2),
            ],
            -1,
            lambda: left_color_sensor.rgb()[0] < (WHITE_RGB_LEFT[0] - 5),
            200,
            False,
        )

    move()
    base.brake()
    parking_lot_action(4, 90)

    line_track.rgb_move(
        right_color_sensor,
        500,
        [
            ((BLACK_RGB_RIGHT[0] + WHITE_RGB_RIGHT[0]) / 2),
            ((BLACK_RGB_RIGHT[0] + WHITE_RGB_RIGHT[0]) / 2),
            ((BLACK_RGB_RIGHT[0] + WHITE_RGB_RIGHT[0]) / 2),
        ],
        -1,
        lambda: left_color_sensor.rgb()[0] > (BLACK_RGB_LEFT[0] + 5),
        200,
    )
    base.brake()
    parking_lot_action(5, 90)

    move()
    base.hold()
    parking_lot_action(6, 90)

    move()
    parking_lot_action(7, 90)

    gyro_straight.move(
        -500, 0, lambda: left_color_sensor.rgb()[0] > (BLACK_RGB_LEFT[0] + 5)
    )

    # go back

    while left_color_sensor.rgb()[0] < (WHITE_RGB_LEFT[0] - 5):
        base.run(500, 0)
    while left_color_sensor.rgb()[0] > (BLACK_RGB_LEFT[0] + 5):
        base.run(500, 0)
    while left_color_sensor.rgb()[0] < (WHITE_RGB_LEFT[0] - 5):
        base.run(500, 0)
    base.brake()
    wait(50)

    # base.run_target(800, -800, 250, -250)
    
    gyro_turn.turn(180)

    base.run(-1500, -1500)
    wait(800)
    base.brake()

    move()
    parking_lot_action(2, 270)

    move()
    base.hold()
    if parking_lots[1].parked_color != Color.RED:
        parking_lot_action(1, 270)

    move()
    if parking_lots[0].parked_color != Color.RED:
        parking_lot_action(0, 270)


def deposit_parked_1():

    gyro_turn.single_motor_turn(180, 0, 1)

    base.reset_angle()
    gyro_straight.move(
        1400,
        170,
        lambda: base.angle() < 600,
        True,
    )

    gyro_straight.move(
        1400,
        170,
        lambda: left_color_sensor.rgb()[0] > (BLACK_RGB_LEFT[0] + 5),
        True,
    )

    ev3.speaker.beep()

    base.reset_angle()
    gyro_straight.move(
        800,
        180,
        lambda: base.angle() < 203,
        False,
    )

    base.brake()

    gyro_turn.turn(270)

    line_track.rgb_move(
        right_color_sensor,
        800,
        [
            ((BLACK_RGB_RIGHT[0] + WHITE_RGB_RIGHT[0]) / 2),
            ((BLACK_RGB_RIGHT[0] + WHITE_RGB_RIGHT[0]) / 2),
            ((BLACK_RGB_RIGHT[0] + WHITE_RGB_RIGHT[0]) / 2),
        ],
        -1,
        lambda: left_color_sensor.rgb()[0] > (BLACK_RGB_LEFT[0] + 5),
        100,
        kp=0.045,
    )

    base.brake()

    gyro_turn.single_motor_turn(360, 0, 1)
    base.run(-1500, -1500)
    wait(500)
    base.brake()
    intake.open(left_intake)
    wait(100)
    left_parking_bay.update(True, intake.left_car_color)
    intake.update_left_possessions(None, None)

    gyro_straight.move(
        1400, 360, lambda: left_color_sensor.rgb()[0] > (BLACK_RGB_LEFT[0] + 5)
    )
    gyro_straight.move(
        1400, 360, lambda: left_color_sensor.rgb()[0] < (WHITE_RGB_LEFT[0] - 5)
    )

    intake.close()
    wait(400)

    if intake.right_car_type == 1:
        gyro_turn.single_motor_turn(250, 0, 1)
        gyro_turn.single_motor_turn(360, 1, 0)
        intake.open(right_intake)
        base.run(-1500, -1500)
        wait(800)
        base.brake()
        wait(100)
        right_parking_bay.update(True, intake.right_car_color)
        intake.update_right_possessions(None, None)

        gyro_straight.move(
            800, 360, lambda: left_color_sensor.rgb()[0] > (BLACK_RGB_LEFT[0] + 5)
        )

        intake.close()
        wait(500)


def collect_waiting_2():
    gyro_turn.single_motor_turn(465, 1, 0)
    base.brake()
    wait(100)
    gyro_sensor.reset_angle(gyro_sensor.angle() - 360)
    wait(100)
    gyro_turn.turn(180)

    intake.open()
    wait(300)

    base.reset_angle()
    gyro_straight.move(-1400, 180, lambda: base.angle() > -600)

    intake.close()

    intake.update_left_possessions(car_order[3], 0)
    intake.update_right_possessions(car_order[2], 0)

    gyro_turn.single_motor_turn(85, 1, 0)
    gyro_turn.single_motor_turn(0, 0, 1)
    intake.hold()


def deposit_waiting_2():
    def move():
        line_track.rgb_move(
            right_color_sensor,
            500,
            [
                ((BLACK_RGB_RIGHT[0] + WHITE_RGB_RIGHT[0]) / 2),
                ((BLACK_RGB_RIGHT[0] + WHITE_RGB_RIGHT[0]) / 2),
                ((BLACK_RGB_RIGHT[0] + WHITE_RGB_RIGHT[0]) / 2),
            ],
            -1,
            lambda: left_color_sensor.rgb()[0] > (BLACK_RGB_LEFT[0] + 5),
            200,
        )

        line_track.rgb_move(
            right_color_sensor,
            500,
            [
                ((BLACK_RGB_RIGHT[0] + WHITE_RGB_RIGHT[0]) / 2),
                ((BLACK_RGB_RIGHT[0] + WHITE_RGB_RIGHT[0]) / 2),
                ((BLACK_RGB_RIGHT[0] + WHITE_RGB_RIGHT[0]) / 2),
            ],
            -1,
            lambda: left_color_sensor.rgb()[0] < (WHITE_RGB_LEFT[0] - 5),
            200,
            False,
        )

    move()

    move()
    base.brake()
    parking_lot_action(9, 90)

    move()
    parking_lot_action(10, 90)

    line_track.rgb_move(
        right_color_sensor,
        500,
        [
            ((BLACK_RGB_RIGHT[0] + WHITE_RGB_RIGHT[0]) / 2),
            ((BLACK_RGB_RIGHT[0] + WHITE_RGB_RIGHT[0]) / 2),
            ((BLACK_RGB_RIGHT[0] + WHITE_RGB_RIGHT[0]) / 2),
        ],
        -1,
        lambda: left_color_sensor.rgb()[0] > (BLACK_RGB_LEFT[0] + 5),
        200,
        False,
    )
    base.hold()
    parking_lot_action(11, 90)

    gyro_straight.move(
        -500, 0, lambda: left_color_sensor.rgb()[0] > (BLACK_RGB_LEFT[0] + 5)
    )

    # go back

    while left_color_sensor.rgb()[0] < (WHITE_RGB_LEFT[0] - 5):
        base.run(500, 0)
    while left_color_sensor.rgb()[0] > (BLACK_RGB_LEFT[0] + 5):
        base.run(500, 0)
    while left_color_sensor.rgb()[0] < (WHITE_RGB_LEFT[0] - 5):
        base.run(500, 0)
    base.brake()
    wait(50)

    # base.run_target(800, -800, 250, -250)
    
    gyro_turn.turn(180)

    base.run(-1500, -1500)
    wait(800)
    base.brake()

    # cross boundary to collect red
    base.reset_angle()

    line_track.rgb_move(
        right_color_sensor,
        500,
        [
            ((BLACK_RGB_RIGHT[0] + WHITE_RGB_RIGHT[0]) / 2),
            ((BLACK_RGB_RIGHT[0] + WHITE_RGB_RIGHT[0]) / 2),
            ((BLACK_RGB_RIGHT[0] + WHITE_RGB_RIGHT[0]) / 2),
        ],
        -1,
        lambda: base.angle() < 3,
        200,
    )

    gyro_turn.turn(270)
    intake.open(right_intake)
    base.reset_angle()
    gyro_straight.move(
        -900,
        270,
        lambda: base.angle() > -510,
        True,
    )
    gyro_straight.move(
        -700,
        270,
        lambda: right_color_sensor.rgb()[0] > (BLACK_RGB_RIGHT[0] + 5),
        False,
    )
    gyro_straight.move(
        -300,
        270,
        lambda: right_color_sensor.rgb()[0] < (WHITE_RGB_RIGHT[0] - 5),
        False,
    )

    # line_track.rgb_move(
    #     right_color_sensor,
    #     500,
    #     [
    #         ((BLACK_RGB_RIGHT[0] + WHITE_RGB_RIGHT[0]) / 2),
    #         ((BLACK_RGB_RIGHT[0] + WHITE_RGB_RIGHT[0]) / 2),
    #         ((BLACK_RGB_RIGHT[0] + WHITE_RGB_RIGHT[0]) / 2),
    #     ],
    #     -1,
    #     lambda: base.angle() < 8,
    #     200,
    # )

    # gyro_turn.turn(90)
    # base.reset_angle()
    # gyro_straight.move(
    #     1400,
    #     90,
    #     lambda: base.angle() < 450,
    #     True,
    # )
    # gyro_straight.move(
    #     800,
    #     90,
    #     lambda: left_color_sensor.rgb()[0] < (WHITE_RGB_LEFT[0] - 5),
    #     False,
    # )
    # gyro_straight.move(
    #     500,
    #     90,
    #     lambda: left_color_sensor.rgb()[0] > (BLACK_RGB_LEFT[0] + 5),
    #     False,
    # )
    # base.hold()
    # gyro_turn.turn(270)

    # intake.open(right_intake)

    # gyro_straight.move(
    #     -1400,
    #     270,
    #     lambda: right_color_sensor.rgb()[0] > (BLACK_RGB_RIGHT[0] + 5),
    # )
    # gyro_straight.move(
    #     -1400,
    #     270,
    #     lambda: right_color_sensor.rgb()[0] < (WHITE_RGB_RIGHT[0] - 5),
    #     False,
    # )

    intake.close(right_intake)
    wait(400)
    intake.update_left_possessions(Color.RED, 1)

    gyro_turn.single_motor_turn(260, 0, 1)

    base.reset_angle()
    gyro_straight.move(
        1400,
        260,
        lambda: base.angle() < 480,
        True,
    )
    gyro_straight.move(
        800,
        260,
        lambda: right_color_sensor.rgb()[0] < (WHITE_RGB_RIGHT[0] - 5),
        False,
    )
    gyro_straight.move(
        800,
        260,
        lambda: right_color_sensor.rgb()[0] > (BLACK_RGB_RIGHT[0] + 5),
        False,
    )
    gyro_straight.move(
        650,
        260,
        lambda: right_color_sensor.rgb()[0] < (WHITE_RGB_RIGHT[0] - 5),
        False,
    )

    base.hold()
    intake.hold()
    gyro_turn.turn(180)
    base.brake()

    move()
    move()
    move()
    base.brake()
    base.reset_angle()

    line_track.rgb_move(
        right_color_sensor,
        500,
        [
            ((BLACK_RGB_RIGHT[0] + WHITE_RGB_RIGHT[0]) / 2),
            ((BLACK_RGB_RIGHT[0] + WHITE_RGB_RIGHT[0]) / 2),
            ((BLACK_RGB_RIGHT[0] + WHITE_RGB_RIGHT[0]) / 2),
        ],
        -1,
        lambda: base.angle() < 70,
        200,
    )
    base.brake()

    base.run_target(-800, 800, -150, 150)
    base.brake()

    gyro_straight.move(
        -1400, 90, lambda: right_color_sensor.rgb()[0] > (BLACK_RGB_RIGHT[0] + 5)
    )
    gyro_straight.move(
        -1400, 90, lambda: right_color_sensor.rgb()[0] < (WHITE_RGB_RIGHT[0] - 5)
    )
    gyro_straight.move(
        -1400, 90, lambda: right_color_sensor.rgb()[0] > (GREY_RGB_RIGHT[0] + 5)
    )
    base.brake()
    intake.open(right_intake)
    wait(100)
    intake.update_right_possessions(None, None)
    gyro_straight.move(
        300, 90, lambda: right_color_sensor.rgb()[0] < (WHITE_RGB_RIGHT[0] - 5)
    )
    gyro_straight.move(
        500, 90, lambda: right_color_sensor.rgb()[0] > (BLACK_RGB_RIGHT[0] + 5)
    )
    base.brake()
    intake.close(right_intake)
    wait(400)
    gyro_straight.move(
        1400, 90, lambda: right_color_sensor.rgb()[0] < (WHITE_RGB_RIGHT[0] - 5)
    )
    gyro_straight.move(
        1400, 90, lambda: right_color_sensor.rgb()[0] > (GREY_RGB_RIGHT[0] + 5)
    )
    base.brake()
    
    base.run_target(-800, 800, -145, 145)
    
    base.brake()
    intake.hold()
    gyro_straight.move(
        1400,
        180,
        lambda: left_color_sensor.rgb()[0] > (BLACK_RGB_LEFT[0] + 5),
        True,
    )
    base.hold()


def deposit_parked_2():
    gyro_straight.move(
        800, 180, lambda: left_color_sensor.rgb()[0] > (BLACK_RGB_LEFT[0] + 5)
    )
    ev3.speaker.beep()
    gyro_turn.turn(240)

    if left_parking_bay.occupied == False:
        gyro_turn.single_motor_turn(360, 0, 1)
        base.run(-800, -800)
        wait(1000)
        base.brake()
        intake.open(left_intake)
        wait(800)
        left_parking_bay.update(True, intake.left_car_color)
        intake.update_left_possessions(None, None)

        gyro_straight.move(
            800, 360, lambda: left_color_sensor.rgb()[0] > (BLACK_RGB_LEFT[0] + 5)
        )

        gyro_turn.single_motor_turn(240, 0, 1)

    gyro_turn.single_motor_turn(360, 1, 0)
    base.run(-800, -800)
    wait(1000)
    base.brake()

    if intake.left_car_type == 1:
        intake.open(left_intake)
        wait(800)
        gyro_straight.move(
            800, 360, lambda: left_color_sensor.rgb()[0] > (BLACK_RGB_LEFT[0] + 5)
        )
        right_parking_bay.update(True, intake.left_car_color)
        intake.update_left_possessions(None, None)
    elif intake.right_car_type == 1:
        intake.open(right_intake)
        wait(800)
        gyro_straight.move(
            800, 360, lambda: left_color_sensor.rgb()[0] > (BLACK_RGB_LEFT[0] + 5)
        )
        right_parking_bay.update(True, intake.right_car_color)
        intake.update_right_possessions(None, None)


def collect_waiting_3():
    gyro_turn.turn(90)

    base.reset_angle()
    gyro_straight.move(-900, 90, lambda: base.angle() > -130)
    base.brake()
    gyro_turn.single_motor_turn(0, 1, 0)
    base.brake()

    intake.open()

    base.reset_angle()
    gyro_straight.move(-1400, 0, lambda: base.angle() > -350)

    intake.close()
    wait(500)

    intake.update_left_possessions(car_order[4], 0)
    intake.update_right_possessions(car_order[5], 0)

    base.reset_angle()
    gyro_straight.move(1400, 0, lambda: base.angle() < 350)

    base.brake()
    intake.hold()

    gyro_turn.single_motor_turn(85, 1, 0)
    gyro_turn.single_motor_turn(0, 0, 1)


def deposit_waiting_3():
    def move():
        line_track.rgb_move(
            right_color_sensor,
            500,
            [
                ((BLACK_RGB_RIGHT[0] + WHITE_RGB_RIGHT[0]) / 2),
                ((BLACK_RGB_RIGHT[0] + WHITE_RGB_RIGHT[0]) / 2),
                ((BLACK_RGB_RIGHT[0] + WHITE_RGB_RIGHT[0]) / 2),
            ],
            -1,
            lambda: left_color_sensor.rgb()[0] > (BLACK_RGB_LEFT[0] + 5),
            200,
            False,
        )

        line_track.rgb_move(
            right_color_sensor,
            500,
            [
                ((BLACK_RGB_RIGHT[0] + WHITE_RGB_RIGHT[0]) / 2),
                ((BLACK_RGB_RIGHT[0] + WHITE_RGB_RIGHT[0]) / 2),
                ((BLACK_RGB_RIGHT[0] + WHITE_RGB_RIGHT[0]) / 2),
            ],
            -1,
            lambda: left_color_sensor.rgb()[0] < (WHITE_RGB_LEFT[0] - 5),
            200,
            False,
        )

    move()
    move()
    move()

    line_track.rgb_move(
        right_color_sensor,
        500,
        [
            ((BLACK_RGB_RIGHT[0] + WHITE_RGB_RIGHT[0]) / 2),
            ((BLACK_RGB_RIGHT[0] + WHITE_RGB_RIGHT[0]) / 2),
            ((BLACK_RGB_RIGHT[0] + WHITE_RGB_RIGHT[0]) / 2),
        ],
        -1,
        lambda: left_color_sensor.rgb()[0] > (BLACK_RGB_LEFT[0] + 5),
        200,
        False,
    )
    base.hold()

    gyro_turn.turn(-90, kp=0.85)

    intake.open(left_intake)

    gyro_straight.move(
        -1400, -90, lambda: left_color_sensor.rgb()[0] > (BLACK_RGB_LEFT[0] + 5)
    )
    gyro_straight.move(
        -1400, -90, lambda: left_color_sensor.rgb()[0] < (WHITE_RGB_LEFT[0] - 5)
    )
    gyro_straight.move(
        -1400, -90, lambda: left_color_sensor.rgb()[0] > (GREY_RGB_LEFT[0] + 5)
    )
    wait(100)
    intake.update_left_possessions(None, None, intake.left_batteries - 1)
    gyro_straight.move(
        800, -90, lambda: left_color_sensor.rgb()[0] < (WHITE_RGB_LEFT[0] - 5)
    )
    gyro_straight.move(
        800, -90, lambda: left_color_sensor.rgb()[0] > (BLACK_RGB_LEFT[0] + 5)
    )
    gyro_straight.move(
        500, -90, lambda: left_color_sensor.rgb()[0] < (WHITE_RGB_LEFT[0] - 5)
    )
    gyro_straight.move(
        300, -90, lambda: left_color_sensor.rgb()[0] > (GREY_RGB_LEFT[0] + 5)
    )

    gyro_turn.turn(-183)

    line_track.rgb_move(
        right_color_sensor,
        500,
        [
            ((BLACK_RGB_RIGHT[0] + WHITE_RGB_RIGHT[0]) / 2),
            ((BLACK_RGB_RIGHT[0] + WHITE_RGB_RIGHT[0]) / 2),
            ((BLACK_RGB_RIGHT[0] + WHITE_RGB_RIGHT[0]) / 2),
        ],
        -1,
        lambda: left_color_sensor.rgb()[0] > (BLACK_RGB_LEFT[0] + 5),
        200,
        False,
    )
    base.hold()
    parking_lot_action(6, -90)
    move()
    move()

    line_track.rgb_move(
        right_color_sensor,
        1400,
        [
            ((BLACK_RGB_RIGHT[0] + WHITE_RGB_RIGHT[0]) / 2),
            ((BLACK_RGB_RIGHT[0] + WHITE_RGB_RIGHT[0]) / 2),
            ((BLACK_RGB_RIGHT[0] + WHITE_RGB_RIGHT[0]) / 2),
        ],
        -1,
        lambda: left_color_sensor.rgb()[0] > (BLACK_RGB_LEFT[0] + 5),
        200,
        False,
    )


def end():
    gyro_turn.turn(-50)
    base.reset_angle()
    gyro_straight.move(-1400, -52, lambda: base.angle() > -1100)


def parking_lot_action(parking_lot: int, angle: int):
    if (
        parking_lots[parking_lot].parked_color is None
        and parking_lots[parking_lot].barrier == False
    ):
        if intake.left_car_color == parking_lots[parking_lot].color and (
            intake.left_car_type == 0 or intake.left_car_color == Color.RED
        ):
            if intake.left_car_color == Color.RED and intake.left_batteries > 0:
                deposit_waiting_without_battery(left_intake, angle)
            else:
                deposit_waiting(left_intake, angle)

            parking_lots[parking_lot].update(intake.left_car_color, 0, False)
        elif intake.right_car_color == parking_lots[parking_lot].color and (
            intake.right_car_type == 0 or intake.right_car_color == Color.RED
        ):
            if intake.right_car_color == Color.RED and intake.right_batteries > 0:
                deposit_waiting_without_battery(right_intake, angle)
            else:
                deposit_waiting(right_intake, angle)

            parking_lots[parking_lot].update(intake.right_car_color, 0, False)

    elif (
        parking_lots[parking_lot].parked_type == 1
        and parking_lots[parking_lot].barrier == False
    ):
        if intake.left_car_type is None:
            collect_parked(left_intake, angle, parking_lots[parking_lot].parked_color)
        elif intake.right_car_type is None:
            collect_parked(right_intake, angle, parking_lots[parking_lot].parked_color)

        parking_lots[parking_lot].update(None, None, False)


# Write your program here.

while True:
    if ev3.buttons.pressed():
        if ev3.buttons.pressed()[0] == Button.CENTER:
            break

# intake.update_left_possessions(Color.GREEN, 0, 2)
# intake.update_right_possessions(Color.RED, 0, 2)
# intake.close()
# wait(400)
# intake.hold()

start()
collect_waiting_1()
deposit_waiting_1()
deposit_parked_1()
collect_waiting_2()
deposit_waiting_2()
# deposit_parked_2()
collect_waiting_3()
deposit_waiting_3()
end()

# ev3.speaker.beep()

# while True:
#     gyro_turn.turn(90)
#     base.brake()
#     ev3.speaker.beep()
#     gyro_sensor.reset_angle(0)
#     wait(1000)
