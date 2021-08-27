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
import constants


class PID(object):
    def __init__(
        self,
        base: Base,
        kp: float,
        ki: float,
        kd: float,
    ):
        self.kp = kp
        self.ki = ki
        self.kd = kd
        self.base = base
        self.proportional = 0
        self.integral = 0
        self.derivative = 0
        self.last_error = 0
        self.loop = 0

    def reset_values(self):
        self.proportional = 0
        self.integral = 0
        self.derivative = 0
        self.last_error = 0
        self.loop = 0


class PID_LineTrack(PID):
    def __init__(self):
        PID.__init__(self, base, 0.07, 0.00, 0.80)

    def move(
        self,
        sensor: ColorSensor,
        speed: float,
        threshold: int,
        side=1,
        condition=lambda: True,
        reset=True,
    ):
        self.reset_values()

        while condition():
            self.error = threshold - sensor.reflection()
            self.proportional = self.error * self.kp
            self.integral += self.error
            self.derivative = (self.error - self.last_error) * self.kd

            self.correction = (
                (self.integral * self.ki) + self.proportional + self.derivative
            )

            if self.loop < 200:
                self.base.run(
                    200 + side * self.correction, 200 - side * self.correction
                )
            else:
                self.base.run(
                    speed + (side * self.correction * 10),
                    speed - (side * self.correction * 10),
                )

            self.loop += 1
            self.last_error = self.error

        base.stop()


class PID_GyroStraight(PID):
    def __init__(self, gyro: GyroSensor):
        self.gyro = gyro
        PID.__init__(self, base, 0.70, 0.00, 0.00)

    def move(
        self,
        speed: float,
        threshold: int,
        condition=lambda: True,
        reset=True,
    ):
        self.reset_values()

        while condition():
            self.error = threshold - self.gyro.angle()
            self.proportional = self.error * self.kp
            self.integral += self.error
            self.derivative = (self.error - self.last_error) * self.kd

            self.correction = (
                (self.integral * self.ki) + self.proportional + self.derivative
            )

            self.base.run(
                speed + (self.correction * 10), speed - (self.correction * 10)
            )
            self.last_error = self.error

        base.stop()


class PID_GyroTurn(PID):
    def __init__(self, gyro: GyroSensor):
        self.gyro = gyro
        PID.__init__(self, base, 0.86, 0.000005, 0.0004)

    def turn(self, threshold: int):
        self.reset_values()

        while self.gyro.angle() != threshold:
            self.error = threshold - self.gyro.angle()
            self.proportional = self.error * self.kp
            self.integral += self.error
            self.derivative = (self.error - self.last_error) * self.kd

            self.correction = (
                (self.integral * self.ki) + self.proportional + self.derivative
            )

            base.run(self.correction * 10, -(self.correction * 10))

        base.stop()

    def single_motor_turn(
        self,
        threshold: int,
        left_speed: int,
        right_speed: int,
        kp=1.00,
        ki=0.000005,
        kd=0.0004,
    ):
        self.reset_values()
        self.kp = kp
        self.ki = ki
        self.kd = kd

        while self.gyro.angle() != threshold:
            self.error = threshold - self.gyro.angle()
            self.proportional = self.error * self.kp
            self.integral += self.error
            self.derivative = (self.error - self.last_error) * self.kd

            self.correction = (
                (self.integral * self.ki) + self.proportional + self.derivative
            )

            if left_speed == 0:
                base.run(
                    0,
                    -(self.correction * 10),
                )
            elif right_speed == 0:
                base.run(
                    self.correction * 10,
                    0,
                )
            elif abs(left_speed) > abs(right_speed):
                print(right_speed / left_speed)

                base.run(
                    (self.correction * 10),
                    (-(right_speed / left_speed) * self.correction * 10),
                )
            elif abs(left_speed) < abs(right_speed):
                print(left_speed / right_speed)
                base.run(
                    (-(left_speed / right_speed) * self.correction * 10),
                    (-self.correction * 10),
                )

            print(left_motor.speed(), right_motor.speed())

        base.stop()
