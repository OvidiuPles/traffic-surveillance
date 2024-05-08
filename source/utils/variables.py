PIXELS_UPPER_CNT_LINE = 250  # number of pixels upper than mid of image, used for vehicle counting line
THIRD_LINE = 1000  # third line on the road from right to left

STREAM_WIDTH = 1200
STREAM_HEIGHT = 700

# distance used for conditioning IOU calculation
MAX_DIST_TRACKING_X = 300
MAX_DIST_TRACKING_Y = 600

MAX_ID = 100

dict_letter_to_figure = {
    'O': '0',
    'I': '1',
    'Z': '2',
    'J': '3',
    'A': '4',
    'S': '5',
    'G': '4',
    'T': '7',
    'B': '8',
    'U': '0',
    'R': '2',
}

dict_figure_to_letter = {
    '0': 'O',
    '1': 'I',
    '2': 'Z',
    '3': 'J',
    '4': 'G',
    '5': 'S',
    '6': 'G',
    '7': 'T',
    '8': 'B',
}
