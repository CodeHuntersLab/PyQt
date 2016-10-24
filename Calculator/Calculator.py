from PyQt5.QtCore import QSize, pyqtSlot
from PyQt5.QtWidgets import QApplication, QGridLayout, QLineEdit,\
    QMessageBox, QPushButton, QWidget


class Calculator(QWidget):
    def __init__(self, parent=None):
        super(Calculator, self).__init__(parent)
        layout = QGridLayout()
        self.lineEdit = QLineEdit(self)
        layout.addWidget(self.lineEdit, 0, 0, 1, 4)
        layout.setSpacing(0)
        numbers = {'1': (1, 0),
                   '2': (1, 1),
                   '3': (1, 2),
                   chr(247): (1, 3),
                   '4': (2, 0),
                   '5': (2, 1),
                   '6': (2, 2),
                   chr(215): (2, 3),
                   '7': (3, 0),
                   '8': (3, 1),
                   '9': (3, 2),
                   '-': (3, 3),
                   '0': (4, 0),
                   '.': (4, 1),
                   '=': (4, 2),
                   '+': (4, 3)}

        layout.setSpacing(0)
        layout.setContentsMargins(0, 0, 0, 0)
        for key, value in numbers.items():
            btn = QPushButton(key)
            size = QSize(80, 60)
            btn.setMinimumSize(size)
            btn.setMaximumSize(size)
            btn.clicked.connect(self.addText)
            layout.addWidget(btn, value[0], value[1])
        self.setLayout(layout)
        self.setMaximumSize(self.sizeHint())

    @pyqtSlot()
    def addText(self):
        character = self.sender().text()
        if character == '=':
            text = self.lineEdit.text()
            operation = ''
            for letter in text:
                if ord(letter) == 247:
                    operation += '/'
                elif ord(letter) == 215:
                    operation += '*'
                else:
                    operation += letter
            try:
                resp = eval(operation)
                self.lineEdit.setText(str(resp))
            except SyntaxError:
                QMessageBox().critical(self, "Error", "Verífica tus cálculos")
        else:
            self.lineEdit.setText(self.lineEdit.text() + character)

if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    app.setApplicationName("Calculadora")
    w = Calculator()
    w.show()
    sys.exit(app.exec_())
