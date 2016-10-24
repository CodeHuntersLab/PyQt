from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QCheckBox


def onchange_state(state):
    msg = {
        Qt.Unchecked: "Sin Chequear",
        Qt.PartiallyChecked: "Parcialmente Chequeado",
        Qt.Checked: "Chequeado"
    }[state]
    w.setText(msg)
    w.resize(w.sizeHint())


if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    global w
    w = QCheckBox()
    w.setText("Me escoges?")
    w.setTristate(True)
    w.stateChanged.connect(onchange_state)
    w.show()
    sys.exit(app.exec_())
