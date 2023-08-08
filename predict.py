"""
AI-Controlled Traffic Light
Spencer Karofsky
"""
from ultralytics import YOLO
import numpy as np
import cv2

model = YOLO("yolov8n.pt")  # load pretrained YOLOv8 model on COCO

# Creating a VideoCapture object to read the video
cap = cv2.VideoCapture('highway.mp4')

# Loop until the end of the video
while (cap.isOpened()):

    # Capture frame-by-frame
    ret, frame = cap.read()
    frame = cv2.resize(frame,(1200,700))
    frame = cv2.convertScaleAbs(frame,alpha=1.5,beta=-50)
    results = model(frame)  # return a list of Results objects

    # Process results list
    for result in results:
        boxes = result.boxes.xyxy
        cls = result.boxes.cls
        probs = result.probs  # Probs object for classification outputs

    class_names = result.names  # dictionary of COCO classes

    for i in range(len(boxes)):
        # calculate bounding boxes
        x1 = int(boxes[i][0])
        y1 = int(boxes[i][1])
        x2 = int(boxes[i][2])
        y2 = int(boxes[i][3])
        width = x2 - x1
        height = y2 - y1
        cv2.rectangle(frame,(x1,y1),(x2,y2),(0,255,0),2)

        # use class dictionary to convert integer to correpsponding label and add to plot
        label = class_names.get(int(cls[i]))
        cv2.putText(frame,label,(x1,y1-5),cv2.FONT_HERSHEY_DUPLEX,.75 ,(0,255,0),2)


    # Display the resulting frame
    cv2.imshow('Frame', frame)
    # define q as the exit button
    if cv2.waitKey(25) & 0xFF == ord('q'):
        break

# release the video capture object
cap.release()
# Closes all the windows currently opened.
cv2.destroyAllWindows()


'''
Sources:
1) https://github.com/ultralytics/ultralytics
2) https://docs.ultralytics.com/usage/python/
3) https://docs.ultralytics.com/reference/engine/results/#ultralytics.engine.results.Boxes
4) https://www.geeksforgeeks.org/python-process-images-of-a-video-using-opencv/
5) https://docs.opencv.org/3.4/dc/da5/tutorial_py_drawing_functions.html
6) https://www.tutorialspoint.com/how-to-change-the-contrast-and-brightness-of-an-image-using-opencv-in-python
7) 
'''
