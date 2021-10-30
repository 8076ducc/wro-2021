#!/usr/bin/env pybricks-micropython
from pybricks.parameters import Color, Button
from pybricks.tools import wait
from devices import *
from pid import *
from localise import *
from deposit import *
from constants import *


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
    )
    gyro_straight.move(
        800,
        -10,
        lambda: left_color_sensor.rgb()[0] < (WHITE_RGB_LEFT[0] - 5),
    )
    ev3.speaker.beep()
    base.brake()

    gyro_turn.turn(-90)
    base.run(-800, -800)
    wait(600)
    base.brake()
    intake.stop()
    intake.close()
    wait(600)
    intake.stop()
    intake.hold()
    left_intake_possessions.update(number_of_batteries=1)
    right_intake_possessions.update(number_of_batteries=1)

    gyro_turn.single_motor_turn(-10, 1, 0)
    gyro_turn.single_motor_turn(-90, 0, 1)
    intake.open()
    wait(400)
    base.run(-800, -800)
    wait(600)
    base.brake()
    intake.stop()
    intake.close()
    wait(600)
    intake.stop()
    intake.hold()
    left_intake_possessions.update(number_of_batteries=2)
    right_intake_possessions.update(number_of_batteries=2)
    gyro_turn.single_motor_turn(-35, 1, 0)
    gyro_turn.single_motor_turn(-90, 0, 1)


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
    speed = 400

    color = None
    last_color = None

    loop = 100

    while len(car_order) < 6:
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

        if color is not None and color is not last_color:

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
    gyro_straight.move(-400, -90, lambda: left_color_sensor.rgb()[0] < 70)

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
    right_intake_possessions.update(car_order[1], 0)

    wait(500)

    gyro_straight.move(
        1400, 0, lambda: left_color_sensor.rgb()[0] < (WHITE_RGB_LEFT[0] - 5)
    )
    gyro_straight.move(
        1400, 0, lambda: left_color_sensor.rgb()[0] > (BLACK_RGB_LEFT[0] + 5)
    )

    base.brake()

    gyro_turn.single_motor_turn(110, 1, 0)
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
    base.brake()
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
    gyro_turn.turn(180)
    base.run(-800, -800)
    wait(1000)
    base.brake()
    wait(50)

    move()
    parking_lot_action(2, 270)

    move()
    base.hold()
    if parking_lots[1].parked_color is not Color.RED:
        parking_lot_action(1, 270)

    move()
    if parking_lots[0].parked_color is not Color.RED:
        parking_lot_action(0, 270)


def deposit_parked_1():
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
        0,
        False,
    )

    # line_track.rgb_move(
    #     right_color_sensor,
    #     1400,
    #     [
    #         ((BLACK_RGB_RIGHT[0] + WHITE_RGB_RIGHT[0]) / 2),
    #         ((BLACK_RGB_RIGHT[0] + WHITE_RGB_RIGHT[0]) / 2),
    #         ((BLACK_RGB_RIGHT[0] + WHITE_RGB_RIGHT[0]) / 2),
    #     ],
    #     -1,
    #     lambda: left_color_sensor.rgb()[0] < (WHITE_RGB_LEFT[0] - 5),
    #     100,
    #     False,
    # )

    gyro_turn.turn(220)
    gyro_straight.move(
        800, 225, lambda: left_color_sensor.rgb()[0] > (BLACK_RGB_LEFT[0] + 5)
    )
    gyro_straight.move(
        800, 225, lambda: left_color_sensor.rgb()[0] < (WHITE_RGB_LEFT[0] - 5)
    )
    gyro_turn.single_motor_turn(270, 1, 0)

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
        200,
    )

    gyro_turn.single_motor_turn(360, 0, 1)
    base.run(-800, -800)
    wait(1000)
    base.brake()
    if left_intake_possessions.car_type is 1:
        intake.open(left_intake)
        wait(800)
        left_parking_bay.update(True, left_intake_possessions.car_color)
        left_intake_possessions.update(None, None)
    elif right_intake_possessions.car_type is 1:
        intake.open(right_intake)
        wait(800)
        right_parking_bay.update(True, right_intake_possessions.car_color)
        right_intake_possessions.update(None, None)

    gyro_straight.move(
        800, 360, lambda: left_color_sensor.rgb()[0] > (BLACK_RGB_LEFT[0] + 5)
    )

    intake.close()
    wait(500)
    intake.hold()

    if right_intake_possessions.car_type is 1:
        gyro_turn.single_motor_turn(240, 0, 1)
        gyro_turn.single_motor_turn(360, 1, 0)
        base.run(-800, -800)
        wait(1000)
        base.brake()

        intake.open(right_intake)
        wait(800)
        right_parking_bay.update(True, right_intake_possessions.car_color)
        right_intake_possessions.update(None, None)

        gyro_straight.move(
            800, 360, lambda: left_color_sensor.rgb()[0] > (BLACK_RGB_LEFT[0] + 5)
        )

        intake.close()
        wait(500)
        intake.hold()


