import sys

import numpy as np
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
        self.transpose_data = []

        self.loadDataButton.clicked.connect(self.load_data)
        self.getWinCleanStrategyVal.clicked.connect(self.get_win_in_clean_strategy)
        self.getWinMixedStrategyVal.clicked.connect(self.get_win_in_mixed_strategy)

        self.saveTableValuesButton.clicked.connect(self.save_table_values)
        # self.changeTableSizeButton.clicked.connect(self.get_win_in_clean_strategy)

    def get_max_col_array(self):
        data = self.data.copy()
        transpose_data = self.transpose_data.copy()
        max_col_vals = []
        for row in range(len(transpose_data)):
            max_col_vals.append(max(transpose_data[row]))
        return max_col_vals

    def get_min_row_array(self):
        data = self.data.copy()
        min_row_vals = []
        for row in range(len(data)):
            min_row_vals.append(min(data[row]))
        return min_row_vals

    def get_win_in_clean_strategy(self):
        if self.data:
            data = self.data.copy()

            # Поиск максимумов в транспозе
            max_col_vals = self.get_max_col_array()
            # Поиск минимумов в оригинале
            min_row_vals = self.get_min_row_array()

            # Поиск седловых точек
            self.saddle_points.clear()
            for row, min_row_val in enumerate(min_row_vals):
                min_row_idx = [i for i, j in enumerate(data[row]) if j == min_row_val]
                for idx in min_row_idx:
                    if max_col_vals[idx] <= data[row][idx]:
                        self.saddle_points.append((row, idx))

            # Выделение седловых точек жирным
            bold_font = QFont()
            bold_font.setBold(True)
            for row, column in self.saddle_points:
                self.table.item(row, column).setFont(bold_font)

            # Напечатать значение игры в чистых стратегиях
            if self.saddle_points:
                win_saddle_point = self.saddle_points[0]
                win_value = self.table.item(win_saddle_point[0], win_saddle_point[1]).text()
            else:
                win_value = 'None'
        else:
            win_value = 'None'

        self.win_value_on_clean_strategy.setText(win_value)

    def get_win_in_mixed_strategy(self):
        if self.data:
            # Поиск максимума
            self.v2_down_mixed_strategy.setText(str(max(self.get_min_row_array())))
            # Поиск минимума
            self.v1_up_mixed_strategy.setText(str(min(self.get_max_col_array())))

            if self.vector_p.toPlainText() and self.vector_q.toPlainText():
                self.p = [float(elem) for elem in self.vector_p.toPlainText().split()]
                self.q = [float(elem) for elem in self.vector_q.toPlainText().split()]

                xmin = min(np.dot(self.p, self.data))
                ymax = max(np.dot(self.q, self.transpose_data))

                if xmin == ymax:
                    win_value = str(xmin)
                else:
                    win_value = 'None'
            else:
                win_value = 'None'
        else:
            win_value = 'None'
        self.win_value_on_mixed_strategy.setText(win_value)

        # 0.625 0 0.375 0
        # 0 0.8125 0.1875

    def load_data(self):
        filename = QtWidgets.QFileDialog.getOpenFileName(self, "Выберите файл (txt, csv)",
                                                         "/home/liza/PycharmProjects/gameTheory",
                                                         "txt (*.txt);; xlsx (*.xlsx)")

        filename = filename[0]
        ext = filename.split('.')[-1]
        if ext == 'txt':
            data = self.read_data_from_txt(filename)
        else:
            data = self.read_data_from_xlsx(filename)

        self.data = data
        self.transpose_data = list(map(list, zip(*data)))

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

        self.transpose_data = list(map(list, zip(*self.data)))
        self.set_table_data()


def main():
    app = QtWidgets.QApplication(sys.argv)
    window = ExampleApp()
    window.show()
    app.exec_()


if __name__ == '__main__':
    main()
