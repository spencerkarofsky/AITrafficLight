"""
AI-Controlled Traffic Light
Spencer Karofsky
"""
from ultralytics import YOLO
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image

model = YOLO("yolov8n.pt")  # load pretrained YOLOv8 model on COCO

#img = 'https://ultralytics.com/images/bus.jpg'
img = './Oxford-Street.jpg'
img = np.asarray(Image.open(img))


results = model(img)  # return a list of Results objects
# Process results list
for result in results:
    boxes = result.boxes.xyxy
    cls = result.boxes.cls
    probs = result.probs  # Probs object for classification outputs

class_names = result.names

for i in range(len(boxes)):
    width = boxes[i][2]-boxes[i][0]
    height = boxes[i][3]-boxes[i][1]
    x1 = boxes[i][0]
    y1 = boxes[i][1]
    label = class_names.get(int(cls[i]))
    rect = plt.Rectangle((x1, y1), width, height, fill=False, edgecolor=(0,1,0), linewidth=2)
    plt.gca().add_patch(rect)
    plt.text(x1, y1-5, label, fontsize=12, color=(0,1,0))

plt.imshow(img)
plt.show()


'''
Sources:
1) https://github.com/ultralytics/ultralytics
2) https://docs.ultralytics.com/usage/python/
3) https://docs.ultralytics.com/reference/engine/results/#ultralytics.engine.results.Boxes
4) 
'''
