import os
import sys  # sys нужен для передачи argv в QApplication
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QTableWidgetItem, QHeaderView
from PyQt5.uic.properties import QtGui, QtCore

import design


class ExampleApp(QtWidgets.QWidget, design.Ui_Form):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.loadDataButton.clicked.connect(self.browse_folder)  # Выполнить функцию browse_folder

    def browse_folder(self):
        self.table.clear()
        filename = QtWidgets.QFileDialog.getOpenFileName(self, "Выберите фвйл (txt, csv)",
                                                         "/home/liza/PycharmProjects/gameTheory", "txt (*.txt)")
        if filename[0]:
            f = open(filename[0], 'r')
            with f:
                data = f.read()

        data = data.split('\n')[:-1]
        data = [[int(elem) for elem in line.split()] for line in data]
        self.table.setColumnWidth(len(data), len(data[0]))

        for row in range(len(data)):
            for col in range(len(data[row])):
                self.table.setItem(row, col, QTableWidgetItem(data[row][col]))



def main():
    app = QtWidgets.QApplication(sys.argv)
    window = ExampleApp()
    window.show()
    app.exec_()


if __name__ == '__main__':
    main()
