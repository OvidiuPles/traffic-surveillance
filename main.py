import pyqtgraph as pg

from source.gui.main_gui import MainGUI

if __name__ == "__main__":
    app = pg.mkQApp()
    window = MainGUI()
    window.show()
    app.exec()
