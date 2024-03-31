import time
import cv2
import easyocr

import pyopencl as cl
import torch



reader = easyocr.Reader(['en'], gpu=True)  # Use English language
frame = cv2.imread(r'C:\Users\Ovi Carici\OneDrive - Technical University of Cluj-Napoca\Desktop\w\x.png')


frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
_, frame_thresh = cv2.threshold(frame_gray, 138, 255, cv2.THRESH_BINARY_INV)

if not torch.cuda.is_available():
    print("ok")
avg_time = 0
for i in range(1, 1000):
    print("i="+str(i))
    start = time.perf_counter()
    result = reader.readtext(frame_thresh)
    stop = time.perf_counter()

    local_time = stop - start
    avg_time += local_time
    print(f"time: {local_time}")
print(f"avg time: {avg_time}")


cv2.imshow("1", frame)
cv2.imshow("2", frame_thresh)
cv2.waitKey(0)

# Output the recognized text
print(result[0][1])  # The detected text

#  TODO: convert letter to numbers and vice versa as expected by number plates format!!!!


