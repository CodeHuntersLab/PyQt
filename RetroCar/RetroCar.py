"""
 / ___|___   __| | ___| | | |_   _ _ __ | |_ ___ _ __ ___  | |    __ _| |__
| |   / _ \ / _` |/ _ \ |_| | | | | '_ \| __/ _ \ '__/ __| | |   / _` | '_ \
| |__| (_) | (_| |  __/  _  | |_| | | | | ||  __/ |  \__ \ | |__| (_| | |_) |
 \____\___/ \__,_|\___|_| |_|\__,_|_| |_|\__\___|_|  |___/ |_____\__,_|_.__/
"""
from PyQt5.QtCore import QPoint, QRect, QSize, Qt, qsrand, QTime, qrand
from PyQt5.QtGui import QBrush, QColor, QPainter, QFont
from PyQt5.QtMultimedia import QSound
from PyQt5.QtWidgets import QApplication, QWidget, QDesktopWidget


class RetroCar(QWidget):
    def __init__(self, parent=None):
        super(RetroCar, self).__init__(parent)
        self.rows, self.cols = [25, 10]
        self.factor = 25
        self.resize(self.factor * QSize(self.cols, self.rows))
        self.isObs = 0
        self.isBorder = 0
        self.car_pos = QPoint(self.cols / 2, self.rows - 4)
        self.size = QSize(self.factor, self.factor)
        self._poss = [QPoint(0, -1),
                      QPoint(0, 0),
                      QPoint(1, 0),
                      QPoint(-1, 0),
                      QPoint(0, 1),
                      QPoint(-1, 2),
                      QPoint(1, 2)]
        self.color = QColor(0, 0, 0)
        final = 3
        self.border = []
        while final < self.rows:
            self.border += list(range(final - 3, final))
            final += 5
        self.obs_pos = None
        self.create_obs()
        self.rect_text = QRect(self.cols * self.factor / 2, self.rows * self.factor / 2,
                               5 * self.factor, 2 * self.factor)
        self.rect_text.moveCenter(QPoint(self.cols / 2, self.rows / 2) * self.factor)
        self.isDrawMenu = True
        self.text_Menu = 'Iniciar'
        self.setMinimumSize(self.factor * QSize(self.cols, self.rows))
        self.setMaximumSize(self.factor * QSize(self.cols, self.rows))
        self.move(QDesktopWidget().screen().rect().center() - self.rect().center())
        self.score = 0
        sound = QSound("Tetris.wav", self)
        sound.setLoops(QSound.Infinite)
        sound.play()
        self.level = 1
        self.scores = [5000*(x+1) for x in list(range(8))]

    def create_obs(self):
        qsrand(QTime(0, 0, 0).secsTo(QTime.currentTime()))
        self.obs_pos = QPoint((2 + (qrand() % (self.cols - 4))), 0)

    def isCrash(self):
        for _posi in self._poss:
            for _posj in self._poss:
                if (self.car_pos + _posi) == (self.obs_pos + _posj):
                    return True
        return False

    def paintEvent(self, QPaintEvent):
        super().paintEvent(QPaintEvent)
        painter = QPainter(self)
        painter.setPen(Qt.black)
        self.drawCar(painter, self.car_pos)
        self.drawBorder(painter)
        if self.isDrawMenu:
            self.drawMenu(painter, self.text_Menu)
        else:
            self.drawCar(painter, self.obs_pos)
        self.drawScore(painter)

    def drawSquare(self, painter, pos):
        painter.fillRect(QRect(pos + QPoint(self.size.width(), self.size.height()) / 12,
                               self.size - self.size / 6),
                         QBrush(QColor(Qt.black)))
        painter.fillRect(QRect(pos + QPoint(self.size.width(), self.size.height()) / 8,
                               self.size - self.size / 4),
                         QBrush(QColor(Qt.gray)))
        painter.fillRect(QRect(pos + QPoint(self.size.width(), self.size.height()) / 6,
                               self.size - self.size / 3),
                         QBrush(QColor(Qt.black)))

    def drawBorder(self, painter):
        for element in self.border:
            self.drawSquare(painter, QPoint(0, element) * self.factor)
            self.drawSquare(painter, QPoint(self.cols - 1, element) * self.factor)

    def drawCar(self, painter, pos):
        for _pos in self._poss:
            n_pos = pos + _pos
            if QRect(QPoint(0, 0), QSize(self.cols, self.rows)).contains(n_pos):
                self.drawSquare(painter, n_pos * self.factor)

    def timerEvent(self, event):
        if self.isBorder == 0:
            self.border = [(x + 1) % self.rows for x in self.border]
        if self.isObs == 0:
            if self.obs_pos.y() - 1 < self.rows:
                self.obs_pos += QPoint(0, 1)
            else:
                self.create_obs()
        if self.isCrash():
            self.killTimer(event.timerId())
            self.isDrawMenu = True
            self.text_Menu = 'Reiniciar'
            self.score = 0
        else:
            self.score += 1
            if self.score == self.scores[self.level-1]:
                self.level += 1
                if self.level == 8:
                    self.killTimer(event.timerId())

        self.update()
        self.isObs = (self.isObs + 1) % (10-self.level)
        self.isBorder = (self.isBorder + 1) % 3

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Left:
            if self.car_pos.x() > 2:
                self.car_pos += QPoint(-1, 0)
        if event.key() == Qt.Key_Right:
            if self.car_pos.x() + 3 < self.cols:
                self.car_pos += QPoint(1, 0)

    def mousePressEvent(self, event):
        if self.rect_text.contains(event.pos()):
            self.isDrawMenu = False
            self.create_obs()
            self.startTimer(10)

    def drawMenu(self, painter, text):
        font = "Cantarell"
        painter.setFont(QFont(font, 15))
        painter.drawText(self.rect_text, Qt.AlignCenter, text)

    def drawScore(self, painter):
        painter.setPen(Qt.red)
        font = "Cantarell"
        painter.setFont(QFont(font, 8))
        rect = QRect(QPoint(self.cols/3, 0) * self.factor,
                     self.factor * QSize(self.cols/2, 2))
        painter.drawText(rect, Qt.AlignCenter, 'Nivel: {} Puntaje: {}'.format(self.level, self.score))


if __name__ == '__main__':
    import sys

    app = QApplication(sys.argv)
    app.setApplicationName("RetroCar")
    w = RetroCar()
    w.show()
    sys.exit(app.exec_())
