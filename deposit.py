from pybricks.parameters import Color
from pybricks.tools import wait
from devices import *
from pid import *
from constants import *


def deposit_waiting(motor: Motor, angle: int):

    base.reset_angle()

    if motor is left_intake:
        line_track.move(right_color_sensor, 500, 50, -1, lambda: base.angle() < 95)
        sensor = left_color_sensor
        intake_possessions = left_intake_possessions
        black_value = BLACK_LEFT
        white_value = WHITE_LEFT
        grey_value = GREY_LEFT
    elif motor is right_intake:
        line_track.move(right_color_sensor, 500, 50, -1, lambda: base.angle() < 10)
        sensor = right_color_sensor
        intake_possessions = right_intake_possessions
        black_value = BLACK_RIGHT
        white_value = WHITE_RIGHT
        grey_value = GREY_RIGHT

    gyro_turn.turn(angle)

    gyro_straight.move(-900, angle, lambda: sensor.reflection() > (black_value + 5))
    gyro_straight.move(-900, angle, lambda: sensor.reflection() < (white_value - 5))
    gyro_straight.move(-900, angle, lambda: sensor.reflection() > (grey_value + 5))
    base.brake()
    intake.open(motor)
    wait(800)
    intake_possessions.update(None, None, intake_possessions.number_of_batteries - 1)
    gyro_straight.move(900, angle, lambda: sensor.reflection() < (white_value - 5))
    gyro_straight.move(500, angle, lambda: sensor.reflection() > (black_value + 5))
    gyro_straight.move(500, angle, lambda: sensor.reflection() < (white_value - 15))
    base.brake()
    gyro_turn.turn(angle - 95)
    base.brake()


def deposit_waiting_without_battery(motor: Motor, angle: int):

    base.reset_angle()

    if motor is left_intake:
        line_track.move(right_color_sensor, 500, 50, -1, lambda: base.angle() < 95)
        sensor = left_color_sensor
        intake_possessions = left_intake_possessions
        black_value = BLACK_LEFT
        white_value = WHITE_LEFT
        grey_value = GREY_LEFT
    elif motor is right_intake:
        line_track.move(right_color_sensor, 500, 50, -1, lambda: base.angle() < 10)
        sensor = right_color_sensor
        intake_possessions = right_intake_possessions
        black_value = BLACK_RIGHT
        white_value = WHITE_RIGHT
        grey_value = GREY_RIGHT

    gyro_turn.turn(angle)

    gyro_straight.move(-900, angle, lambda: sensor.reflection() > (black_value + 5))
    gyro_straight.move(-900, angle, lambda: sensor.reflection() < (white_value - 5))
    gyro_straight.move(-900, angle, lambda: sensor.reflection() > (grey_value + 5))
    base.brake()
    intake.open(motor)
    wait(800)
    intake_possessions.update(None, None)
    gyro_straight.move(900, angle, lambda: sensor.reflection() < (white_value - 5))
    gyro_straight.move(900, angle, lambda: sensor.reflection() > (black_value + 5))
    base.brake()
    intake.close(motor)
    wait(500)
    intake.hold()
    gyro_straight.move(900, angle, lambda: sensor.reflection() < (white_value - 5))
    gyro_straight.move(500, angle, lambda: sensor.reflection() > (grey_value + 5))

    base.brake()
    gyro_turn.turn(angle - 100)
    base.brake()


def collect_parked(motor: Motor, angle: int, car_color: Color):

    global collected_red_parked
    global collected_green_parked
    global collected_blue_parked

    base.reset_angle()
    intake.open(motor)

    if motor is left_intake:
        line_track.move(right_color_sensor, 500, 50, -1, lambda: base.angle() < 95)
        sensor = left_color_sensor
        intake_possessions = left_intake_possessions
        black_value = BLACK_LEFT
        white_value = WHITE_LEFT
        # grey_value = GREY_LEFT
    elif motor is right_intake:
        line_track.move(right_color_sensor, 500, 50, -1, lambda: base.angle() < 20)
        sensor = right_color_sensor
        intake_possessions = right_intake_possessions
        black_value = BLACK_RIGHT
        white_value = WHITE_RIGHT
        # grey_value = GREY_RIGHT

    gyro_turn.turn(angle)

    gyro_straight.move(-900, angle, lambda: sensor.reflection() > (black_value + 5))
    gyro_straight.move(-900, angle, lambda: sensor.reflection() < (white_value - 5))
    base.brake()
    intake.close(motor)
    wait(800)
    intake_possessions.update(car_color, 1)

    if car_color is Color.RED:
        collected_red_parked = True
    elif car_color is Color.GREEN:
        collected_green_parked = True
    elif car_color is Color.BLUE:
        collected_blue_parked = True

    gyro_straight.move(900, angle, lambda: sensor.reflection() < (white_value - 5))
    gyro_straight.move(900, angle, lambda: sensor.reflection() > (black_value + 5))
    # gyro_straight.move(900, angle, lambda: sensor.reflection() < (white_value - 5))
    base.brake()
    gyro_turn.turn(angle - 90)
    base.brake()
