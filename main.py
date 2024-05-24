import sys

from PySide6.QtWidgets import QApplication

from source.gui.main_gui import MainGUI


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainGUI()
    window.show()
    sys.exit(app.exec())
