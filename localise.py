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


class ParkingLot:
    def __init__(
        self, x: int, y: int, barrier: bool, parked_color: Color, parked_type: int
    ):
        self.x = x
        self.y = y
        self.barrier = barrier
        self.parked_color = parked_color
        self.parked_type = parked_type

    def update(self, barrier: bool, parked_color: Color, parked_type: int):
        if barrier != None:
            self.barrier = barrier

        if parked_color != None:
            self.parked_color = parked_color

        if parked_type != None:
            self.parked_type = parked_type


red_parking = [
    ParkingLot(2, 0, None, None, None),
    ParkingLot(1, 2, None, None, None),
    ParkingLot(0, 4, None, None, None),
    ParkingLot(1, 4, None, None, None),
]

green_parking = [
    ParkingLot(2, 0, None, None, None),
    ParkingLot(1, 2, None, None, None),
    ParkingLot(0, 4, None, None, None),
    ParkingLot(1, 4, None, None, None),
]

blue_parking = [
    ParkingLot(0, 0, None, None, None),
    ParkingLot(1, 0, None, None, None),
    ParkingLot(3, 2, None, None, None),
    ParkingLot(3, 4, None, None, None),
]


# def find_closest_parking(color: Color):


# def go_to(x: int, y: int):