def collect_waiting_2():
    gyro_turn.single_motor_turn(450, 1, 0)
    gyro_turn.turn(180)

    intake.open()

    base.reset_angle()
    gyro_straight.move(-600, 180, lambda: base.angle() > -600)

    intake.close()
    wait(500)
    intake.hold()

    left_intake_possessions.update(car_order[3], 0)
    right_intake_possessions.update(car_order[2], 0)

    gyro_turn.single_motor_turn(80, 1, 0)
    gyro_turn.single_motor_turn(-3, 0, 1)


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
        )

    move()

    move()
    base.brake()
    parking_lot_action(9, 90)

    move()
    parking_lot_action(10, 90)

    move()
    base.brake()
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
    gyro_turn.turn(180)
    base.run(-800, -800)
    wait(1000)
    base.brake()
    wait(50)

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
        lambda: base.angle() < 5,
        200,
    )

    gyro_turn.turn(270)
    intake.open(right_intake)
    gyro_straight.move(
        -900, 270, lambda: right_color_sensor.rgb()[0] > (BLACK_RGB_RIGHT[0] + 5)
    )
    gyro_straight.move(
        -900, 270, lambda: right_color_sensor.rgb()[0] < (WHITE_RGB_RIGHT[0] - 5)
    )
    gyro_straight.move(
        -900, 270, lambda: right_color_sensor.rgb()[0] > (GREY_RGB_RIGHT[0] + 5)
    )
    gyro_straight.move(
        -900, 270, lambda: right_color_sensor.rgb()[0] > (BLACK_RGB_RIGHT[0] + 5)
    )
    ev3.speaker.beep()
    base.brake()
    gyro_turn.turn(270)
    gyro_straight.move(
        -900, 270, lambda: right_color_sensor.rgb()[0] < (WHITE_RGB_RIGHT[0] - 5)
    )
    gyro_straight.move(
        -700, 270, lambda: right_color_sensor.rgb()[0] > (BLACK_RGB_RIGHT[0] + 5)
    )
    gyro_straight.move(
        -300, 270, lambda: right_color_sensor.rgb()[0] < (WHITE_RGB_RIGHT[0] - 5)
    )
    base.brake()
    intake.close(right_intake)
    wait(600)
    intake.hold()
    left_intake_possessions.update(Color.RED, 1)

    gyro_straight.move(
        900, 270, lambda: right_color_sensor.rgb()[0] < (WHITE_RGB_RIGHT[0] - 5)
    )
    gyro_straight.move(
        900, 270, lambda: right_color_sensor.rgb()[0] > (BLACK_RGB_RIGHT[0] + 5)
    )
    gyro_straight.move(
        900, 270, lambda: right_color_sensor.rgb()[0] < (WHITE_RGB_RIGHT[0] - 5)
    )
    gyro_straight.move(
        900, 270, lambda: right_color_sensor.rgb()[0] > (GREY_RGB_RIGHT[0] + 5)
    )
    base.brake()
    gyro_turn.turn(270)
    gyro_straight.move(
        900, 270, lambda: right_color_sensor.rgb()[0] < (WHITE_RGB_RIGHT[0] - 5)
    )
    gyro_straight.move(
        900, 270, lambda: right_color_sensor.rgb()[0] > (BLACK_RGB_RIGHT[0] + 5)
    )

    base.brake()
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
        lambda: base.angle() < 80,
        200,
    )
    base.brake()

    gyro_turn.turn(90)
    base.brake()

    gyro_straight.move(
        -900, 90, lambda: right_color_sensor.rgb()[0] > (BLACK_RGB_RIGHT[0] + 5)
    )
    gyro_straight.move(
        -900, 90, lambda: right_color_sensor.rgb()[0] < (WHITE_RGB_RIGHT[0] - 5)
    )
    gyro_straight.move(
        -900, 90, lambda: right_color_sensor.rgb()[0] > (GREY_RGB_RIGHT[0] + 5)
    )
    base.brake()
    intake.open(right_intake)
    wait(600)
    right_intake_possessions.update(None, None)
    gyro_straight.move(
        900, 90, lambda: right_color_sensor.rgb()[0] < (WHITE_RGB_RIGHT[0] - 5)
    )
    gyro_straight.move(
        900, 90, lambda: right_color_sensor.rgb()[0] > (BLACK_RGB_RIGHT[0] + 5)
    )
    base.brake()
    intake.close(right_intake)
    wait(600)
    intake.hold()
    gyro_straight.move(
        900, 90, lambda: right_color_sensor.rgb()[0] < (WHITE_RGB_RIGHT[0] - 5)
    )
    gyro_straight.move(
        500, 90, lambda: right_color_sensor.rgb()[0] > (GREY_RGB_RIGHT[0] + 5)
    )

    base.brake()
    gyro_turn.turn(177)
    base.brake()

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
        200,
        False,
    )
    ev3.speaker.beep()
    base.brake()


