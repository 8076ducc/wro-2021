#!/usr/bin/env pybricks-micropython
from pybricks.hubs import EV3Brick
import pybricks.ev3devices
from pybricks.ev3devices import (Motor, TouchSensor,
                                 InfraredSensor, UltrasonicSensor, GyroSensor)
import pybricks.nxtdevices
from pybricks.parameters import Port, Stop, Direction, Button, Color
from pybricks.tools import wait, StopWatch, DataLog
from pybricks.robotics import DriveBase
from pybricks.media.ev3dev import SoundFile, ImageFile
from pybricks.iodevices import Ev3devSensor

import calibrate.py


# This program requires LEGO EV3 MicroPython v2.0 or higher.
# Click "Open user guide" on the EV3 extension tab for more information.


# Create your objects here.
ev3 = EV3Brick()

left_motor = Motor(Port.B)
right_motor = Motor(Port.C, Direction.COUNTERCLOCKWISE)
left_intake = Motor(Port.A)
right_intake = Motor(Port.D)

# nxt_color_sensor = pybricks.nxtdevices.ColorSensor(Port.S1)
ht_color_sensor = Ev3devSensor(Port.S1)
left_color_sensor = pybricks.ev3devices.ColorSensor(Port.S2)
right_color_sensor = pybricks.ev3devices.ColorSensor(Port.S3)
gyro_sensor = GyroSensor(Port.S4)

car_order = []

def pid_color(threshold: int, speed: int, sensor: int, target: int):
    kp = 0.07
    ki = 0.000
    kd = 0.8

    proportional = 0.0
    integral = 0.0
    derivative = 0.0

    last_error = 0.0
    error = 0.0
    
    if sensor == 2:
        target_sensor = right_color_sensor
    elif sensor == 3:
        target_sensor = left_color_sensor
    
    loop = 0

    # while target_sensor.reflection() != target:
    while True:
    
        if sensor == 2:
            reading = left_color_sensor.reflection()
        elif sensor == 3:
            reading = right_color_sensor.reflection()

        error = threshold - reading
        proportional = error * kp
        integral += error
        derivative = (error - last_error) * kd

        correction = (integral * ki) + proportional + derivative
        
        if loop <= 400:
            left_motor.run(200 - (correction * 10))
            right_motor.run(200 + (correction * 10))
        else:
            left_motor.run(speed - (correction * 10))
            right_motor.run(speed + (correction * 10))

        last_error = error
        
        loop += 1

def pid_gyro_straight_angle(threshold: float, speed: float, target: int):
    kp = 0.7
    ki = 0.0
    kd = 0.0

    proportional = 0.0
    integral = 0.0
    derivative = 0.0

    last_error = 0.0
    error = 0.0
    
    left_motor.reset_angle(0)
    right_motor.reset_angle(0)

    while right_motor.angle() < target:
        
        error = threshold - gyro_sensor.angle()
        # speed_percentage = 1 - (right_motor.angle() / target)
        proportional = error * kp
        integral += error
        derivative = (error - last_error) * kd

        correction = (integral * ki) + proportional + derivative
        left_motor.run(speed - (correction * 10))
        right_motor.run(speed + (correction * 10))

        last_error = error
        
    brake()
        
def detect_cars():
    
    last_color = None
    
    # all unneeded wrong
    red_lower = (60, 7, 13)
    green_lower = (10, 30, 13)
    green_higher = (18, 40, 22)
    blue_lower = (13, 23, 60)
    
    right_motor.reset_angle(0)
    
    kp = 0.07
    ki = 0.000
    kd = 0.8

    proportional = 0.0
    integral = 0.0
    derivative = 0.0

    last_error = 0.0
    error = 0.0
    
    loop = 0
    
    reading = left_color_sensor.reflection()
        
    threshold = 32
    speed = 200
    
    while len(car_order) < 5:

        error = threshold - reading
        proportional = error * kp
        integral += error
        derivative = (error - last_error) * kd

        correction = (integral * ki) + proportional + derivative
        
        if loop <= 400:
            left_motor.run(200 + (correction * 10))
            right_motor.run(200 - (correction * 10))
        else:
            left_motor.run(speed + (correction * 10))
            right_motor.run(speed - (correction * 10))

        last_error = error
        
        loop += 1
        
        if right_motor.angle() > 120:
        
            color = None
        
            if 60 < ht_color_sensor.read('RGB')[0]:
                print(ht_color_sensor.read('RGB'))
                color = Color.RED
            elif 60 < ht_color_sensor.read('RGB')[2]:
                print(ht_color_sensor.read('RGB'))
                color = Color.BLUE
            else:
                print(ht_color_sensor.read('RGB'))
                color = Color.GREEN

            car_order.append(color)

            print(color)

            if color == Color.BLUE:
                # blue
                ev3.speaker.beep(frequency=600, duration=100)
            elif color == Color.GREEN:
                # green
                ev3.speaker.beep(frequency=700, duration=100)
            elif color == Color.RED:
                # red
                ev3.speaker.beep(frequency=800, duration=100)

            last_color = color
            
            right_motor.reset_angle(0)

    brake()
    print(car_order)
        
def brake():
    left_motor.brake()
    right_motor.brake()

# Write your program here.
ev3.speaker.beep()
gyro_sensor.reset_angle(0)

detect_cars()
