"""
 Created by PyCharm Community Edition.
 User: Anton Vasiliev <bysslaev@gmail.com>
 Date: 16/04/2018
 Time: 23:54

"""
import random

from PyQt5.QtGui import QPainter, QPolygonF, QPen, QColor
from PyQt5.QtWidgets import QVBoxLayout, QLabel, QDialog

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

        self.label_summary = QLabel()
        self.label_summary.setText("")
        self.label_summary.resize(self.label_summary.sizeHint())
        self.label_summary.move(10, 10)

        self.chart = QChart()
        # self.chart.legend().hide()
        self.set_title("График дифференциальных уравнений")
        self.view = QChartView(self.chart)
        self.view.setRenderHint(QPainter.Antialiasing)
        self.view.move(500, 300)
        self.view.resize(400, 250)

        vBox = QVBoxLayout()
        vBox.addWidget(self.view)
        vBox.addWidget(self.label)
        vBox.addWidget(self.label_summary)

        self.setLayout(vBox)
        self.resize(700, 450)
        self.setWindowTitle('Charts')

    def set_title(self, title):
        """
        Устанавливает титул в график
        :param title:
        :return:
        """
        self.chart.setTitle(title)

    def add_data(self, xdata, ydata, color=None, curve_name="None"):
        """
        Добавляет новую функцию на график
        :param xdata:
        :param ydata:
        :param color:
        :param curve_name:
        :return:
        """
        curve = QLineSeries()
        pen = curve.pen()
        if color is not None:
            if isinstance(color, str):
                color = QColor(color)
            pen.setColor(color)
            pen.setColor(color)
        else:
            pen.setColor(self.getRandomColor())
        pen.setWidthF(.1)
        curve.setPen(pen)
        curve.setName(curve_name)
        curve.setUseOpenGL(True)
        curve.append(series_to_polyline(xdata, ydata))
        self.chart.addSeries(curve)
        self.chart.createDefaultAxes()
        self.ncurves += 1
        print(ydata)
        summary_value = np.sum(ydata)
        self.label_summary.setText(self.label_summary.text() + curve_name + " = " + str(summary_value) + "\n")

    def getRandomColor(self):
        """
        Возвращает случайный цвет из списка
        :return:
        """
        colors = {}
        colors[0] = QColor("black")
        colors[1] = QColor("red")
        colors[2] = QColor("blue")
        colors[3] = QColor("green")
        colors[4] = QColor("yellow")
        colors[5] = QColor("orange")
        colors[6] = QColor("violet")
        index = random.randint(0, 6)
        return colors[index]

    def show(self):
        self.exec_()
