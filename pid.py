from devices import *
from constants import *


class PID(object):
    def __init__(
        self,
    ):
        self.base = base
        self.proportional = 0
        self.integral = 0
        self.derivative = 0
        self.error = 0
        self.last_error = 0
        self.correction = 0
        self.loop = 0

    def reset_values(self):
        self.proportional = 0
        self.integral = 0
        self.derivative = 0
        self.last_error = 0
        self.loop = 0


class LineTrack(PID):
    def __init__(self):
        PID.__init__(self)

    def rgb_move(
        self,
        sensor: ColorSensor,
        speed: float,
        threshold,
        side: int = 1,
        condition=lambda: True,
        loop=0,
        reset=True,
        kp=0.035,
        ki=0.0001,
        kd=1.3,
    ):
        if reset is True:
            self.reset_values()

        self.loop = loop

        while condition():
            self.error = (
                (threshold[0] - sensor.rgb()[0])
                + (threshold[1] - sensor.rgb()[1])
                + (threshold[2] - sensor.rgb()[2])
            )
            self.proportional = self.error * kp
            self.integral += self.error
            self.derivative = (self.error - self.last_error) * kd

            self.correction = (self.integral * ki) + self.proportional + self.derivative

            if self.loop < 200:
                self.base.run(
                    200 + (side * self.correction * 10),
                    200 - (side * self.correction * 10),
                )
            else:
                self.base.run(
                    speed + (side * self.correction * 10),
                    speed - (side * self.correction * 10),
                )

            self.loop += 1
            self.last_error = self.error

    def double_sensor_move(
        self,
        speed: float,
        left_threshold,
        right_threshold,
        condition=lambda: True,
        loop=0,
        reset=True,
        kp=0.03,
        ki=0.00,
        kd=0.5,
    ):
        if reset is True:
            self.reset_values()

        self.loop = loop

        while condition():
            self.error = (
                -(left_threshold[0] - left_color_sensor.rgb()[0])
                - (left_threshold[1] - left_color_sensor.rgb()[1])
                - (left_threshold[2] - left_color_sensor.rgb()[2])
                + (right_threshold[0] - right_color_sensor.rgb()[0])
                + (right_threshold[1] - right_color_sensor.rgb()[1])
                + (right_threshold[2] - left_color_sensor.rgb()[2])
            )
            self.proportional = self.error * kp
            self.integral += self.error
            self.derivative = (self.error - self.last_error) * kd

            self.correction = (self.integral * ki) + self.proportional + self.derivative

            if self.loop < 200:
                self.base.run(
                    200 + (self.correction * 10),
                    200 - (self.correction * 10),
                )
            else:
                self.base.run(
                    speed + (self.correction * 10),
                    speed - (self.correction * 10),
                )

            self.loop += 1
            self.last_error = self.error


class GyroStraight(PID):
    def __init__(self):
        PID.__init__(self)

    def move(
        self,
        speed: float,
        threshold: int,
        condition=lambda: True,
        kp=0.70,
        ki=0.00,
        kd=0.00,
    ):
        self.reset_values()

        while condition():
            self.error = threshold - gyro_sensor.angle()
            self.proportional = self.error * kp
            self.integral += self.error
            self.derivative = (self.error - self.last_error) * kd

            self.correction = (self.integral * ki) + self.proportional + self.derivative

            self.base.run(
                speed + (self.correction * 10), speed - (self.correction * 10)
            )

            self.last_error = self.error

        base.brake()


class GyroTurn(PID):
    def __init__(self):
        PID.__init__(self)

    def turn(
        self,
        threshold: int,
        kp=0.9,
        ki=0.0001,
        kd=0.0004,
    ):
        self.reset_values()

        while gyro_sensor.angle() is not threshold:
            self.error = threshold - gyro_sensor.angle()
            self.proportional = self.error * kp
            self.integral += self.error
            self.derivative = (self.error - self.last_error) * kd

            self.correction = (self.integral * ki) + self.proportional + self.derivative

            base.run(self.correction * 10, -(self.correction * 10))

            self.last_error = self.error

        base.brake()

    def single_motor_turn(
        self,
        threshold: int,
        left_mode: int,
        right_mode: int,
        kp=1.50,
        ki=0.00001,
        kd=0.0004,
    ):
        self.reset_values()

        while gyro_sensor.angle() is not threshold:
            self.error = threshold - gyro_sensor.angle()
            self.proportional = self.error * kp
            self.integral += self.error
            self.derivative = (self.error - self.last_error) * kd

            self.correction = (self.integral * ki) + self.proportional + self.derivative

            base.run(
                left_mode * self.correction * 10,
                right_mode * -(self.correction * 10),
            )

            self.last_error = self.error

        base.brake()


gyro_straight = GyroStraight()
gyro_turn = GyroTurn()
line_track = LineTrack()
