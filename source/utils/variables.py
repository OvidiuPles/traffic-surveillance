PIXELS_UPPER_CNT_LINE = 250  # number of pixels upper than mid of image, used for vehicle counting line
THIRD_LINE = 1000  # third line on the road from right to left, only used for reading zone

STREAM_WIDTH = 1200
STREAM_HEIGHT = 700

# distance used for conditioning IOU calculation
MAX_DIST_TRACKING_X = 300
MAX_DIST_TRACKING_Y = 600

MAX_ID = 100
MAX_READING_ATTEMPTS = 2

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

DEFAULT_FRAME_HEIGHT = 2160

LINE1_PT1 = (2500, 0)
LINE1_PT2 = (3950, DEFAULT_FRAME_HEIGHT)

LINE2_PT1 = (2030, 0)
LINE2_PT2 = (2290, DEFAULT_FRAME_HEIGHT)

LINE3_PT1 = (1660, 0)
LINE3_PT2 = (1160, DEFAULT_FRAME_HEIGHT)

LINE4_PT1 = (1370, 0)
LINE4_PT2 = (75, DEFAULT_FRAME_HEIGHT)

LINE5_PT1 = (1100, 0)
LINE5_PT2 = (0, int(DEFAULT_FRAME_HEIGHT / 2 + 70))

LINE6_PT1 = (800, 0)
LINE6_PT2 = (0, int(DEFAULT_FRAME_HEIGHT / 4))

