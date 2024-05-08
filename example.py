import time
import cv2
import easyocr

import pyopencl as cl
import torch



reader = easyocr.Reader(['en'], gpu=True)  # Use English language
frame = cv2.imread(r'C:\Users\Ovi Carici\OneDrive - Technical University of Cluj-Napoca\Desktop\w\z.jpg')

frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
#_, frame_thresh = cv2.threshold(frame_gray, 138, 255, cv2.THRESH_BINARY_INV)
frame_thresh = cv2.adaptiveThreshold(frame_gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY_INV, 11, 2)

avg_time = 0

result = reader.readtext(frame_thresh)

print(result[0][1])  # The detected text

cv2.imshow("1", frame)
cv2.imshow("2", frame_thresh)
cv2.waitKey(0)

# Output the recognized text

#  TODO: convert letter to numbers and vice versa as expected by number plates format!!!!


