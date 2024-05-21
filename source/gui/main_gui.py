import sys

import cv2
from PySide6.QtGui import QPixmap, QImage
from PySide6.QtWidgets import QApplication, QLabel, QMainWindow

from source.gui.generated.main_window import Ui_MainWindow
from source.processing.analyzer import Analyzer


#  pyside6-uic source/gui/generated/main_window.ui -o source/gui/generated/main_window.py


class MainGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.gui = Ui_MainWindow()
        self.gui.setupUi(self)

        self.gui.pushButton.clicked.connect(self.on_button_click)

        label = QLabel()
        label.setScaledContents(True)
        self.gui.image_layout.addWidget(label)
        label.setPixmap(QPixmap(r"C:\Licenta\traffic-surveillance-backend\source\gui\images\background_stream.png"))
        self.analyzer = Analyzer(stream_output=label)

        #  self.put_image(r'C:\Licenta\data\raw_data\videos\wtf\video_6_processed.mp4_frame_312.jpg')

    def on_button_click(self):
        self.analyzer.process_stream(r"C:\Licenta\data\raw_data\videos\video_5.mp4")

    def put_image(self, path):
        label = QLabel()
        pixmap = QPixmap(path)
        label.setPixmap(pixmap)
        label.setScaledContents(True)
        self.gui.image_layout.addWidget(label)
