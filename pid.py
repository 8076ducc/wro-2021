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
                    speed + side * self.correction, speed - side * self.correction
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

            self.base.run(speed + self.correction, speed - self.correction)
            self.last_error = self.error

        base.stop()


class PID_GyroTurn(PID):
    def __init__(self, gyro: GyroSensor):
        self.gyro = gyro
        PID.__init__(self, base, 0.86, 0.000003, 0.0004)

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
