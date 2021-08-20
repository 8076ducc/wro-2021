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

ev3 = EV3Brick()

left_motor = Motor(Port.B, Direction.COUNTERCLOCKWISE)
right_motor = Motor(Port.C)
left_intake = Motor(Port.A, Direction.COUNTERCLOCKWISE)
right_intake = Motor(Port.D)

# nxt_color_sensor = pybricks.nxtdevices.ColorSensor(Port.S1)
ht_color_sensor = Ev3devSensor(Port.S1)
left_color_sensor = pybricks.ev3devices.ColorSensor(Port.S2)
right_color_sensor = pybricks.ev3devices.ColorSensor(Port.S3)
gyro_sensor = GyroSensor(Port.S4)

# red 98 37 26
# green 31 56 45
# blue 28 43 73
red_waiting = [70, 0, 0]
green_waiting = [0, 50, 0]
blue_waiting = [0, 0, 60]

red_parked_red = []
red_parked_green = []
red_parked_blue = []

green_parked_red = []
green_parked_green = []
green_parked_blue = []

blue_parked_red = []
blue_parked_green = []
blue_parked_blue = []

red_parking = []
blue_parking = []
green_parking = []

# red 18 10 6
# green 15 15 15
# blue 9 12 20

red_parked = []
green_parked = []
blue_parked = []

car_order = []

robot_position = None
