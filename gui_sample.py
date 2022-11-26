import sys
import matplotlib
import yfinance as yf
matplotlib.use('Qt5Agg')

from PyQt5 import QtCore, QtWidgets

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg, NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure


class MplCanvas(FigureCanvasQTAgg):

    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        super(MplCanvas, self).__init__(fig)


class MainWindow(QtWidgets.QMainWindow):

    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)

        # Create the maptlotlib FigureCanvas object,
        # which defines a single set of axes as self.axes.
        sc = MplCanvas(self, width=5, height=4, dpi=100)
        self.canvas = sc 
        toolbar = NavigationToolbar(sc, self)
        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(toolbar)
        layout.addWidget(sc)
        widget = QtWidgets.QWidget()
        widget.setLayout(layout)
        self.widget = widget
    
    def simple_plot(self,data):
        self.canvas.axes.plot(data)
        self.setCentralWidget(self.widget)
        self.show()

data = yf.Ticker("SPY").history(period="1y")
app = QtWidgets.QApplication(sys.argv)
w = MainWindow()
w.simple_plot(data["High"])
app.exec_()