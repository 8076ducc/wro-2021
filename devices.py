from pybricks.hubs import EV3Brick
from pybricks.ev3devices import (
    Motor,
    ColorSensor,
    GyroSensor,
)
from pybricks import nxtdevices
from pybricks.parameters import Port, Direction, Stop
from pybricks.iodevices import Ev3devSensor

ev3 = EV3Brick()

left_motor = Motor(Port.B, Direction.COUNTERCLOCKWISE)
right_motor = Motor(Port.C)
left_intake = Motor(Port.A, Direction.COUNTERCLOCKWISE)
right_intake = Motor(Port.D)

left_motor.control.limits(1500)
right_motor.control.limits(1500)
left_intake.control.limits(1500)
right_intake.control.limits(1500)

ht_color_sensor = Ev3devSensor(Port.S1)
left_color_sensor = ColorSensor(Port.S2)
right_color_sensor = ColorSensor(Port.S3)
gyro_sensor = GyroSensor(Port.S4)


class Base:
    def __init__(self):
        self.left_motor = left_motor
        self.right_motor = right_motor
        self.left_color_sensor = left_color_sensor
        self.right_color_sensor = right_color_sensor

    def brake(self):
        self.left_motor.brake()
        self.right_motor.brake()

    def hold(self, motor: Motor = None):
        if motor is None:
            self.left_motor.hold()
            self.right_motor.hold()
        else:
            motor.hold()

    def angle(self):
        return (self.left_motor.angle() + self.right_motor.angle()) / 2

    def reset_angle(self, angle: int = 0):
        self.left_motor.reset_angle(angle)
        self.right_motor.reset_angle(angle)

    def run(self, left_speed: float, right_speed: float):
        self.left_motor.run(left_speed)
        self.right_motor.run(right_speed)

    def run_time(self, left_speed, right_speed, time):
        left_motor.run_time(left_speed, time, wait=False, then=Stop.HOLD)
        right_motor.run_time(right_speed, time, wait=True, then=Stop.HOLD)

        base.brake()

    def run_target(self, left_speed, right_speed, left_angle, right_angle):
        base.reset_angle()

        left_motor.run_target(left_speed, left_angle, wait=False, then=Stop.HOLD)
        right_motor.run_target(right_speed, right_angle, wait=True, then=Stop.HOLD)

        base.brake()


base = Base()


class Intake:
    def __init__(self):
        self.left_intake = left_intake
        self.right_intake = right_intake

        self.left_car_color = None
        # 0: waiting, 1: parked
        self.left_car_type = None
        self.left_batteries = 0

        self.right_car_color = None
        # 0: waiting, 1: parked
        self.right_car_type = None
        self.right_batteries = 0

    def hold(self, motor: Motor = None):
        if motor is None:
            self.left_intake.hold()
            self.right_intake.hold()
        else:
            motor.hold()

    def reset(self):
        self.left_intake.reset_angle(0)
        self.right_intake.reset_angle(0)

    def run(self, left_speed: float, right_speed: float):
        self.left_intake.run(left_speed)
        self.right_intake.run(right_speed)

    def stop(self):
        self.left_intake.brake()
        self.right_intake.brake()

    def open(self, motor: Motor = None):
        if motor is None:
            self.left_intake.run(1500)
            self.right_intake.run(1500)
        else:
            motor.run(1500)

    def close(self, motor: Motor = None):
        if motor is None:
            self.left_intake.run(-1500)
            self.right_intake.run(-1500)
        else:
            motor.run(-1500)

    def run_time(self, speed, time, motor: Motor = None):

        if motor is None:
            left_intake.run_time(speed, time, wait=False, then=Stop.HOLD)
            right_intake.run_time(speed, time, wait=True, then=Stop.HOLD)
        else:
            motor.run_time(speed, time, then=Stop.HOLD)

    def run_target(self, speed, angle, motor: Motor = None):
        if motor is None:
            left_intake.run_target(speed, angle, then=Stop.HOLD)
            right_intake.run_target(speed, angle, then=Stop.HOLD)
        else:
            motor.run_target(speed, angle, then=Stop.HOLD)

        base.brake()

    def update_left_possessions(
        self,
        car_color=None,
        car_type=None,
        number_of_batteries=None,
    ):
        self.left_car_color = car_color
        self.left_car_type = car_type
        if number_of_batteries is not None:
            self.left_batteries = number_of_batteries

    def update_right_possessions(
        self,
        car_color=None,
        car_type=None,
        number_of_batteries=None,
    ):
        self.right_car_color = car_color
        self.right_car_type = car_type
        if number_of_batteries is not None:
            self.right_batteries = number_of_batteries


intake = Intake()


class Sensors:
    def __init__(self):
        self.ht_color_sensor = ht_color_sensor
        self.left_color_sensor = left_color_sensor
        self.right_color_sensor = right_color_sensor
        self.gyro_sensor = gyro_sensor

    def calibrate_rli(self, sensor: ColorSensor):
        while True:
            ev3.screen.print(sensor.reflection())
            print(sensor.reflection())

    def calibrate_rgb(self, sensor: ColorSensor):
        while True:
            r, g, b = sensor.rgb()
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


sensors = Sensors()
