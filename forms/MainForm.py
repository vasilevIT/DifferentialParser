"""
 Created by PyCharm Community Edition.
 User: Anton Vasiliev <bysslaev@gmail.com>
 Date: 19/03/2018
 Time: 22:17

"""

from PyQt5.QtWidgets import (QToolTip,
                             QPushButton, QTextEdit, QLabel, QMessageBox, QDesktopWidget, qApp,
                             QVBoxLayout, QWidget)
from PyQt5.QtGui import (QIcon, QFont)

from classes.Parser import Parser


class MainForm(QWidget):
    EXAMPLE_TEXT1 = """
    program DiffSolv1.0

Equations:
Susc/dt = -A * Susc * Sick
Sick/dt = A * Susk * Sick - (B + C) * Sick
Cured/dt = B * Sick

BeginConditions:
Susk = 620
Sick = 10
Cured = 70
A = 000.1
B = 0.07
C = 0.01

IntegrationConfitions:
method = Euler
t = 50
dt = 0.5
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
        self.btn.clicked.connect(qApp.quit)

        vBox = QVBoxLayout()
        vBox.addStretch(1)
        vBox.addWidget(self.label)
        vBox.addWidget(self.txtEdit)
        vBox.addWidget(self.btnParse)
        vBox.addWidget(self.btn)

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

    def parseStart(self):
        text = self.txtEdit.toPlainText()
        self.parser.parse(text)

    def closeEvent(self, event):

        reply = QMessageBox.question(self, 'Message',
                                     "Are you sure to quit?", QMessageBox.Yes |
                                     QMessageBox.No, QMessageBox.No)

        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()
