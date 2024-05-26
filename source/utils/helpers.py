import os
import sys


# paths are different if app is running in one file exe
def get_vehicles_model_path():
    try:
        path = os.path.join(sys._MEIPASS, 'runs', 'detect', 'train11', 'weights', 'last.pt')
    except AttributeError:
        path = os.path.join('.', '.', '.', 'runs', 'detect', 'train11', 'weights', 'last.pt')
    return path


def get_plates_model_path():
    try:
        path = os.path.join(sys._MEIPASS, 'runs', 'detect', 'train18', 'weights', 'last.pt')
    except AttributeError:
        path = os.path.join('.', '.', '.', 'runs', 'detect', 'train18', 'weights', 'last.pt')
    return path


def get_stream_background_path():
    try:
        path = os.path.join(sys._MEIPASS, 'background_stream.png')
    except AttributeError:
        path = os.path.join('.', '.', 'source', 'gui', 'images', 'background_stream.png')
    return path
