from PyQt5.QtWidgets import QApplication, QPushButton


def onclick():
    print("You have clicked me")
    w.setText("click me, again please")
    w.resize(w.sizeHint())

if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    global w
    w = QPushButton("Click me, please")
    w.clicked.connect(onclick)
    w.setFlat(True)
    w.show()
    sys.exit(app.exec_())
