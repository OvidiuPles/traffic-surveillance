import os

import cv2
from easyocr import easyocr
from ultralytics import YOLO

from source.utils.colors import class_colors

plates_model_path = os.path.join('.', 'runs', 'detect', 'train18', 'weights', 'last.pt')
number_plates_model = YOLO(plates_model_path)
reader = easyocr.Reader(['en'])  # Use English language

frame = cv2.imread(r"C:\Licenta\data\plate_recognition\data\images\train\frame_1.jpg")
results = number_plates_model(frame)[0]
x1, y1, x2, y2, score, class_id = results.boxes.data.tolist()[0]
x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
cropped_plate = frame[y1:y2, x1:x2]

plate_gray = cv2.cvtColor(cropped_plate, cv2.COLOR_BGR2GRAY)
_, plate_thresh = cv2.threshold(plate_gray, 100, 255, cv2.THRESH_BINARY_INV)
string_result = reader.readtext(plate_gray)
print(string_result[0][1].upper())
print(str('000'))


cv2.imshow("ok", plate_thresh)
cv2.waitKey(0)
