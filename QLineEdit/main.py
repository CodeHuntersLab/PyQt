from PyQt5.QtCore import qrand
from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import QApplication, QLineEdit


def onchange_text():
    color = QColor(qrand() % 256, qrand() % 256, qrand() % 256)
    w.setStyleSheet('background: rgb({}, {}, {});'.format(color.red(), color.green(), color.blue()))

if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    global w
    w = QLineEdit()
    w.textChanged.connect(onchange_text)
    w.show()
    sys.exit(app.exec_())
