import sys

import matplotlib.pyplot as plt
from PyQt5.QtCore import QRect
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from PyQt5.QtWidgets import QApplication, QMainWindow, QDialog, QVBoxLayout, QLabel

from main_window import Ui_MainWindow


class CoordinateDecentWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.setWindowTitle('Coordinate Decent Method')
        self.f = None
        self.x0 = None
        self.ab = None
        self.exp = None
        self.fig = None
        self.canvas = None
        self.triggers()

    def initialize(self):
        self.ui.plainTextEdit.clear()

        try:
            self.f = lambda x: eval(self.ui.f.text())
            self.x0 = [float(self.ui.x01.text()), float(self.ui.x02.text())]
            self.ab = [float(self.ui.a.text()), float(self.ui.b.text())]
            self.exp = float(self.ui.exp.text())

            self.fig = plt.figure(figsize=(5, 3), dpi=80)
            plt.xlabel('X1')
            plt.ylabel('X2')
            ax = self.fig.gca()

            result = self.calculate()
            self.ui.plainTextEdit.insertPlainText(f'{result}\n')

        except Exception as e:
            dialog = QDialog(self)
            dialog.setWindowTitle('An error was occurred')
            dialog.setMaximumSize(dialog.size())
            layout = QVBoxLayout()
            layout.addWidget(QLabel(f'{e}'))
            dialog.setLayout(layout)
            dialog.exec()

    def clear_ui(self):
        self.ui.f.clear()
        self.ui.x01.clear()
        self.ui.x02.clear()
        self.ui.a.clear()
        self.ui.b.clear()
        self.ui.exp.clear()
        self.ui.plainTextEdit.clear()

        self.resize(self.size().width() - 400, self.size().height())

    def _golden_ratio_method(self, var, is_x: bool):
        a, b = self.ab
        c = (3 - 5 ** (1 / 2)) / 2 * (b - a) + a
        d = (5 ** (1 / 2) - 1) / 2 * (b - a) + a

        while (b - a) / 2 > self.exp:
            y = [
                self.f([var, c]) if is_x else self.f([c, var]),
                self.f([var, d]) if is_x else self.f([d, var])
            ]

            self.ui.plainTextEdit.insertPlainText(f'{a=} {b=} {c=} {d=} {y=}\n')

            if y[0] > y[1]:
                a = c
                c = d
                d = (5 ** (1 / 2) - 1) / 2 * (b - a) + a
            elif y[0] < y[1]:
                b = d
                d = c
                c = (3 - 5 ** (1 / 2)) / 2 * (b - a) + a

        return (a + b) / 2

    def calculate(self):

        self.resize(self.size().width() + 400, self.size().height())
        self.canvas = FigureCanvas(self.fig)
        self.canvas.setGeometry(QRect(800, 0, 400, 283))
        self.layout().addWidget(self.canvas)

        x, y = [], []
        x01, x02 = self.x0
        x01_min = self._golden_ratio_method(x01, True)
        x02_min = self._golden_ratio_method(x02, False)
        x.append(x01_min)
        y.append(x02_min)
        self.ui.plainTextEdit.insertPlainText(f"{'----------' * 5}\n")
        while abs(self.f([x01, x02]) - self.f([x01_min, x02_min])) > self.exp:
            x01, x02 = x01_min, x02_min
            x01_min = self._golden_ratio_method(x01, True)
            x02_min = self._golden_ratio_method(x02, False)
            x.append(x01_min)
            y.append(x02_min)
            self.ui.plainTextEdit.insertPlainText(f"{'----------' * 5}\n")

        plt.step(x, y, '-o', where='pre')
        plt.grid()

        self.ui.plainTextEdit.verticalScrollBar().setValue(
            self.ui.plainTextEdit.verticalScrollBar().maximum()
        )

        return x01_min, x02_min

    def triggers(self):
        self.ui.calculate.clicked.connect(self.initialize)
        self.ui.pushButton.clicked.connect(self.clear_ui)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = CoordinateDecentWindow()
    win.show()
    sys.exit(app.exec())