def deposit_parked_2():
    gyro_straight.move(
        800, 180, lambda: left_color_sensor.rgb()[0] > (BLACK_RGB_LEFT[0] + 5)
    )
    ev3.speaker.beep()
    gyro_turn.turn(240)

    if left_parking_bay.occupied is False:
        gyro_turn.single_motor_turn(360, 0, 1)
        base.run(-800, -800)
        wait(1000)
        base.brake()
        intake.open(left_intake)
        wait(800)
        left_parking_bay.update(True, left_intake_possessions.car_color)
        left_intake_possessions.update(None, None)

        gyro_straight.move(
            800, 360, lambda: left_color_sensor.rgb()[0] > (BLACK_RGB_LEFT[0] + 5)
        )

        gyro_turn.single_motor_turn(240, 0, 1)

    gyro_turn.single_motor_turn(360, 1, 0)
    base.run(-800, -800)
    wait(1000)
    base.brake()

    if left_intake_possessions.car_type is 1:
        intake.open(left_intake)
        wait(800)
        gyro_straight.move(
            800, 360, lambda: left_color_sensor.rgb()[0] > (BLACK_RGB_LEFT[0] + 5)
        )
        right_parking_bay.update(True, left_intake_possessions.car_color)
        left_intake_possessions.update(None, None)
    elif right_intake_possessions.car_type is 1:
        intake.open(right_intake)
        wait(800)
        gyro_straight.move(
            800, 360, lambda: left_color_sensor.rgb()[0] > (BLACK_RGB_LEFT[0] + 5)
        )
        right_parking_bay.update(True, right_intake_possessions.car_color)
        right_intake_possessions.update(None, None)


def collect_waiting_3():
    gyro_turn.turn(90)
    gyro_straight.move(
        -900, 90, lambda: right_color_sensor.rgb()[0] < (WHITE_RGB_RIGHT[0] - 5)
    )
    gyro_straight.move(
        -900, 90, lambda: right_color_sensor.rgb()[0] > (BLACK_RGB_RIGHT[0] + 5)
    )
    gyro_straight.move(
        -900, 90, lambda: right_color_sensor.rgb()[0] < (WHITE_RGB_RIGHT[0] - 5)
    )
    base.brake()
    gyro_turn.single_motor_turn(0, 1, 0)
    base.brake()

    intake.open()

    base.reset_angle()
    gyro_straight.move(-700, 0, lambda: base.angle() > -600)

    intake.close()
    wait(500)
    intake.hold()

    left_intake_possessions.update(car_order[4], 0)
    right_intake_possessions.update(car_order[5], 0)

    wait(500)

    base.reset_angle()
    gyro_straight.move(900, 0, lambda: base.angle() < 600)

    base.brake()

    gyro_turn.single_motor_turn(110, 1, 0)
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
        )

    move()
    move()
    move()
    move()

    # go back

    while left_color_sensor.rgb()[0] < (WHITE_RGB_LEFT[0] - 5):
        base.run(500, 0)
    while left_color_sensor.rgb()[0] > (BLACK_RGB_LEFT[0] + 5):
        base.run(500, 0)
    while left_color_sensor.rgb()[0] < (WHITE_RGB_LEFT[0] - 5):
        base.run(500, 0)
    base.brake()
    wait(50)
    gyro_turn.turn(180)
    base.run(-800, -800)
    wait(1000)
    base.brake()
    wait(50)

    parking_lot_action(7, 270)

    move()
    base.brake()
    parking_lot_action(6, 270)

    move()
    parking_lot_action(5, 270)

    move()
    parking_lot_action(4, 270)

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
        200,
        False,
    )


