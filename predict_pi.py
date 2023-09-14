"""
AI-Controlled Traffic Light
Spencer Karofsky

predict.py draws bounding boxes around all COCO class objects, using the pretrained YOLOv8 model with their corresponding labels.
The program then counts the amount of vehicles (cars, trucks, motorcycles, and buses) and writes this amount along with the date and time to a gen>
"""
import cv2
import datetime
import os
import Detector
import Motor
import TrafficLight
import random


# Constants
VEHICLE_TIME_CONSTANT = 2  # time, in seconds, per vehicle, of green light time

# Functions
'''
take_pic()
Inputs: none
Returns: the picture
Takes and saves a picture
'''
def take_pic():  # take picture using fswebcam command line tool
    return os.system('fswebcam -r 1000x600 -S 3 --jpeg 50 --save img.jpg')

def main():
    # Create instance of Detector class
    detector = Detector()

    # Create instance of Motor class to represent the stepper motor
    motor_channel = (29, 31, 33, 35)
    motor = Motor(motor_channel)

    # Create instance of a TrafficLight class
    traffic_light = TrafficLight()


    while True:
        # Create new data row
        data_row = []
        # For the first column in data_row, 'Date/Time', add the date and time using the datetime module
        data_row.append(str(datetime.datetime.now()))

        # Create traffic queue to store priority of street light
        traffic_queue = []

        # The motor will rotate 90 degrees 4 times to capture the 4 different streets/views before turning back 360 degrees
        for turn in range(4):
            motor.rotate_clock(90)
            take_pic()
            frame = cv2.imread('img.jpg')

            # Get the number of vehicles in the frame by calling the detect_objects Detector method
            detections = detector.detect_objects(frame)

            # Get number of vehicles from detections list
            vehicle_count = 0
            for object in detections:
                if object in ["car", "motorcycle","bus","truck"]:
                    vehicle_count += 1

            # Append traffic_count value to data_row list (to later be added to the traffic_dataframe)
            data_row.append(vehicle_count)

        # Add the new data as a row to the DataFrame
        traffic_light.append_data_row(data_row)

        # Set the traffic lights based on the data
        traffic_light.set_traffic_lights()

        # Rotate Counter-Clockwise back to starting position
        motor.rotate_count_clock(360)

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
