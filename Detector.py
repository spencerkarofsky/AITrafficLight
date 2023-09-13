'''
Detector Class
This class creates an object that detects object
'''
from ultralytics import YOLO

class Detector:
    # Constructor
    def __init__(self):
        # Load pretrained YOLOv8 model on MS COCO dataset
        model = YOLO("yolov8n.pt")

    # Methods

    def detect_objects(self,frame):
        # Declare objects list, which will store the detections
        objects = []

        # return a list of Results objects
        detections = self.model(frame)

        # Process results list
        for detection in detections:
            cls = detection.boxes.cls

        # Dictionary of COCO classes
        class_names = detection.names

        for i in range(len(cls)):
            # Append each detection to list
            for j in range(len(detections[0])):
                label = class_names.get(int(cls[j]))
                objects.append(label)
        return objects


