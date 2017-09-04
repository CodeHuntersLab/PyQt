from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import QApplication

from lib import Led


def onTimeout(w):
    w.flashRate += 100
    print(w.flashRate)

if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    w = Led()
    w.flashing = True
    w.onColor = Led.Blue
    w.shape = Led.Circle
    timer = QTimer()
    timer.timeout.connect(lambda: onTimeout(w))
    timer.start(10000)
    w.show()
    sys.exit(app.exec_())