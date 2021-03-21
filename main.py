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
        self.changeTableSizeButton.clicked.connect(self.change_table_size)

        self.loadDataVectorP.clicked.connect(self.load_data_vectorP)
        self.loadDataVectorQ.clicked.connect(self.load_data_vectorQ)

        self.getStrictReduction.clicked.connect(self.get_strict_reduction)
        self.getUnstrictReduction.clicked.connect(self.get_unstrict_reduction)

    def get_strict_reduction(self):

        if len(self.data) > 1:
            is_break = False
            for idx, first_row in enumerate(self.data):
                for second_row in self.data[idx + 1:]:
                    if all(x > y for x, y in zip(first_row, second_row)):
                        self.data.pop(idx)
                        is_break = True
                        break
                    elif all(x < y for x, y in zip(first_row, second_row)):
                        self.data.pop(idx + 1)
                        is_break = True
                        break

                if is_break:
                    break

            if is_break:
                self.set_table_data(self.data)

            if len(self.data) > 1:
                return

            is_break = False
            for idx, first_row in enumerate(self.transpose_data):
                for second_row in self.transpose_data[idx + 1:]:
                    if all(x > y for x, y in zip(first_row, second_row)):
                        self.transpose_data.pop(idx)
                        is_break = True
                        break
                    elif all(x < y for x, y in zip(first_row, second_row)):
                        self.transpose_data.pop(idx + 1)
                        is_break = True
                        break

                if is_break:
                    break

            if is_break:
                self.set_table_data(list(map(list, zip(*self.transpose_data))))
                self.save_table_values()

    def get_unstrict_reduction(self):

        if len(self.data) > 1:
            is_break = False
            for idx, first_row in enumerate(self.data):
                for second_row in self.data[idx + 1:]:
                    if all(x >= y for x, y in zip(first_row, second_row)):
                        self.data.pop(idx)
                        is_break = True
                        break
                    elif all(x <= y for x, y in zip(first_row, second_row)):
                        self.data.pop(idx + 1)
                        is_break = True
                        break

                if is_break:
                    break

            if is_break:
                self.set_table_data(self.data)

            if len(self.data) > 1:
                return

            is_break = False
            for idx, first_row in enumerate(self.transpose_data):
                for second_row in self.transpose_data[idx + 1:]:
                    if all(x >= y for x, y in zip(first_row, second_row)):
                        self.transpose_data.pop(idx)
                        is_break = True
                        break
                    elif all(x <= y for x, y in zip(first_row, second_row)):
                        self.transpose_data.pop(idx + 1)
                        is_break = True
                        break

                if is_break:
                    break

            if is_break:
                self.set_table_data(list(map(list, zip(*self.transpose_data))))
                self.save_table_values()

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

    def change_table_size(self):
        self.table.setRowCount(self.row_num.value())
        self.table.setColumnCount(self.col_num.value())

    def change_table_size_to(self, row_num, col_num):
        self.row_num.setValue(row_num)
        self.col_num.setValue(col_num)

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
                self.p = [float(elem) for elem in self.vector_p.toPlainText()[1:-1].split(', ')]
                self.q = [float(elem) for elem in self.vector_q.toPlainText()[1:-1].split(', ')]

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

    def load_data_vectorP(self):
        filename = QtWidgets.QFileDialog.getOpenFileName(self, "Выберите файл (txt, csv)",
                                                         "/home/liza/PycharmProjects/gameTheory",
                                                         "txt (*.txt);; xlsx (*.xlsx)")

        filename = filename[0]
        ext = filename.split('.')[-1]
        if ext == 'txt':
            data = self.read_data_from_txt(filename, type='float')
        else:
            data = self.read_data_from_xlsx(filename, type='float')

        self.p = data[0]
        self.vector_p.setText(str(self.p))

    def load_data_vectorQ(self):
        filename = QtWidgets.QFileDialog.getOpenFileName(self, "Выберите файл (txt, csv)",
                                                         "/home/liza/PycharmProjects/gameTheory",
                                                         "txt (*.txt);; xlsx (*.xlsx)")

        filename = filename[0]
        ext = filename.split('.')[-1]
        if ext == 'txt':
            data = self.read_data_from_txt(filename, type='float')
        else:
            data = self.read_data_from_xlsx(filename, type='float')

        self.q = data[0]
        self.vector_q.setText(str(self.q))

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

        self.set_table_data(self.data)

    def read_data_from_xlsx(self, filename, type='int'):
        if filename:
            df = pd.read_excel(filename, header=None)
            data = df.values.tolist()
            if type == 'float':
                data = [[float(elem) for elem in line.split()] for line in data]
            else:
                data = [[int(elem) for elem in line.split()] for line in data]
            return data

    def read_data_from_txt(self, filename, type='int'):
        if filename:
            f = open(filename, 'r')
            with f:
                data = f.read()
        data = data.split('\n')[:-1]
        if type == 'float':
            data = [[float(elem) for elem in line.split()] for line in data]
        else:
            data = [[int(elem) for elem in line.split()] for line in data]
        return data

    def set_table_data(self, data):
        self.transpose_data = list(map(list, zip(*data)))

        numrows = len(data)
        numcols = len(data[0])

        self.table.setColumnCount(numcols)
        self.table.setRowCount(numrows)
        self.change_table_size_to(numcols, numrows)

        self.table.clear()
        for row in range(numrows):
            for column in range(numcols):
                self.table.setItem(row, column, QTableWidgetItem((str(data[row][column]))))

    def save_table_values(self):
        self.data.clear()
        for row in range(self.table.rowCount()):
            temp_row = []
            for column in range(self.table.columnCount()):
                item_val = QTableWidgetItem(self.table.item(row, column)).text()
                temp_row.append(item_val)
            self.data.append(temp_row)

        self.set_table_data(self.data)


def main():
    app = QtWidgets.QApplication(sys.argv)
    window = ExampleApp()
    window.show()
    app.exec_()


if __name__ == '__main__':
    main()
