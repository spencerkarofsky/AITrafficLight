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

        # Dictate Traffic Logic:
        num_vehicles = traffic_light.calculate_total_vehicles()

        # Case 1: All sides have less than 2 cars; intersection will act as a 4-way stop.
        if data_row[1] <= 2 and data_row[2] <= 2 and data_row[3] <= 2 and data_row[3] <= 2:
            # turn all greens and yellows off; all reds  blink to signal 4-way stop
            traffic_light.set_flash_red('Street 1')
            traffic_light.set_flash_red('Street 2')
        # Case 2: some sides have more than 2 cars, so the ratio between the 2 streets will be calculated using the calculate_traffic_ratio function.
        # That ratio will then be used to determine the timing of the lights.
        else:
            ratio = traffic_light.calculate_traffic_ratio(data_row)
            # Case A: Street 2 has more traffic than Street 1; Street 2 gets green light priority
            if ratio < 1:
                # Green light time = a constant * the average number of vehicles on a given street
                green_light_time = traffic_light.get_green_light_time('Side 2')

                # Set street 2 lights (green[1] and green[3]) to green and street 1 lights to red.


                traffic_queue.append(['Side 2','Side 4'],)
            # Case B: Street 1 has more traffic than Street 2; Street 1 gets green light priority.
            elif ratio > 1:
                # Green light time = a constant * the average number of vehicles on a given street
                green_light_time = traffic_light.get_green_light_time('Side 2')

                # Set street 1 lights (green[0] and green[2]) to green and street 2 lights to red.

            else:
                # The streets have equal traffic amounts.

                # If traffic_dataframe row is first row, randomly select street to get green light priority
                current_row_index = traffic_light.traffic_dataframe.index.get_loc(traffic_light.traffic_dataframe.index[0])
                if current_row_index == 0:
                    random_street = random.randint(1, 2)
                    if random_street == 1:
                        # Street 1 gets green light priority
                        green_light_time = traffic_light.get_green_light_time('Side 1')
                        # Set green and red lights
                    else:
                        # Street 2 gets green light priority
                        green_light_time = traffic_light.get_green_light_time('Side 2')
                        # Set green and red lights
                # Else, give green light priority to the last street to have red light.
                else:
                    if (traffic_light.traffic_dataframe.iloc[-2, 1] + traffic_light.traffic_dataframe.iloc[-2, 3]) > (traffic_light.traffic_dataframe.iloc[-2, 2] + traffic_light.traffic_dataframe.iloc[-2, 4]):
                        pass
                    else:
                        street_green = traffic_light.get_last_green()
                        traffic_light.set_green_light(street_green)
                        if street_green == 'Street 1':
                            traffic_light.set_red_light('Street 2')
                        else:
                            traffic_light.set_red_light('Street 1')

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
