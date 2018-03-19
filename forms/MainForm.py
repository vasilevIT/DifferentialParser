"""
 Created by PyCharm Community Edition.
 User: Anton Vasiliev <bysslaev@gmail.com>
 Date: 19/03/2018
 Time: 22:17

"""

from PyQt5.QtWidgets import (QWidget, QToolTip,
                             QPushButton, QTextEdit, QLabel, QMessageBox)
from PyQt5.QtCore import QCoreApplication
from PyQt5.QtGui import QIcon
from PyQt5.QtGui import QFont


class MainForm(QWidget):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        QToolTip.setFont(QFont('SansSerif', 10))

        self.setToolTip('This is a <b>QWidget</b> widget')

        label = QLabel(self)
        label.setText('Сюда пишем текст:')
        label.move(50, 30)

        txtEdit = QTextEdit(self)
        txtEdit.resize(400, 300)
        txtEdit.move(50, 50)

        btnParse = QPushButton('Parse', self)
        btnParse.setToolTip('This is a <b>QPushButton</b> widget')
        btnParse.resize(btnParse.sizeHint())
        btnParse.move(50, 380)
        btnParse.clicked.connect(QCoreApplication.instance().quit)

        btn = QPushButton('Clear', self)
        btn.setToolTip('This is a <b>QPushButton</b> widget')
        btn.resize(btn.sizeHint())
        btn.move(50, 420)
        btn.clicked.connect(QCoreApplication.instance().quit)

        self.setGeometry(300, 300, 700, 500)
        self.setWindowTitle('Differential parser')
        self.setWindowIcon(QIcon('./images/icon.png'))
        self.show()

    def closeEvent(self, event):

        reply = QMessageBox.question(self, 'Message',
                                     "Are you sure to quit?", QMessageBox.Yes |
                                     QMessageBox.No, QMessageBox.No)

        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()
