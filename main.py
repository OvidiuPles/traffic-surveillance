import subprocess
import sys
from PySide6.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QVBoxLayout, QMainWindow
from PySide6.QtGui import QPixmap

from source.gui.main_window import Ui_MainWindow


#  pyside6-uic source/gui/main_window.ui -o source/gui/main_window.py


class SimpleGUI(QMainWindow):
    def __init__(self):
        super().__init__()

        self.gui = Ui_MainWindow()
        self.gui.setupUi(self)

        # Connect the button click event to a method
        self.gui.pushButton.clicked.connect(self.on_button_click)

        pixmap = QPixmap(r'C:\Users\Ovi Carici\OneDrive - Technical University of Cluj-Napoca\Desktop\w\x.jpg')  # Replace with your image path
        self.gui.label.setPixmap(pixmap)  # Assuming the QLabel in Qt Designer is named 'label'


    def on_button_click(self):
        print("Button clicked")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = SimpleGUI()
    window.show()
    sys.exit(app.exec())
