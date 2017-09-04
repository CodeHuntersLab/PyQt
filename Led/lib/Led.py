from PyQt5.QtCore import pyqtProperty, QTimer, pyqtSlot, QRectF, QSize
from PyQt5.QtGui import QPainter
from PyQt5.QtSvg import QSvgRenderer
from PyQt5.QtWidgets import QWidget


class Led(QWidget):
    # https://www.linux-apps.com/p/1132197/
    _state = False

    Red, Green, Yellow, Grey, Orange, Purple, Blue = range(7)
    Circle, Square, Triangle, Rounded = range(4)

    colors = ("red.svg", "green.svg", "yellow.svg", "grey.svg", "orange.svg", "purple.svg", "blue.svg")
    shapes = (":/resources/circle_", ":/resources/square_", ":/resources/triang_", ":/resources/round_")

    _onColor = colors[Red]
    _offColor = colors[Grey]

    _shape = shapes[Circle]

    _flashing = False

    _flashRate = 200

    renderer = QSvgRenderer()

    def __init__(self, parent=None):
        QWidget.__init__(self, parent)
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.toogle)

    @pyqtSlot()
    def on(self):
        self.state = True

    @pyqtSlot()
    def off(self):
        self.state = False

    @pyqtProperty(bool)
    def state(self):
        return self._state

    @state.setter
    def state(self, val):
        if self._state == val:
            return
        self._state = val
        self.update()

    @pyqtProperty(bool)
    def flashing(self):
        return self._flashing

    @flashing.setter
    def flashing(self, val):
        if self._flashing == val:
            return
        self._flashing = val
        if self._flashing:
            self.timer.start(100)
        else:
            self.timer.stop()

    @pyqtSlot()
    def toogle(self):
        self.state = not self.state

    @pyqtProperty(int)
    def flashRate(self):
        return self._flashRate

    @flashRate.setter
    def flashRate(self, val):
        if self._flashRate == val:
            return
        self._flashRate = val
        self.timer.setInterval(self._flashRate)

    @pyqtProperty(int)
    def onColor(self):
        return self.colors.index(self._onColor)

    @onColor.setter
    def onColor(self, val):
        if self._onColor == self.colors[val]:
            return
        self._onColor = self.colors[val]
        self.update()

    @pyqtProperty(int)
    def offColor(self):
        return self.colors.index(self._offColor)

    @offColor.setter
    def offColor(self, val):
        if self._offColor == self.colors[val]:
            return
        self._offColor = self.colors[val]
        self.update()

    @pyqtProperty(int)
    def shape(self):
        return self.shapes.index(self._shape)

    @shape.setter
    def shape(self, val):
        if self._shape == self.shapes[val]:
            return
        self._shape = self.shapes[val]
        self.update()

    def sizeHint(self):
        return QSize(100, 100)

    def paintEvent(self, event):
        ledShapeAndColor = self._shape
        ledShapeAndColor += self._onColor if self._state else self._offColor
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing, True)
        self.renderer.load(ledShapeAndColor)
        self.renderer.render(painter, QRectF(self.rect()))
