import sys

import pandas as pd
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QTableWidgetItem

import design


class ExampleApp(QtWidgets.QWidget, design.Ui_Form):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.saddle_points = []
        self.data = []
        self.loadDataButton.clicked.connect(self.load_data)  # Выполнить функцию browse_folder
        self.findSaddlePointsButton.clicked.connect(self.find_saddle_poins)  # Выполнить функцию browse_folder

    def find_saddle_poins(self):
        data = self.data.copy()
        transpose_data = list(map(list, zip(*data)))

        # Поиск максимумов в транспозе
        max_col_vals = []
        for row in range(len(transpose_data)):
            max_col_vals.append(max(transpose_data[row]))

        # Поиск минимумов в оригинале и сравнение с максимумами транспоза
        self.saddle_points.clear()
        for row in range(len(data)):
            min_row_val = min(data[row])
            min_row_idx = [i for i, j in enumerate(data[row]) if j == min_row_val]
            for idx in min_row_idx:
                if max_col_vals[idx] <= data[row][idx]:
                    self.saddle_points.append((row, idx))

        print(self.saddle_points)

    def load_data(self):
        filename = QtWidgets.QFileDialog.getOpenFileName(self, "Выберите фвйл (txt, csv)",
                                                         "/home/liza/PycharmProjects/gameTheory",
                                                         "xlsx (*.xlsx);; txt (*.txt)")

        filename = filename[0]
        ext = filename.split('.')[-1]
        if ext == 'txt':
            data = self.read_data_from_txt(filename)
        else:
            data = self.read_data_from_xlsx(filename)

        self.set_table_data(data)
        self.data = data

    def read_data_from_xlsx(self, filename):
        if filename:
            df = pd.read_excel(filename, header=None)
            data = df.values.tolist()
            return data

    def read_data_from_txt(self, filename):
        if filename:
            f = open(filename, 'r')
            with f:
                data = f.read()
        data = data.split('\n')[:-1]
        data = [[int(elem) for elem in line.split()] for line in data]
        return data

    def set_table_data(self, data):
        numrows = len(data)
        numcols = len(data[0])

        self.table.setColumnCount(numcols)
        self.table.setRowCount(numrows)

        self.table.clear()
        for row in range(numrows):
            for column in range(numcols):
                self.table.setItem(row, column, QTableWidgetItem((str(data[row][column]))))


def main():
    app = QtWidgets.QApplication(sys.argv)
    window = ExampleApp()
    window.show()
    app.exec_()


if __name__ == '__main__':
    main()
