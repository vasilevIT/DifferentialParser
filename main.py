"""
 Created by PyCharm Community Edition.
 User: Anton Vasiliev <bysslaev@gmail.com>
 Date: 19/03/2018
 Time: 21:26

"""

import sys
from PyQt5.QtWidgets import QApplication
from forms.MainForm import MainForm

if __name__ == '__main__':
    app = QApplication(sys.argv)

    ex = MainForm()
    sys.exit(app.exec_())