def end():
    gyro_turn.turn(315)
    gyro_straight.move(
        -900, 315, lambda: right_color_sensor.rgb()[0] > (BLACK_RGB_RIGHT[0] + 5)
    )
    gyro_straight.move(
        -900, 315, lambda: right_color_sensor.rgb()[0] < (WHITE_RGB_RIGHT[0] - 5)
    )
    gyro_straight.move(
        -900, 315, lambda: right_color_sensor.rgb()[0] > (BLACK_RGB_RIGHT[0] + 5)
    )
    gyro_straight.move(
        -900, 315, lambda: right_color_sensor.rgb()[0] < (WHITE_RGB_RIGHT[0] - 5)
    )
    # gyro_straight.move(
    #     -900, 315, lambda: right_color_sensor.rgb()[0] > (BLACK_RGB_RIGHT[0] + 5)
    # )

    base.run(-900, -700)
    wait(1000)
    base.brake()


def parking_lot_action(parking_lot: int, angle: int):
    if (
        parking_lots[parking_lot].parked_color is None
        and parking_lots[parking_lot].barrier is False
    ):
        if left_intake_possessions.car_color is parking_lots[parking_lot].color and (
            left_intake_possessions.car_type is 0
            or left_intake_possessions.car_color is Color.RED
        ):
            if (
                left_intake_possessions.car_color is Color.RED
                and left_intake_possessions.number_of_batteries > 0
            ):
                deposit_waiting_without_battery(left_intake, angle)
            else:
                deposit_waiting(left_intake, angle)
        elif right_intake_possessions.car_color is parking_lots[parking_lot].color and (
            right_intake_possessions.car_type is 0
            or right_intake_possessions.car_color is Color.RED
        ):
            if (
                right_intake_possessions.car_color is Color.RED
                and right_intake_possessions.number_of_batteries > 0
            ):
                deposit_waiting_without_battery(right_intake, angle)
            else:
                deposit_waiting(right_intake, angle)

        parking_lots[parking_lot].update(None, None, False)

    elif (
        parking_lots[parking_lot].parked_type is 1
        and parking_lots[parking_lot].barrier is False
    ):
        if left_intake_possessions.car_type is None:
            collect_parked(left_intake, angle, parking_lots[parking_lot].parked_color)
        elif right_intake_possessions.car_type is None:
            collect_parked(right_intake, angle, parking_lots[parking_lot].parked_color)

        parking_lots[parking_lot].update(None, None, False)


# Write your program here.

# while True:
#     if ev3.buttons.pressed():
#         if ev3.buttons.pressed()[0] is Button.CENTER:
#             break

# wait(100)
# ev3.speaker.beep()

left_intake_possessions.update(Color.GREEN, 0, 2)
right_intake_possessions.update(Color.RED, 0, 2)
intake.close()
wait(400)
intake.hold()

# start()
# collect_waiting_1()
deposit_waiting_1()
deposit_parked_1()
collect_waiting_2()
deposit_waiting_2()
deposit_parked_2()
collect_waiting_3()
deposit_waiting_3()
end()

ev3.speaker.beep()

# line_track.rgb_move(
#     right_color_sensor,
#     800,
#     [
#         ((BLACK_RGB_RIGHT[0] + WHITE_RGB_RIGHT[0]) / 2),
#         ((BLACK_RGB_RIGHT[0] + WHITE_RGB_RIGHT[0]) / 2),
#         ((BLACK_RGB_RIGHT[0] + WHITE_RGB_RIGHT[0]) / 2),
#     ],
#     -1,
#     lambda: True,
#     0,
# )
