import threading

import torch
from PySide6.QtGui import QPixmap, Qt
from PySide6.QtWidgets import QLabel, QMainWindow, QMessageBox, QApplication

from source.gui.generated.main_window import Ui_MainWindow
from source.processing.analyzer import Analyzer
from source.utils.variables import STREAM_BACKGROUND_PATH


#  pyside6-uic source/gui/generated/main_window.ui -o source/gui/generated/main_window.py


class MainGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.gui = Ui_MainWindow()
        self.gui.setupUi(self)

        screen_width = 1150
        screen_height = 750
        self.setFixedSize(screen_width, screen_height)
        app = QApplication.instance()
        screen_size = app.primaryScreen().availableGeometry()
        screen_center = screen_size.center()
        self.move(screen_center.x() - screen_width * 0.5, screen_center.y() - screen_height * 0.5)

        self.analyzer = Analyzer(on_tracked_found=self.on_tracked_found)
        self.stream_output = QLabel()
        self.stream_output.setScaledContents(True)
        self.gui.image_layout.addWidget(self.stream_output)
        self.stream_output.setPixmap(QPixmap(STREAM_BACKGROUND_PATH))

        # buttons
        self.gui.start_stream_pushButton.clicked.connect(self.start_stream)
        self.gui.stop_stream_pushButton.clicked.connect(self.stop_stream)
        self.gui.track_plate_pushButton.clicked.connect(self.track_plate_number)
        self.gui.clear_tracking_pushButton.clicked.connect(self.clear_tracking)
        self.gui.process_video_pushButton.clicked.connect(self.process_video)

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

        # processing parameters
        self.gui.vehicles_confidence_spinBox.setValue(self.analyzer.vehicles_confidence)
        self.gui.tracking_depth_spinBox.setValue(self.analyzer.tracking_depth)
        self.gui.plates_confidence_spinBox.setValue(self.analyzer.plates_confidence)
        self.gui.reading_attempts_spinBox.setValue(self.analyzer.reading_attempts)

        self.gui.vehicles_confidence_spinBox.valueChanged.connect(self.change_vehicle_confidence)
        self.gui.tracking_depth_spinBox.valueChanged.connect(self.change_tracking_depth)
        self.gui.plates_confidence_spinBox.valueChanged.connect(self.change_plates_confidence)
        self.gui.reading_attempts_spinBox.valueChanged.connect(self.change_reading_attempts)

        if not torch.cuda.is_available():
            self.nonmodal_message("CUDA not available - defaulting to CPU. Note: This module is much faster with a GPU.")

    def start_stream(self):
        if self.gui.stream_input_lineEdit.text() == "0":
            stream_input = 0
        else:
            stream_input = fr"{self.gui.stream_input_lineEdit.text()}"
        self.analyzer.process_stream(stream_input, self.stream_output)
        self.stop_stream()

    def stop_stream(self):
        self.analyzer.stop_stream = True
        self.stream_output.setPixmap(QPixmap(STREAM_BACKGROUND_PATH))

    def process_video(self):
        video_input = fr"{self.gui.video_input_lineEdit.text()}"
        if self.gui.video_output_lineEdit.text() == "":
            video_output = None
        else:
            video_output = fr"{self.gui.video_output_lineEdit.text()}"
        generate_statistics = self.gui.generate_statistics_checkBox.isChecked()
        thread = threading.Thread(target=self.analyzer.process_video, args=(video_input, video_output, generate_statistics))
        thread.start()
        QMessageBox.information(self, 'Info', "Video processing started.", QMessageBox.Ok)
        thread.join()
        self.on_video_processing_end()

    def track_plate_number(self):
        if self.gui.tracked_plate_lineEdit.text() != "":
            plate_number = self.gui.tracked_plate_lineEdit.text()
            if plate_number not in self.analyzer.tracked_plate_numbers:
                self.analyzer.tracked_plate_numbers.append(plate_number)
                self.nonmodal_message(f"{plate_number} added to tracking list.")
            else:
                self.nonmodal_message(f"{plate_number} is already tracked.")
            self.gui.tracked_plate_lineEdit.setText("")
        else:
            self.nonmodal_message("Input plate number.")

    def clear_tracking(self):
        self.analyzer.clear_tracking_list()
        self.gui.tracked_plate_lineEdit.setText("")
        self.nonmodal_message("Tracking list is cleared.")

    def on_tracked_found(self, plate_number):
        self.nonmodal_message(f"{plate_number} found. Recording started. It can be found in root directory.")

    def on_video_processing_end(self):
        if self.analyzer.statistics_generated:
            self.nonmodal_message("Video processing ended.")
        else:
            self.nonmodal_message("Video processing ended. Statistics were not generated. Check video paths, close Excel and try again.")

    def nonmodal_message(self, text):
        # doesn't block the main window
        message = QMessageBox(self)
        message.setIcon(QMessageBox.Icon.Information)
        message.setWindowTitle("Info")
        message.setText(text)
        message.setStandardButtons(QMessageBox.StandardButton.Ok)
        message.setWindowModality(Qt.WindowModality.NonModal)
        message.show()

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

    def change_vehicle_confidence(self):
        self.analyzer.model_confidence = self.gui.vehicles_confidence_spinBox.value()

    def change_tracking_depth(self):
        self.analyzer.tracking_depth = self.gui.tracking_depth_spinBox.value()

    def change_plates_confidence(self):
        self.analyzer.plates_confidence = self.gui.plates_confidence_spinBox.value()

    def change_reading_attempts(self):
        self.analyzer.reading_attempts = self.gui.reading_attempts_spinBox.value()

    def closeEvent(self, event):
        response = QMessageBox.question(self, 'Quit', "Are you sure you want to quit?", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if response == QMessageBox.Yes:
            event.accept()
            self.analyzer.stop_stream = True
        else:
            event.ignore()
