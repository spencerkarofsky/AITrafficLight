"""
AI-Controlled Traffic Light
Spencer Karofsky

predict.py draws bounding boxes around all COCO class objects, using the pretrained YOLOv8 model with their corresponding labels.
The program then counts the amount of vehicles (cars, trucks, motorcycles, and buses) and writes this amount along with the date and time to a gen>
"""
from ultralytics import YOLO
import cv2
import datetime
import os
import RPi.GPIO as GPIO
from time import sleep
import pandas as pd
import sys
import time

# Variables and Constants:

# LED pins
# reds = [None,None,None,None]
# greens = [None, None, None, None]
# yellows = [None, None,None,None]

# Constants

GEAR_RATIO = 8
SLEEP_TIME = 0.002 # seconds
STEP_ANGLE = 5.625

LIGHT_CONSTANT = 2 # time, in seconds, per vehicle, of green light time

#assign GPIO pins for motor
motor_channel = (29,31,33,35)

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
#for defining more than 1 GPIO channel as input/output use
GPIO.setup(motor_channel, GPIO.OUT)

dataframe_columns = ['Date/Time','Side 1', 'Side 2', 'Side 3', 'Side 4']
traffic_dataframe = pd.DataFrame(columns=dataframe_columns)

# load pretrained YOLOv8 model on MS COCO dataset
model = YOLO("yolov8n.pt")

'''
Inputs: d, the number of degrees
Returns: none
rotate_clock rotates the stepper motor d degrees clockwise.
'''
def rotate_clock(d):
    steps = int(GEAR_RATIO*(d/STEP_ANGLE))
    for i in range(steps):
        GPIO.output(motor_channel, (GPIO.HIGH,GPIO.LOW,GPIO.LOW,GPIO.HIGH))
        sleep(SLEEP_TIME)
        GPIO.output(motor_channel, (GPIO.HIGH,GPIO.HIGH,GPIO.LOW,GPIO.LOW))
        sleep(SLEEP_TIME)
        GPIO.output(motor_channel, (GPIO.LOW,GPIO.HIGH,GPIO.HIGH,GPIO.LOW))
        sleep(SLEEP_TIME)
        GPIO.output(motor_channel, (GPIO.LOW,GPIO.LOW,GPIO.HIGH,GPIO.HIGH))
        sleep(SLEEP_TIME)

'''
Inputs: d, the number of degrees
Returns: none
rotate_clock rotates the stepper motor d degrees clockwise.
'''
def rotate_count_clock(d):
    steps = int(GEAR_RATIO*(d/STEP_ANGLE))
    for i in range(steps):
        GPIO.output(motor_channel, (GPIO.HIGH,GPIO.LOW,GPIO.LOW,GPIO.HIGH))
        sleep(SLEEP_TIME)
        GPIO.output(motor_channel, (GPIO.LOW,GPIO.LOW,GPIO.HIGH,GPIO.HIGH))
        sleep(SLEEP_TIME)
        GPIO.output(motor_channel, (GPIO.LOW,GPIO.HIGH,GPIO.HIGH,GPIO.LOW))
        sleep(SLEEP_TIME)
        GPIO.output(motor_channel, (GPIO.HIGH,GPIO.HIGH,GPIO.LOW,GPIO.LOW))
        sleep(SLEEP_TIME)
'''
Inputs: none
Returns: the picture
take_pic takes and saves a picture
'''
def take_pic():  # take picture using fswebcam command line tool
    return os.system('fswebcam -r 1000x600 -S 3 --jpeg 50 --save img.jpg')

'''
calculate_traffic_ratio compares the amount of vehicles on the roads. Sides 1 & 3 are opposite sides of the same street; same with Sides 2 & 4.
This function calculates the 2 average traffic amounts for the 2 street pairs and then returns a ratio of Sides 1 & 3 to Sides 2 & 4.
Inputs: data_row, a list where elements 1-4 are the 4 amounts of detected vehicles for each corresponding street.
Returns: ratio, the ratio of Street 1 to Street 2
'''
def calculate_traffic_ratio(data_row):
    # Calculate the average traffic amount for both streets
    street_1_average = (data_row[1] + data_row[3]) / 2
    street_2_average = (data_row[2] + data_row[4]) / 2
    ratio = street_1_average / street_2_average
    return ratio

