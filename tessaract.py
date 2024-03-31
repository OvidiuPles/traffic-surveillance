import time
import concurrent.futures
import cv2
import pytesseract
from PIL import Image
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
# Path to the image file
image_path = r'C:\Users\Ovi Carici\OneDrive - Technical University of Cluj-Napoca\Desktop\w\x.png'

# Open the image using PIL (Python Imaging Library)
# frame = cv2.imread(r'C:\Users\Ovi Carici\OneDrive - Technical University of Cluj-Napoca\Desktop\w\x.png')
# frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
# _, frame_thresh = cv2.threshold(frame_gray, 138, 255, cv2.THRESH_BINARY_INV)
# # Use pytesseract to perform OCR on the image


frame = Image.open(image_path)
frame = frame.resize((100, 30))


def read_image(x):
    #time.sleep(1)
    text = pytesseract.image_to_string(frame, lang='eng', config='--psm 7')


start = time.perf_counter()
with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
    futures = [executor.submit(read_image, i) for i in range(5)]
    concurrent.futures.wait(futures)
stop = time.perf_counter()
print(f"time:{stop-start}")
