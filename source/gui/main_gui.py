import sys
import time

import cv2
from PySide6.QtGui import QPixmap, QImage
from PySide6.QtWidgets import QApplication, QLabel, QMainWindow, QMessageBox

from source.gui.generated.main_window import Ui_MainWindow
from source.processing.analyzer import Analyzer


#  pyside6-uic source/gui/generated/main_window.ui -o source/gui/generated/main_window.py


class MainGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.gui = Ui_MainWindow()
        self.gui.setupUi(self)

        self.gui.start_stream_pushButton.clicked.connect(self.start_stream)
        self.gui.stop_stream_pushButton.clicked.connect(self.stop_stream)
        self.stream_output = QLabel()
        self.stream_output.setScaledContents(True)
        self.gui.image_layout.addWidget(self.stream_output)
        self.stream_output.setPixmap(QPixmap(r"C:\Licenta\traffic-surveillance-backend\source\gui\images\background_stream.png"))
        self.analyzer = Analyzer(stream_output=self.stream_output)

    def closeEvent(self, event):
        self.analyzer.stop_stream = True
        #  TODO: uncomment
        # response = QMessageBox.question(self, 'Quit', "Are you sure you want to quit?", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        # if response == QMessageBox.Yes:
        #     event.accept()
        # else:
        #     event.ignore()

    def start_stream(self):
        self.analyzer.process_stream(fr"{self.gui.stream_input_lineEdit.text()}")
        self.stop_stream()

    def stop_stream(self):
        self.analyzer.stop_stream = True
        self.stream_output.setPixmap(QPixmap(r"C:\Licenta\traffic-surveillance-backend\source\gui\images\background_stream.png"))

    def put_image(self, path):
        label = QLabel()
        pixmap = QPixmap(path)
        label.setPixmap(pixmap)
        label.setScaledContents(True)
        self.gui.image_layout.addWidget(label)
