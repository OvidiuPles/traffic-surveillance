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

        # processing options
        self.gui.boxes_checkBox.setChecked(self.analyzer.show_boxes)
        self.gui.boxes_checkBox.stateChanged.connect(self.toggle_boxes)

        self.gui.classes_checkBox.setChecked(self.analyzer.show_classes)
        self.gui.classes_checkBox.stateChanged.connect(self.toggle_classes)

        self.gui.number_plates_checkBox.setChecked(self.analyzer.show_number_plates)
        self.gui.number_plates_checkBox.stateChanged.connect(self.toggle_number_plates)

        self.gui.total_counting_checkBox.setChecked(self.analyzer.show_total_counting)
        self.gui.total_counting_checkBox.stateChanged.connect(self.toggle_total_counting)

        self.gui.class_counting_checkBox.setChecked(self.analyzer.show_class_counting)
        self.gui.class_counting_checkBox.stateChanged.connect(self.toggle_class_counting)

        self.gui.lane_counting_checkBox.setChecked(self.analyzer.show_lane_counting)
        self.gui.lane_counting_checkBox.stateChanged.connect(self.toggle_lane_counting)

        self.gui.lanes_checkBox.setChecked(self.analyzer.show_lanes)
        self.gui.lanes_checkBox.stateChanged.connect(self.toggle_lanes)

        self.gui.ids_checkBox.setChecked(self.analyzer.show_ids)
        self.gui.ids_checkBox.stateChanged.connect(self.toggle_ids)

        self.gui.counting_line_checkBox.setChecked(self.analyzer.show_counting_line)
        self.gui.counting_line_checkBox.stateChanged.connect(self.toggle_counting_line)

    def start_stream(self):
        self.analyzer.process_stream(fr"{self.gui.stream_input_lineEdit.text()}")
        self.stop_stream()

    def stop_stream(self):
        self.analyzer.stop_stream = True
        self.stream_output.setPixmap(QPixmap(r"C:\Licenta\traffic-surveillance-backend\source\gui\images\background_stream.png"))

    def toggle_boxes(self):
        if self.gui.boxes_checkBox.isChecked():
            self.analyzer.show_boxes = True
        else:
            self.analyzer.show_boxes = False

    def toggle_classes(self):
        if self.gui.classes_checkBox.isChecked():
            self.analyzer.show_classes = True
        else:
            self.analyzer.show_classes = False

    def toggle_number_plates(self):
        if self.gui.number_plates_checkBox.isChecked():
            self.analyzer.show_number_plates = True
        else:
            self.analyzer.show_number_plates = False

    def toggle_total_counting(self):
        if self.gui.total_counting_checkBox.isChecked():
            self.analyzer.show_total_counting = True
        else:
            self.analyzer.show_total_counting = False

    def toggle_class_counting(self):
        if self.gui.class_counting_checkBox.isChecked():
            self.analyzer.show_class_counting = True
        else:
            self.analyzer.show_class_counting = False

    def toggle_lane_counting(self):
        if self.gui.lane_counting_checkBox.isChecked():
            self.analyzer.show_lane_counting = True
        else:
            self.analyzer.show_lane_counting = False

    def toggle_lanes(self):
        if self.gui.lanes_checkBox.isChecked():
            self.analyzer.show_lanes = True
        else:
            self.analyzer.show_lanes = False

    def toggle_ids(self):
        if self.gui.ids_checkBox.isChecked():
            self.analyzer.show_ids = True
        else:
            self.analyzer.show_ids = False

    def toggle_counting_line(self):
        if self.gui.counting_line_checkBox.isChecked():
            self.analyzer.show_counting_line = True
        else:
            self.analyzer.show_counting_line = False

    def closeEvent(self, event):
        #  TODO: uncomment
        # response = QMessageBox.question(self, 'Quit', "Are you sure you want to quit?", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        # if response == QMessageBox.Yes:
        #     event.accept()
              self.analyzer.stop_stream = True
        # else:
        #     event.ignore()