"""
AI-Controlled Traffic Light
Spencer R. Karofsky
"""
import cv2
import datetime
from Detector import Detector
from TrafficLight import TrafficLight
import math


def tester():
    # Create instance of Detector class
    detector = Detector()

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

            img_name = "./test_images/" + str(random.randint(1,13) + ".jpg"
            print(img_name)
            frame = cv2.imread(img_name)

            # Get the number of vehicles in the frame by calling the detect_objects Detector method
            detections = detector.detect_objects(frame)

            # Get number of vehicles from detections list
            vehicle_count = 0
            for object in detections:
                if object in ['car', 'motorcycle','bus','truck']:
                    vehicle_count += 1

            # vehicle_count is the true amount of vehicles squared. to get the true count, take the square root
            vehicle_count = int(math.sqrt(vehicle_count))

            # Append traffic_count value to data_row list (to later be added to the traffic_dataframe)
            data_row.append(vehicle_count)

        # Add the new data as a row to the DataFrame
        traffic_light.append_data_row(data_row)

        # Set the traffic lights based on the data
        traffic_light.set_traffic_lights()

tester()
