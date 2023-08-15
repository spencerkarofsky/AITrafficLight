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

with open('traffic.txt','w') as f:
    f.write('Traffic Log\n\n')

# load pretrained YOLOv8 model on MS COCO dataset
model = YOLO("yolov8n.pt")

def take_pic(): # take picture using fswebcam command line tool
    return os.system('fswebcam -r 1000x600 -S 3 --jpeg 50 --save img.jpg')

take_pic()
frame = cv2.imread('img.jpg')


# Capture frame-by-frame
#frame = cv2.resize(frame,(1000,600))
#frame = cv2.convertScaleAbs(frame,alpha=1.5,beta=-50) # adjust contrast and brightness (alpha is contrast, beta is brightness)
results = model(frame)  # return a list of Results objects

# Process results list
for result in results:
    boxes = result.boxes.xyxy
    cls = result.boxes.cls
    probs = result.probs  # Probs object for classification outputs

class_names = result.names  # dictionary of COCO classes

for i in range(len(boxes)):  
    # count the number of cars, motorcycles, busses, and trucks
    traffic_count = 0
    for j in range(len(results[0])):
        label = class_names.get(int(cls[j]))
        if label == 'car' or label == ' motorcycle' or label == 'truck' or label == 'bus':
            traffic_count += 1
    with open('traffic.txt', 'a') as f:
        dt = str(datetime.datetime.now()) + ': ' # date and time
        f.write(dt)
        traffic = str(traffic_count) + ' vehicles\n'
        f.write(traffic)


'''
Sources:
1) https://github.com/ultralytics/ultralytics
2) https://docs.ultralytics.com/usage/python/
3) https://docs.ultralytics.com/reference/engine/results/#ultralytics.engine.results.Boxes
4) https://www.geeksforgeeks.org/python-process-images-of-a-video-using-opencv/
5) https://docs.opencv.org/3.4/dc/da5/tutorial_py_drawing_functions.html
6) https://www.tutorialspoint.com/how-to-change-the-contrast-and-brightness-of-an-image-using-opencv-in-python
7) https://docs.python.org/3/library/datetime.html
'''
