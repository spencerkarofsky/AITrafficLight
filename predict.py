"""
AI-Controlled Traffic Light
Spencer Karofsky
"""
from ultralytics import YOLO
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
import cv2

model = YOLO("yolov8n.pt")  # load pretrained YOLOv8 model on COCO

img = './Oxford-Street.jpg'
img = np.asarray(Image.open(img))

results = model(img)  # return a list of Results objects

# Process results list
for result in results:
    boxes = result.boxes.xyxy
    cls = result.boxes.cls
    probs = result.probs  # Probs object for classification outputs

class_names = result.names # dictionary of COCO classes

for i in range(len(boxes)):
    # calculate bounding boxes
    x1 = boxes[i][0]
    y1 = boxes[i][1]
    x2 = boxes[i][2]
    y2 = boxes[i][3]
    width = x2-x1
    height = y2-y1
    # plot bounding box
    rect = plt.Rectangle((x1, y1), width, height, fill=False, edgecolor=(0,1,0), linewidth=2)
    plt.gca().add_patch(rect)
    # use class dictionary to convert integer to correpsponding label and add to plot
    label = class_names.get(int(cls[i]))
    plt.text(x1, y1-5, label, fontsize=12, color=(0,1,0))

# display the image
plt.imshow(img)
plt.show()


'''
Sources:
1) https://github.com/ultralytics/ultralytics
2) https://docs.ultralytics.com/usage/python/
3) https://docs.ultralytics.com/reference/engine/results/#ultralytics.engine.results.Boxes
4) 
'''