'''
Inputs: None
Returns: vehicles, the total number of vehicles detected on the road.
calculate_total_vehicles calculates the total amount of vehicles on the road.
'''
def calculate_total_vehicles():
    # Calculate the average traffic amount for both streets
    vehicles = data_row[1] + data_row[2] + data_row[3] + data_row[4]
    return vehicles

'''
Inputs:
Returns: vehicle_count, the number of vehicles detected in the frame
get_vehicle_count uses the Ultralytics API's YOLOv8 model to count the number of vehicles (cars, busses, motorcycles, and trucks)
'''
def get_vehicle_count():
    frame = cv2.imread('img.jpg')

    results = model(frame)  # return a list of Results objects

    # Process results list
    for result in results:
        cls = result.boxes.cls

    class_names = result.names  # dictionary of COCO classes

    for i in range(len(cls)):
        # count the number of cars, motorcycles, busses, and trucks
        vehicle_count = 0
        for j in range(len(results[0])):
            label = class_names.get(int(cls[j]))
            if label == 'car' or label == ' motorcycle' or label == 'truck' or label == 'bus':
                vehicle_count += 1
    return vehicle_count


def main():
    with open('traffic.txt','w') as f:
        f.write('Traffic Log\n\n')

    while True:
        # Create new data row
        data_row = []
        # For the first column in data_row, 'Date/Time', add the date and time using the datetime module
        data_row.append(str(datetime.datetime.now()))

        # The motor will rotate 90 degrees 4 times to capture the 4 different streets/views before turning back 360 degrees
        for turn in range(4):
            rotate_clock(90)
            take_pic()
            frame = cv2.imread('img.jpg')

            # Get the number of vehicles in the frame by calling the get_vehicle_count function.
            vehicle_count = get_vehicle_count(frame)

            # Append traffic_count value to data_row list (to later be added to the traffic_dataframe)
            data_row.append(vehicle_count)

        # Add the new data as a row to the DataFrame
        traffic_dataframe.loc[len(traffic_dataframe)] = data_row

        # Dictate Traffic Logic:
        num_vehicles = calculate_total_vehicles()
        # Case 1: All sides have less than 2 cars; intersection will act as a 4-way stop.
        if data_row[1] <= 2 and data_row[2] <= 2 and data_row[3] <= 2 and data_row[3] <= 2:
            # turn all greens and yellows off; all reds  blink to signal 4-way stop
            pass
        # Case 2: some sides have more than 2 cars, so the ratio between the 2 streets will be calculated using the calculate_traffic_ratio function.
        # That ratio will then be used to determine the timing of the lights.
        else:
            ratio = calculate_traffic_ratio(data_row)
            # Case A: Street 2 has more traffic than Street 1; Street 2 gets green light priority
            if ratio < 1:
                # set street 1 lights (green[0] and green[3]) to green and street 2 lights to red.
                pass
            # Case B: Street 1 has more traffic than Street 2; Street 1 gets green light priority.
            elif ratio > 1:
                pass
            else:
                pass

        # Rotate Counter-Clockwise back to starting position
        rotate_count_clock(360)

main()


'''
Sources:
1) https://github.com/ultralytics/ultralytics
2) https://docs.ultralytics.com/usage/python/
3) https://docs.ultralytics.com/reference/engine/results/#ultralytics.engine.results.Boxes
4) https://www.geeksforgeeks.org/python-process-images-of-a-video-using-opencv/
5) https://docs.opencv.org/3.4/dc/da5/tutorial_py_drawing_functions.html
6) https://www.tutorialspoint.com/how-to-change-the-contrast-and-brightness-of-an-image-using-opencv-in-python
7) https://docs.python.org/3/library/datetime.html
8) https://www.electronicwings.com/raspberry-pi/stepper-motor-interfacing-with-raspberry-pi
'''
