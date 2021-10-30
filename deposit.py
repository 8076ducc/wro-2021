from pybricks.parameters import Color
from pybricks.tools import wait
from devices import *
from pid import *
from constants import *


def deposit_waiting(motor: Motor, angle: int):

    base.reset_angle()

    if motor is left_intake:
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
            False,
        )
        base.brake()
        sensor = left_color_sensor
        intake_possessions = left_intake_possessions
        black_value = BLACK_RGB_LEFT
        white_value = WHITE_RGB_LEFT
        grey_value = GREY_RGB_LEFT
    elif motor is right_intake:
        # gyro_straight.move(
        #     -400,
        #     (angle - 90),
        #     lambda: base.angle() > -3,
        # )
        base.brake()
        sensor = right_color_sensor
        intake_possessions = right_intake_possessions
        black_value = BLACK_RGB_RIGHT
        white_value = WHITE_RGB_RIGHT
        grey_value = GREY_RGB_RIGHT

    gyro_turn.turn(angle)
    base.brake()

    gyro_straight.move(-1400, angle, lambda: sensor.rgb()[0] > (black_value[0] + 5))
    gyro_straight.move(-1400, angle, lambda: sensor.rgb()[0] < (white_value[0] - 5))
    gyro_straight.move(-1400, angle, lambda: sensor.rgb()[0] > (grey_value[0] + 5))
    base.brake()
    intake.open(motor)
    wait(600)
    gyro_straight.move(1400, angle, lambda: sensor.rgb()[0] < (white_value[0] - 5))
    gyro_straight.move(500, angle, lambda: sensor.rgb()[0] > (black_value[0] + 5))

    if intake_possessions.number_of_batteries is 2:
        ev3.speaker.beep()
        base.brake()
        intake.close(motor)
        wait(600)
        intake.hold()

        gyro_straight.move(500, angle, lambda: sensor.rgb()[0] < (white_value[0] - 5))
        gyro_straight.move(300, angle, lambda: sensor.rgb()[0] > (grey_value[0] + 5))
    else:
        gyro_straight.move(500, angle, lambda: sensor.rgb()[0] < (white_value[0] - 5))

    base.brake()
    gyro_turn.turn(angle - 98)
    base.brake()
    intake_possessions.update(None, None, intake_possessions.number_of_batteries - 1)


def deposit_waiting_without_battery(motor: Motor, angle: int):

    base.reset_angle()

    if motor is left_intake:
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
        sensor = left_color_sensor
        intake_possessions = left_intake_possessions
        black_value = BLACK_RGB_LEFT
        white_value = WHITE_RGB_LEFT
        grey_value = GREY_RGB_LEFT
    elif motor is right_intake:
        # gyro_straight.move(
        #     -400,
        #     (angle - 90),
        #     lambda: base.angle() > -3,
        # )
        base.brake()
        sensor = right_color_sensor
        intake_possessions = right_intake_possessions
        black_value = BLACK_RGB_RIGHT
        white_value = WHITE_RGB_RIGHT
        grey_value = GREY_RGB_RIGHT

    gyro_turn.turn(angle)
    base.brake()

    gyro_straight.move(-1400, angle, lambda: sensor.rgb()[0] > (black_value[0] + 5))
    gyro_straight.move(-1400, angle, lambda: sensor.rgb()[0] < (white_value[0] - 5))
    gyro_straight.move(-1400, angle, lambda: sensor.rgb()[0] > (grey_value[0] + 5))
    base.brake()
    intake.open(motor)
    wait(600)
    intake_possessions.update(None, None)
    gyro_straight.move(1400, angle, lambda: sensor.rgb()[0] < (white_value[0] - 5))
    gyro_straight.move(1400, angle, lambda: sensor.rgb()[0] > (black_value[0] + 5))
    base.brake()
    intake.close(motor)
    wait(600)
    intake.hold()
    gyro_straight.move(1400, angle, lambda: sensor.rgb()[0] < (white_value[0] - 5))
    gyro_straight.move(300, angle, lambda: sensor.rgb()[0] > (grey_value[0] + 5))

    base.brake()
    gyro_turn.turn(angle - 98)
    base.brake()


def collect_parked(motor: Motor, angle: int, car_color: Color):

    base.reset_angle()

    if motor is left_intake:
        line_track.rgb_move(
            right_color_sensor,
            500,
            [
                ((BLACK_RGB_RIGHT[0] + WHITE_RGB_RIGHT[0]) / 2),
                ((BLACK_RGB_RIGHT[0] + WHITE_RGB_RIGHT[0]) / 2),
                ((BLACK_RGB_RIGHT[0] + WHITE_RGB_RIGHT[0]) / 2),
            ],
            -1,
            lambda: base.angle() < 95,
        )
        base.brake()
        sensor = left_color_sensor
        intake_possessions = left_intake_possessions
        black_value = BLACK_RGB_LEFT
        white_value = WHITE_RGB_LEFT
        # grey_value = GREY_LEFT
    elif motor is right_intake:
        # line_track.rgb_move(
        #     right_color_sensor,
        #     500,
        #     [
        #         ((BLACK_RGB_RIGHT[0] + WHITE_RGB_RIGHT[0]) / 2),
        #         ((BLACK_RGB_RIGHT[0] + WHITE_RGB_RIGHT[0]) / 2),
        #         ((BLACK_RGB_RIGHT[0] + WHITE_RGB_RIGHT[0]) / 2),
        #     ],
        #     -1,
        #     lambda: base.angle() < 10,
        # )
        sensor = right_color_sensor
        intake_possessions = right_intake_possessions
        black_value = BLACK_RGB_RIGHT
        white_value = WHITE_RGB_RIGHT
        # grey_value = GREY_RIGHT

    gyro_turn.turn(angle)
    base.brake()

    intake.open(motor)

    gyro_straight.move(-1400, angle, lambda: sensor.rgb()[0] > (black_value[0] + 5))
    gyro_straight.move(-1400, angle, lambda: sensor.rgb()[0] < (white_value[0] - 5))
    base.brake()
    intake.close(motor)
    wait(600)
    intake_possessions.update(car_color, 1)

    gyro_straight.move(1400, angle, lambda: sensor.rgb()[0] < (white_value[0] - 5))
    gyro_straight.move(1400, angle, lambda: sensor.rgb()[0] > (black_value[0] + 5))
    gyro_straight.move(300, angle, lambda: sensor.rgb()[0] < (white_value[0] - 5))
    base.brake()
    gyro_turn.turn(angle - 90)
    base.brake()
