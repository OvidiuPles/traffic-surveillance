import time
import cv2
import easyocr
import torch
import pyopencl as cl

#
# # Initialize EasyOCR with the desired language(s)


reader = easyocr.Reader(['en'], gpu=True)  # Use English language
frame = cv2.imread(r'C:\Users\Ovi Carici\OneDrive - Technical University of Cluj-Napoca\Desktop\w\x.png')


frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
_, frame_thresh = cv2.threshold(frame_gray, 138, 255, cv2.THRESH_BINARY_INV)


start = time.perf_counter()
result = reader.readtext(frame_thresh)
stop = time.perf_counter()

local_time = stop - start
print(f"time: {local_time}")


# Output the recognized text
print(result[0][1])  # The detected text

#  TODO: convert letter to numbers and vice versa as expected by number plates format!!!!


