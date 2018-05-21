"""
 Created by PyCharm Community Edition.
 User: Anton Vasiliev <bysslaev@gmail.com>
 Date: 19/03/2018
 Time: 22:17

"""

from PyQt5.QtWidgets import (QToolTip,
                             QPushButton, QTextEdit, QLabel, QMessageBox, QDesktopWidget, qApp,
                             QVBoxLayout, QWidget)
from PyQt5.QtGui import (QIcon, QFont, QTextCursor)

from classes.Parser import Parser
from forms.ChartsForm import ChartsForm


class MainForm(QWidget):
    EXAMPLE_TEXT1 = """Program: DiffSolv1.0

Equations:
Susc/dt = -A * Susc * Sick;
Sick/dt = A * Susc * Sick - (B + C) * Sick;
Cured/dt = B * Sick;

BeginConditions:
Susc = 620;
Sick = 10;
Cured = 70;
A = 0.001;
B = 0.07;
C = 0.01;

IntegrationConditions:
method = Euler;
t = 50;
dt = 0.5;
"""

    def __init__(self):
        super().__init__()
        self.parser = Parser()
        self.initUI()

    def initUI(self):
        QToolTip.setFont(QFont('SansSerif', 10))

        self.label = QLabel()
        self.label.setText('Сюда пишем текст:')
        self.label.resize(self.label.sizeHint())
        self.label.move(50, 30)

        self.txtEdit = QTextEdit()
        self.txtEdit.resize(700, 400)
        self.txtEdit.move(50, 50)
        self.txtEdit.setText(self.EXAMPLE_TEXT1)

        self.btnParse = QPushButton('Parse')
        self.btnParse.setToolTip('This is a <b>QPushButton</b> widget')
        self.btnParse.resize(self.btnParse.sizeHint())
        self.btnParse.move(50, 380)
        self.btnParse.clicked.connect(self.parseStart)

        self.btn = QPushButton('Clear')
        self.btn.setToolTip('This is a <b>QPushButton</b> widget')
        self.btn.resize(self.btn.sizeHint())
        self.btn.move(50, 420)
        self.btn.clicked.connect(self.clear)

        self.error = QLabel()
        self.error.resize(self.error.sizeHint())
        self.error.move(50, 480)

        vBox = QVBoxLayout()
        vBox.addStretch(1)
        vBox.addWidget(self.label)
        vBox.addWidget(self.txtEdit)
        vBox.addWidget(self.btnParse)
        vBox.addWidget(self.btn)
        vBox.addWidget(self.error)

        self.setLayout(vBox)
        self.resize(700, 400)
        self.setWindowTitle('Differential parser')
        self.setWindowIcon(QIcon('./images/icon.png'))

        self.show()

    def center(self):

        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def clear(self):
        self.txtEdit.setText("")
        self.error.setText("")

    def parseStart(self):
        text = self.txtEdit.toPlainText()
        cursor = self.txtEdit.textCursor()
        current_position = cursor.position()
        cursor.setPosition(0)
        self.txtEdit.setTextCursor(cursor)
        self.txtEdit.setPlainText(text)
        self.error.setText("")
        cursor.setPosition(current_position)
        self.txtEdit.setTextCursor(cursor)
        try:
            self.parser.parse(text)
        except Exception as e:
            text = self.txtEdit.toPlainText()
            self.error.setText(e.args[0])
            shift = 0
            if (e.args[1] > 2):
                shift = -2
            text = text[0:(e.args[1]) + shift] \
                   + "<span style=\"font-weight:600; color:#FF0000;\" >" \
                   + text[e.args[1] + shift:(e.args[1] + shift + e.args[2])] \
                   + "</span>" \
                   + text[e.args[1] + shift + e.args[2]:]
            text = text.replace("\n", "<br>")
            self.txtEdit.setHtml(text)
            cursor = self.txtEdit.textCursor()
            cursor.setPosition(e.args[1])
            self.txtEdit.setTextCursor(cursor)
            return
        try:
            data = self.parser.integrator.run()

            data_clear = {}
            for key, data_item in data.items():
                for var, value in data_item.items():
                    if var not in data_clear.keys():
                        data_clear[var] = {}
                    data_clear[var][key] = value
            chartForm = ChartsForm()
            for key, data_items in data_clear.items():
                data_keys = list(data_items)
                data_values = list(data_items.values())
                chartForm.add_data(data_keys, data_values, None, key)
            chartForm.set_integration_method(
                "Метод интегрирования: " + self.parser.integrator.integration_method + "\nШаг интегрирования: " + str(
                    self.parser.integrator.integration_var_step_value) + "\nИнтервал интегрирования: " + str(
                    self.parser.integrator.integration_var_value))
            chartForm.show()
        except Exception as e:
            self.error.setText(e.__str__())

    def closeEvent(self, event):
        event.accept()
