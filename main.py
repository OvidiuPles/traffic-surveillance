import multiprocessing

import pyqtgraph as pg

from source.gui.main_gui import MainGUI


def main_app():
    app = pg.mkQApp()
    window = MainGUI()
    window.show()
    app.exec()


if __name__ == "__main__":
    # first two predictions of the yolo vehicles model open a new gui when running in exe, original gui is not responding until the second is closed
    # freeze support is a fix for now, takes longer for the first predictions to execute but then works fine, also works fine as a python script
    # https://github.com/ultralytics/ultralytics/issues/3997
    multiprocessing.freeze_support()
    process = multiprocessing.Process(target=main_app)
    process.start()
    process.join()
