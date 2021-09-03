from pybricks.hubs import EV3Brick
from pybricks.ev3devices import (
    Motor,
    TouchSensor,
    InfraredSensor,
    ColorSensor,
    UltrasonicSensor,
    GyroSensor,
)
from pybricks.parameters import Port, Stop, Direction, Button, Color
from pybricks.tools import wait, StopWatch, DataLog
from pybricks.robotics import DriveBase
from pybricks.media.ev3dev import SoundFile, ImageFile
from pybricks.iodevices import Ev3devSensor
# from enum import Enum

ev3 = EV3Brick()

left_motor = Motor(Port.B, Direction.COUNTERCLOCKWISE)
right_motor = Motor(Port.C)
left_intake = Motor(Port.A, Direction.COUNTERCLOCKWISE)
right_intake = Motor(Port.D)

ht_color_sensor = Ev3devSensor(Port.S1)
left_color_sensor = ColorSensor(Port.S2)
right_color_sensor = ColorSensor(Port.S3)
gyro_sensor = GyroSensor(Port.S4)


class Base:
    def __init__(
        self,
        left_motor: Motor,
        right_motor: Motor,
        left_color_sensor: ColorSensor,
        right_color_sensor: ColorSensor,
    ):
        self.left_motor = left_motor
        self.right_motor = right_motor
        self.left_color_sensor = left_color_sensor
        self.right_color_sensor = right_color_sensor

    def stop(self):
        self.left_motor.brake()
        self.right_motor.brake()

    def hold(self):
        self.left_motor.hold()
        self.right_motor.hold()

    def reset(self):
        self.left_motor.reset_angle(0)
        self.right_motor.reset_angle(0)

    def run(self, left_speed: float, right_speed: float):
        self.left_motor.run(left_speed)
        self.right_motor.run(right_speed)


base = Base(left_motor, right_motor, left_color_sensor, right_color_sensor)


class Intake:
    def __init__(self, left_intake: Motor, right_intake: Motor):
        self.left_intake = left_intake
        self.right_intake = right_intake

    def hold(self):
        self.left_intake.hold()
        self.right_intake.hold()

    def reset(self):
        self.left_intake.reset_angle(0)
        self.right_intake.reset_angle(0)

    def run(self, left_speed: float, right_speed: float):
        self.left_intake.run(left_speed)
        self.right_intake.run(right_speed)

    def stop(self):
        self.left_intake.brake()
        self.right_intake.brake()

    def open(self):
        self.left_intake.run(1000)
        self.right_intake.run(1000)

    def close(self):
        self.left_intake.run(-1000)
        self.right_intake.run(-1000)

    def open_left(self):
        self.left_intake.run(1000)
        self.right_intake.hold()

    def open_right(self):
        self.left_intake.hold()
        self.right_intake.run(1000)

    def close_left(self):
        self.left_intake.run(-1000)
        self.right_intake.hold()

    def close_right(self):
        self.left_intake.hold()
        self.right_intake.run(-1000)


intake = Intake(left_intake, right_intake)


class IntakePossessions:
    def __init__(self, car_color: Color, car_type: int, battery: bool):
        self.car_color = car_color
        # 0: waiting, 1: parked
        self.car_type = car_type
        self.battery = battery

    def update(self, car_color=None, car_type=None, battery=None):
        self.car_color = car_color
        self.car_type = car_type
        if battery != None:
            self.battery = battery


left_intake_possessions = IntakePossessions(None, None, False)
right_intake_possessions = IntakePossessions(None, None, False)


class Sensors:
    def __init__(
        self,
        ht_color_sensor: Ev3devSensor,
        left_color_sensor: ColorSensor,
        right_color_sensor: ColorSensor,
        gyro_sensor: GyroSensor,
    ):
        self.ht_color_sensor = ht_color_sensor
        self.left_color_sensor = left_color_sensor
        self.right_color_sensor = right_color_sensor
        self.gyro_sensor = gyro_sensor

    def calibrate_rli(self, sensor: int):
        while True:
            if sensor == 2:
                ev3.screen.print(self.left_color_sensor.reflection())
                print(self.left_color_sensor.reflection())
            elif sensor == 3:
                ev3.screen.print(self.right_color_sensor.reflection())
                print(self.right_color_sensor.reflection())

    def calibrate_rgb(self, sensor: int):
        while True:
            if sensor == 2:
                r, g, b = self.left_color_sensor.rgb()
                ev3.screen.print(
                    "R: {0}\t G: {1}\t B: {2}".format(r, g, b), sep="", end="\n"
                )
                print("R: {0}\t G: {1}\t B: {2}".format(r, g, b), sep="", end="\n")
            elif sensor == 3:
                r, g, b = self.right_color_sensor.rgb()
                ev3.screen.print(
                    "R: {0}\t G: {1}\t B: {2}".format(r, g, b), sep="", end="\n"
                )
                print("R: {0}\t G: {1}\t B: {2}".format(r, g, b), sep="", end="\n")

    def calibrate_ht_rgb(self):
        while True:
            r, g, b, a = self.ht_color_sensor.read("RGB")
            ev3.screen.print(
                "R: {0}\t G: {1}\t B: {2} A: {3}".format(r, g, b, a), sep="", end="\n"
            )
            print(
                "R: {0}\t G: {1}\t B: {2} A: {3}".format(r, g, b, a), sep="", end="\n"
            )

    def calibrate_gyro(self):
        self.gyro_sensor.reset_angle(0)

        while True:
            ev3.screen.print(self.gyro_sensor.angle())
            print(self.gyro_sensor.angle())


sensors = Sensors(ht_color_sensor, left_color_sensor, right_color_sensor, gyro_sensor)
