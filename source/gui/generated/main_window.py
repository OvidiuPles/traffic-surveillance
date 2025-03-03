# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'main_window.ui'
##
## Created by: Qt User Interface Compiler version 6.7.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QCheckBox, QDoubleSpinBox, QGridLayout,
    QGroupBox, QHBoxLayout, QLabel, QLineEdit,
    QMainWindow, QMenuBar, QPushButton, QSizePolicy,
    QSpinBox, QStatusBar, QVBoxLayout, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(1160, 762)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.gridLayoutWidget = QWidget(self.centralwidget)
        self.gridLayoutWidget.setObjectName(u"gridLayoutWidget")
        self.gridLayoutWidget.setGeometry(QRect(20, 20, 801, 461))
        self.image_layout = QGridLayout(self.gridLayoutWidget)
        self.image_layout.setObjectName(u"image_layout")
        self.image_layout.setContentsMargins(0, 0, 0, 0)
        self.layoutWidget = QWidget(self.centralwidget)
        self.layoutWidget.setObjectName(u"layoutWidget")
        self.layoutWidget.setGeometry(QRect(21, 511, 801, 201))
        self.bottom_layout = QHBoxLayout(self.layoutWidget)
        self.bottom_layout.setObjectName(u"bottom_layout")
        self.bottom_layout.setContentsMargins(0, 0, 0, 0)
        self.drawing_groupBox = QGroupBox(self.layoutWidget)
        self.drawing_groupBox.setObjectName(u"drawing_groupBox")
        self.layoutWidget1 = QWidget(self.drawing_groupBox)
        self.layoutWidget1.setObjectName(u"layoutWidget1")
        self.layoutWidget1.setGeometry(QRect(10, 20, 316, 151))
        self.horizontalLayout = QHBoxLayout(self.layoutWidget1)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.boxes_checkBox = QCheckBox(self.layoutWidget1)
        self.boxes_checkBox.setObjectName(u"boxes_checkBox")
        self.boxes_checkBox.setStyleSheet(u"QCheckBox::indicator:unchecked {background-color: darkgray;}")

        self.verticalLayout.addWidget(self.boxes_checkBox)

        self.classes_checkBox = QCheckBox(self.layoutWidget1)
        self.classes_checkBox.setObjectName(u"classes_checkBox")
        self.classes_checkBox.setStyleSheet(u"QCheckBox::indicator:unchecked {background-color: darkgray;}")

        self.verticalLayout.addWidget(self.classes_checkBox)

        self.number_plates_checkBox = QCheckBox(self.layoutWidget1)
        self.number_plates_checkBox.setObjectName(u"number_plates_checkBox")
        self.number_plates_checkBox.setStyleSheet(u"QCheckBox::indicator:unchecked {background-color: darkgray;}")

        self.verticalLayout.addWidget(self.number_plates_checkBox)


        self.horizontalLayout.addLayout(self.verticalLayout)

        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.total_counting_checkBox = QCheckBox(self.layoutWidget1)
        self.total_counting_checkBox.setObjectName(u"total_counting_checkBox")
        self.total_counting_checkBox.setAutoFillBackground(False)
        self.total_counting_checkBox.setStyleSheet(u"QCheckBox::indicator:unchecked {background-color: darkgray;}")

        self.verticalLayout_2.addWidget(self.total_counting_checkBox)

        self.class_counting_checkBox = QCheckBox(self.layoutWidget1)
        self.class_counting_checkBox.setObjectName(u"class_counting_checkBox")
        self.class_counting_checkBox.setStyleSheet(u"QCheckBox::indicator:unchecked {background-color: darkgray;}")

        self.verticalLayout_2.addWidget(self.class_counting_checkBox)

        self.lane_counting_checkBox = QCheckBox(self.layoutWidget1)
        self.lane_counting_checkBox.setObjectName(u"lane_counting_checkBox")
        self.lane_counting_checkBox.setStyleSheet(u"QCheckBox::indicator:unchecked {background-color: darkgray;}")

        self.verticalLayout_2.addWidget(self.lane_counting_checkBox)


        self.horizontalLayout.addLayout(self.verticalLayout_2)

        self.verticalLayout_3 = QVBoxLayout()
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.lanes_checkBox = QCheckBox(self.layoutWidget1)
        self.lanes_checkBox.setObjectName(u"lanes_checkBox")
        self.lanes_checkBox.setStyleSheet(u"QCheckBox::indicator:unchecked {background-color: darkgray;}")
        self.lanes_checkBox.setChecked(False)

        self.verticalLayout_3.addWidget(self.lanes_checkBox)

        self.ids_checkBox = QCheckBox(self.layoutWidget1)
        self.ids_checkBox.setObjectName(u"ids_checkBox")
        self.ids_checkBox.setStyleSheet(u"QCheckBox::indicator:unchecked {background-color: darkgray;}")

        self.verticalLayout_3.addWidget(self.ids_checkBox)

        self.counting_line_checkBox = QCheckBox(self.layoutWidget1)
        self.counting_line_checkBox.setObjectName(u"counting_line_checkBox")
        self.counting_line_checkBox.setStyleSheet(u"QCheckBox::indicator:unchecked {background-color: darkgray;}")

        self.verticalLayout_3.addWidget(self.counting_line_checkBox)


        self.horizontalLayout.addLayout(self.verticalLayout_3)


        self.bottom_layout.addWidget(self.drawing_groupBox)

        self.parameters_groupBox = QGroupBox(self.layoutWidget)
        self.parameters_groupBox.setObjectName(u"parameters_groupBox")
        self.layoutWidget2 = QWidget(self.parameters_groupBox)
        self.layoutWidget2.setObjectName(u"layoutWidget2")
        self.layoutWidget2.setGeometry(QRect(30, 30, 301, 151))
        self.horizontalLayout_3 = QHBoxLayout(self.layoutWidget2)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.horizontalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_4 = QVBoxLayout()
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.label = QLabel(self.layoutWidget2)
        self.label.setObjectName(u"label")

        self.verticalLayout_4.addWidget(self.label)

        self.label_4 = QLabel(self.layoutWidget2)
        self.label_4.setObjectName(u"label_4")

        self.verticalLayout_4.addWidget(self.label_4)

        self.label_2 = QLabel(self.layoutWidget2)
        self.label_2.setObjectName(u"label_2")

        self.verticalLayout_4.addWidget(self.label_2)

        self.label_3 = QLabel(self.layoutWidget2)
        self.label_3.setObjectName(u"label_3")

        self.verticalLayout_4.addWidget(self.label_3)


        self.horizontalLayout_3.addLayout(self.verticalLayout_4)

        self.verticalLayout_5 = QVBoxLayout()
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.vehicles_confidence_spinBox = QDoubleSpinBox(self.layoutWidget2)
        self.vehicles_confidence_spinBox.setObjectName(u"vehicles_confidence_spinBox")
        self.vehicles_confidence_spinBox.setDecimals(1)
        self.vehicles_confidence_spinBox.setMaximum(1.000000000000000)
        self.vehicles_confidence_spinBox.setSingleStep(0.100000000000000)
        self.vehicles_confidence_spinBox.setValue(0.000000000000000)

        self.verticalLayout_5.addWidget(self.vehicles_confidence_spinBox)

        self.tracking_depth_spinBox = QSpinBox(self.layoutWidget2)
        self.tracking_depth_spinBox.setObjectName(u"tracking_depth_spinBox")
        self.tracking_depth_spinBox.setMaximum(40)

        self.verticalLayout_5.addWidget(self.tracking_depth_spinBox)

        self.plates_confidence_spinBox = QDoubleSpinBox(self.layoutWidget2)
        self.plates_confidence_spinBox.setObjectName(u"plates_confidence_spinBox")
        self.plates_confidence_spinBox.setDecimals(1)
        self.plates_confidence_spinBox.setMaximum(1.000000000000000)
        self.plates_confidence_spinBox.setSingleStep(0.100000000000000)

        self.verticalLayout_5.addWidget(self.plates_confidence_spinBox)

        self.reading_attempts_spinBox = QSpinBox(self.layoutWidget2)
        self.reading_attempts_spinBox.setObjectName(u"reading_attempts_spinBox")
        self.reading_attempts_spinBox.setMaximum(40)

        self.verticalLayout_5.addWidget(self.reading_attempts_spinBox)


        self.horizontalLayout_3.addLayout(self.verticalLayout_5)


        self.bottom_layout.addWidget(self.parameters_groupBox)

        self.layoutWidget3 = QWidget(self.centralwidget)
        self.layoutWidget3.setObjectName(u"layoutWidget3")
        self.layoutWidget3.setGeometry(QRect(850, 20, 271, 461))
        self.right_layout = QVBoxLayout(self.layoutWidget3)
        self.right_layout.setObjectName(u"right_layout")
        self.right_layout.setContentsMargins(0, 0, 0, 0)
        self.streaming_groupBox = QGroupBox(self.layoutWidget3)
        self.streaming_groupBox.setObjectName(u"streaming_groupBox")
        self.stream_input_lineEdit = QLineEdit(self.streaming_groupBox)
        self.stream_input_lineEdit.setObjectName(u"stream_input_lineEdit")
        self.stream_input_lineEdit.setGeometry(QRect(20, 40, 231, 22))
        self.layoutWidget4 = QWidget(self.streaming_groupBox)
        self.layoutWidget4.setObjectName(u"layoutWidget4")
        self.layoutWidget4.setGeometry(QRect(20, 80, 231, 26))
        self.horizontalLayout_2 = QHBoxLayout(self.layoutWidget4)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.start_stream_pushButton = QPushButton(self.layoutWidget4)
        self.start_stream_pushButton.setObjectName(u"start_stream_pushButton")

        self.horizontalLayout_2.addWidget(self.start_stream_pushButton)

        self.stop_stream_pushButton = QPushButton(self.layoutWidget4)
        self.stop_stream_pushButton.setObjectName(u"stop_stream_pushButton")

        self.horizontalLayout_2.addWidget(self.stop_stream_pushButton)


        self.right_layout.addWidget(self.streaming_groupBox)

        self.streaming_groupBox_2 = QGroupBox(self.layoutWidget3)
        self.streaming_groupBox_2.setObjectName(u"streaming_groupBox_2")
        self.process_video_pushButton = QPushButton(self.streaming_groupBox_2)
        self.process_video_pushButton.setObjectName(u"process_video_pushButton")
        self.process_video_pushButton.setGeometry(QRect(20, 140, 111, 24))
        self.layoutWidget5 = QWidget(self.streaming_groupBox_2)
        self.layoutWidget5.setObjectName(u"layoutWidget5")
        self.layoutWidget5.setGeometry(QRect(20, 40, 231, 61))
        self.verticalLayout_6 = QVBoxLayout(self.layoutWidget5)
        self.verticalLayout_6.setObjectName(u"verticalLayout_6")
        self.verticalLayout_6.setContentsMargins(0, 0, 0, 0)
        self.video_input_lineEdit = QLineEdit(self.layoutWidget5)
        self.video_input_lineEdit.setObjectName(u"video_input_lineEdit")

        self.verticalLayout_6.addWidget(self.video_input_lineEdit)

        self.video_output_lineEdit = QLineEdit(self.layoutWidget5)
        self.video_output_lineEdit.setObjectName(u"video_output_lineEdit")

        self.verticalLayout_6.addWidget(self.video_output_lineEdit)

        self.generate_statistics_checkBox = QCheckBox(self.streaming_groupBox_2)
        self.generate_statistics_checkBox.setObjectName(u"generate_statistics_checkBox")
        self.generate_statistics_checkBox.setGeometry(QRect(20, 110, 121, 20))
        self.generate_statistics_checkBox.setStyleSheet(u"QCheckBox::indicator:unchecked {background-color: darkgray;}")
        self.generate_statistics_checkBox.setChecked(True)

        self.right_layout.addWidget(self.streaming_groupBox_2)

        self.groupBox = QGroupBox(self.layoutWidget3)
        self.groupBox.setObjectName(u"groupBox")
        self.tracked_plate_lineEdit = QLineEdit(self.groupBox)
        self.tracked_plate_lineEdit.setObjectName(u"tracked_plate_lineEdit")
        self.tracked_plate_lineEdit.setGeometry(QRect(20, 40, 231, 22))
        self.layoutWidget6 = QWidget(self.groupBox)
        self.layoutWidget6.setObjectName(u"layoutWidget6")
        self.layoutWidget6.setGeometry(QRect(20, 80, 231, 26))
        self.horizontalLayout_4 = QHBoxLayout(self.layoutWidget6)
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.horizontalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.track_plate_pushButton = QPushButton(self.layoutWidget6)
        self.track_plate_pushButton.setObjectName(u"track_plate_pushButton")

        self.horizontalLayout_4.addWidget(self.track_plate_pushButton)

        self.clear_tracking_pushButton = QPushButton(self.layoutWidget6)
        self.clear_tracking_pushButton.setObjectName(u"clear_tracking_pushButton")

        self.horizontalLayout_4.addWidget(self.clear_tracking_pushButton)


        self.right_layout.addWidget(self.groupBox)

        self.right_layout.setStretch(0, 7)
        self.right_layout.setStretch(1, 11)
        self.right_layout.setStretch(2, 7)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 1160, 22))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"Traffic Surveillance", None))
        self.drawing_groupBox.setTitle(QCoreApplication.translate("MainWindow", u"Processing options", None))
        self.boxes_checkBox.setText(QCoreApplication.translate("MainWindow", u"Vehicle boxes", None))
        self.classes_checkBox.setText(QCoreApplication.translate("MainWindow", u"Vehicle classes", None))
        self.number_plates_checkBox.setText(QCoreApplication.translate("MainWindow", u"Number plates", None))
        self.total_counting_checkBox.setText(QCoreApplication.translate("MainWindow", u"Total counting", None))
        self.class_counting_checkBox.setText(QCoreApplication.translate("MainWindow", u"Class counting", None))
        self.lane_counting_checkBox.setText(QCoreApplication.translate("MainWindow", u"Lane counting", None))
        self.lanes_checkBox.setText(QCoreApplication.translate("MainWindow", u"Lanes", None))
        self.ids_checkBox.setText(QCoreApplication.translate("MainWindow", u"Internal ID", None))
        self.counting_line_checkBox.setText(QCoreApplication.translate("MainWindow", u"Counting line", None))
        self.parameters_groupBox.setTitle(QCoreApplication.translate("MainWindow", u"Processing parameters", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"Vehicles confidence", None))
        self.label_4.setText(QCoreApplication.translate("MainWindow", u"Tracking depth", None))
        self.label_2.setText(QCoreApplication.translate("MainWindow", u"Number plates confidence", None))
        self.label_3.setText(QCoreApplication.translate("MainWindow", u"Plates reading attempts", None))
        self.streaming_groupBox.setTitle(QCoreApplication.translate("MainWindow", u"Streaming", None))
        self.stream_input_lineEdit.setText("")
        self.stream_input_lineEdit.setPlaceholderText(QCoreApplication.translate("MainWindow", u"Stream input", None))
        self.start_stream_pushButton.setText(QCoreApplication.translate("MainWindow", u"Start stream", None))
        self.stop_stream_pushButton.setText(QCoreApplication.translate("MainWindow", u"Stop stream", None))
        self.streaming_groupBox_2.setTitle(QCoreApplication.translate("MainWindow", u"Video", None))
        self.process_video_pushButton.setText(QCoreApplication.translate("MainWindow", u"Process video", None))
        self.video_input_lineEdit.setText("")
        self.video_input_lineEdit.setPlaceholderText(QCoreApplication.translate("MainWindow", u"Video input", None))
        self.video_output_lineEdit.setText("")
        self.video_output_lineEdit.setPlaceholderText(QCoreApplication.translate("MainWindow", u"Video output", None))
        self.generate_statistics_checkBox.setText(QCoreApplication.translate("MainWindow", u"Generate statistics", None))
        self.groupBox.setTitle(QCoreApplication.translate("MainWindow", u"Track plate number", None))
        self.tracked_plate_lineEdit.setText("")
        self.tracked_plate_lineEdit.setPlaceholderText(QCoreApplication.translate("MainWindow", u"Plate number", None))
        self.track_plate_pushButton.setText(QCoreApplication.translate("MainWindow", u"Start tracking", None))
        self.clear_tracking_pushButton.setText(QCoreApplication.translate("MainWindow", u"Clear tracking", None))
    # retranslateUi

