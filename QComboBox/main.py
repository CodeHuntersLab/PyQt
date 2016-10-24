from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QComboBox


def onchange_index(index):
    print(str(index) + ":" + w.currentText())

if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    global w
    w = QComboBox()
    items = ["index 0", "index 1", "index 2"]
    w.addItems(items)
    w.addItem("index 3")
    w.currentIndexChanged.connect(onchange_index)
    w.show()
    sys.exit(app.exec_())
