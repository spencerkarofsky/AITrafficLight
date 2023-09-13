"""
Motor class represents a stepper motor and contains functionality to rotate motor clockwise and counter-clockwise
"""
import RPi.GPIO as GPIO
from time import sleep

class Motor:
    # Constants
    GEAR_RATIO = 8
    SLEEP_TIME = 0.002 # in seconds
    STEP_ANGLE = 5.625

    # Assign GPIO pins for motor
    motor_channel = (29,31,33,35)

    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BOARD)
    # For defining more than 1 GPIO channel as input/output use
    GPIO.setup(motor_channel, GPIO.OUT)

    # Constructor
    def __init__(self,p1,p2,p3,p4):
        # Assign GPIO pins for motor
        motor_channel = (p1, p2, p3, p4)

    '''
    Inputs: d, the number of degrees
    Returns: none
    rotate_clock rotates the stepper motor d degrees clockwise.
    '''
    def rotate_clock(self,d):
        steps = int(self.GEAR_RATIO * (d / self.STEP_ANGLE))
        for i in range(steps):
            GPIO.output(self.motor_channel, (GPIO.HIGH, GPIO.LOW, GPIO.LOW, GPIO.HIGH))
            sleep(self.SLEEP_TIME)
            GPIO.output(self.motor_channel, (GPIO.HIGH, GPIO.HIGH, GPIO.LOW, GPIO.LOW))
            sleep(self.SLEEP_TIME)
            GPIO.output(self.motor_channel, (GPIO.LOW, GPIO.HIGH, GPIO.HIGH, GPIO.LOW))
            sleep(self.SLEEP_TIME)
            GPIO.output(self.motor_channel, (GPIO.LOW, GPIO.LOW, GPIO.HIGH, GPIO.HIGH))
            sleep(self.SLEEP_TIME)
    '''
    Inputs: d, the number of degrees
    Returns: none
    rotate_count_clock rotates the stepper motor d degrees counter-clockwise.
    '''
    def rotate_count_clock(self,d):
        steps = int(self.GEAR_RATIO * (d / self.STEP_ANGLE))
        for i in range(steps):
            GPIO.output(self.motor_channel, (GPIO.HIGH, GPIO.LOW, GPIO.LOW, GPIO.HIGH))
            sleep(self.SLEEP_TIME)
            GPIO.output(self.motor_channel, (GPIO.LOW, GPIO.LOW, GPIO.HIGH, GPIO.HIGH))
            sleep(self.SLEEP_TIME)
            GPIO.output(self.motor_channel, (GPIO.LOW, GPIO.HIGH, GPIO.HIGH, GPIO.LOW))
            sleep(self.SLEEP_TIME)
            GPIO.output(self.motor_channel, (GPIO.HIGH, GPIO.HIGH, GPIO.LOW, GPIO.LOW))
            sleep(self.SLEEP_TIME)


