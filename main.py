import sys

import pandas as pd
from PyQt5 import QtWidgets
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QTableWidgetItem

import design


class ExampleApp(QtWidgets.QWidget, design.Ui_Form):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.saddle_points = []
        self.data = []

        self.loadDataButton.clicked.connect(self.load_data)
        self.findSaddlePointsButton.clicked.connect(self.find_saddle_poins)

        self.saveTableValuesButton.clicked.connect(self.save_table_values)
        self.changeTableSizeButton.clicked.connect(self.find_saddle_poins)

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

        bold_font = QFont()
        bold_font.setBold(True)
        for row, column in self.saddle_points:
            self.table.item(row, column).setFont(bold_font)

        if self.saddle_points:
            win_saddle_point = self.saddle_points[0]
            win_value = self.table.item(win_saddle_point[0], win_saddle_point[1]).text()
        else:
            win_value = 'None'
        self.win_value_on_clean_strategy.setText(win_value)

    def load_data(self):
        filename = QtWidgets.QFileDialog.getOpenFileName(self, "Выберите файл (txt, csv)",
                                                         "/home/liza/PycharmProjects/gameTheory",
                                                         "xlsx (*.xlsx);; txt (*.txt)")

        filename = filename[0]
        ext = filename.split('.')[-1]
        if ext == 'txt':
            data = self.read_data_from_txt(filename)
        else:
            data = self.read_data_from_xlsx(filename)

        self.data = data
        self.set_table_data()

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

    def set_table_data(self):
        numrows = len(self.data)
        numcols = len(self.data[0])

        self.table.setColumnCount(numcols)
        self.table.setRowCount(numrows)

        self.table.clear()
        for row in range(numrows):
            for column in range(numcols):
                self.table.setItem(row, column, QTableWidgetItem((str(self.data[row][column]))))

    def save_table_values(self):

        self.data.clear()
        for row in range(self.table.columnCount()):
            temp_row = []
            for column in range(self.table.rowCount()):
                item_val = QTableWidgetItem(self.table.item(row, column)).text()
                temp_row.append(item_val)
            self.data.append(temp_row)
        self.set_table_data()


def main():
    app = QtWidgets.QApplication(sys.argv)
    window = ExampleApp()
    window.show()
    app.exec_()


if __name__ == '__main__':
    main()
