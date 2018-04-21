"""
 Created by PyCharm Community Edition.
 User: Anton Vasiliev <bysslaev@gmail.com>
 Date: 16/04/2018
 Time: 23:54

"""
from PyQt5 import Qt

from PyQt5.QtGui import QPainter, QPolygonF
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QDialog

from PyQt5.QtChart import QChart, QChartView, QLineSeries
import numpy as np


def series_to_polyline(xdata, ydata):
    """Convert series data to QPolygon(F) polyline

    This code is derived from PythonQwt's function named
    `qwt.plot_curve.series_to_polyline`"""
    size = len(xdata)
    polyline = QPolygonF(size)
    pointer = polyline.data()
    dtype, tinfo = np.float, np.finfo  # integers: = np.int, np.iinfo
    pointer.setsize(2 * polyline.size() * tinfo(dtype).dtype.itemsize)
    memory = np.frombuffer(pointer, dtype)
    memory[:(size - 1) * 2 + 1:2] = xdata
    memory[1:(size - 1) * 2 + 2:2] = ydata
    return polyline


class ChartsForm(QDialog):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.ncurves = 0

        self.label = QLabel()
        self.label.setText("Графики.")
        self.label.resize(self.label.sizeHint())
        self.label.move(50, 10)
        self.chart = QChart()
        self.chart.legend().hide()
        self.set_title("График дифференциальных уравнений")
        self.view = QChartView(self.chart)
        self.view.setRenderHint(QPainter.Antialiasing)
        self.view.move(500,300)
        self.view.resize(400,250)

        vBox = QVBoxLayout()
        vBox.addWidget(self.view)
        vBox.addWidget(self.label)

        self.setLayout(vBox)
        self.resize(700, 450)
        self.setWindowTitle('Charts')

        npoints = 1000000
        xdata = np.linspace(0., 10., npoints)
        self.add_data(xdata, np.sin(xdata))
        self.add_data(xdata, np.cos(xdata))
        self.exec_()

    def set_title(self, title):
        self.chart.setTitle(title)

    def add_data(self, xdata, ydata, color=None):
        curve = QLineSeries()
        pen = curve.pen()
        if color is not None:
            pen.setColor(color)
        pen.setWidthF(.1)
        curve.setPen(pen)
        curve.setUseOpenGL(True)
        curve.append(series_to_polyline(xdata, ydata))
        self.chart.addSeries(curve)
        self.chart.createDefaultAxes()
        self.ncurves += 1
