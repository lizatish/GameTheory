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
        self.savePQValues.clicked.connect(self.save_data_vectorsPQ)

        self.getStrictReduction.clicked.connect(self.get_strict_reduction)
        self.getUnstrictReduction.clicked.connect(self.get_unstrict_reduction)

        self.get2in2solution.clicked.connect(self.get_mixed_strategy_solution_2in2)
        self.plot2in2solution.clicked.connect(self.plot_mixed_strategy_solution_2in2)

        self.getsolution_2n_m2.clicked.connect(self.get_grapho_analytical_solution)

    def get_grapho_analytical_solution(self):

        if self.data:
            has_reduction = True
            while has_reduction:
                has_reduction = self.get_unstrict_reduction()
            self.plot2.canvas.ax.clear()

            n = len(self.data[0])
            m = len(self.data)
            if m > n:
                data = self.transpose_data
                n, m = m, n
            else:
                data = self.data

            color = ['y', 'm', 'c', 'g', 'b', 'k', 'darkgreen', 'lightblue', 'darkblue', 'darkgreen']
            p1 = np.arange(2)
            for i in range(n):
                y1 = (data[0][i] - data[1][i]) * p1 + data[1][i]
                self.plot2.canvas.ax.plot(p1, y1, color=color[i], linewidth=1.5)

            intersects = []
            for i in range(n - 1):
                y1 = (data[0][i] - data[1][i]) * p1 + data[1][i]
                y2 = (data[0][i + 1] - data[1][i + 1]) * p1 + data[1][i + 1]
                ix, iy = self.get_intersect((p1[0], y1[0]), (p1[1], y1[1]),
                                            (p1[0], y2[0]), (p1[1], y2[1]))
                if y1[0] < y2[0]:
                    intersects.append((ix, iy, i, i + 1))
                else:
                    intersects.append((ix, iy, i+1, i))

            if n > 2:
                y1 = (data[0][0] - data[1][0]) * p1 + data[1][0]
                y2 = (data[0][-1] - data[1][-1]) * p1 + data[1][-1]
                ix, iy = self.get_intersect((p1[0], y1[0]), (p1[1], y1[1]),
                                            (p1[0], y2[0]), (p1[1], y2[1]))
                if y1[0] < y2[0]:
                    intersects.append((ix, iy, 0,len(data)))
                else:
                    intersects.append((ix, iy, len(data), 0))

            intersects.sort(key=lambda x: x[0])
            red_points = []
            for i in range(len(intersects)):
                if not red_points or red_points[-1] == intersects[i][2]:
                    red_points.append(intersects[i][3])
                    self.plot2.canvas.ax.scatter(intersects[i][0], intersects[i][1], s=40, color='red')

            self.plot2.canvas.ax.grid()
            self.plot2.canvas.draw()

            # win = min(intersects)
            # if intersects.count(win) == 1:
            #     self.win_analyticgraphic.setText(str(win)[:7])
            #
            #     t = intersects.index(win)
            #     u = intersects.index(win) + 1
            #     z = data[1][u] - data[1][t]
            #     x = z + data[0][t] - data[0][u]
            #
            #     p1star = z / x
            #     y = (data[1][u] - data[0][u]) / x
            #     W = abs((data[0][t] * data[1][u] - data[0][u] * data[1][t]) / x)
            #     self.win_analyticgraphic_check.setText(str(W)[:7])
            #
            #     pstar = (p1star, 1 - p1star)
            #     self.maximin_first_player.setText('(' + ', '.join(str(elem)[:4] for elem in pstar) + ')')
            #
            #     # TODO как посчитать вектор q
            #     # qstar = (q1star, q2star, q3star)
            #     # self.maximin_first_player.setText(str(qstar))
            # else:
            #     pass

    def plot_mixed_strategy_solution_2in2(self):
        if self.data:
            x = [0, 1]
            y1 = [self.data[0][0], self.data[1][0]]
            y2 = [self.data[0][1], self.data[1][1]]
            self.plot.canvas.ax.plot(x, y1, color='lightblue', linewidth=1.5)
            self.plot.canvas.ax.plot(x, y2, color='darkgreen', linewidth=1.5)
            self.plot.canvas.ax.xaxis.set_data_interval(0, 1)
            self.plot.canvas.ax.yaxis.set_data_interval(0, max(y2 + y1) + 5)

            x, y = self.get_intersect((x[0], y1[0]), (x[1], y1[1]), (x[0], y2[0]), (x[1], y2[1]))
            self.plot.canvas.ax.scatter(x, y, s=40, color='red')
            self.plot.canvas.ax.grid()
            self.plot.canvas.draw()
            self.win_plot2in2.setText(str(round(y, 4)))
            self.xy_analytic2in2.setText(str(f'({str(round(x, 4))}, {str(round(y, 4))})'))

    def get_mixed_strategy_solution_2in2(self):
        if self.data:
            h22 = self.data[1][1]
            h21 = self.data[1][0]
            h11 = self.data[0][0]
            h12 = self.data[0][1]

            a = h22 - h21
            b = a + h11 - h12
            p1 = a / b
            q1 = (h22 - h12) / b
            W = (h11 * h22 - h12 * h21) / b
            p = [p1, 1 - p1]
            q = [q1, 1 - q1]

            if round(min(np.dot(p, self.data)), 4) == round(max(np.dot(self.data, q)), 4):
                self.win_analytic2in2.setText(str(round(W, 4)))
            else:
                self.win_analytic2in2.setText('Ошибка')

    def get_strict_reduction(self):

        sorted_data = list(reversed(list(sorted(self.data))))
        deleted = set()
        for idx, first_row in enumerate(sorted_data):
            for second_row in sorted_data[idx + 1:]:
                if all(x > y for x, y in zip(first_row, second_row)):
                    deleted.add(tuple(second_row))
        for elem in deleted:
            self.data.pop(self.data.index(list(elem)))
        self.set_table_data(self.data)

        sorted_data = list(reversed(list(sorted(self.transpose_data, reverse=True))))
        deleted = set()
        for idx, first_row in enumerate(sorted_data):
            for second_row in sorted_data[idx + 1:]:
                if all(x < y for x, y in zip(first_row, second_row)):
                    deleted.add(tuple(second_row))
        for elem in deleted:
            self.transpose_data.pop(self.transpose_data.index(list(elem)))
        self.data = list(map(list, zip(*self.transpose_data)))
        self.set_table_data(self.data)
        self.save_table_values()

    def get_unstrict_reduction(self):
        has_reduction = False
        sorted_data = list(reversed(list(sorted(self.data))))
        deleted = set()
        for idx, first_row in enumerate(sorted_data):
            for second_row in sorted_data[idx + 1:]:
                if all(x >= y for x, y in zip(first_row, second_row)):
                    deleted.add(tuple(second_row))
        for elem in deleted:
            self.data.pop(self.data.index(list(elem)))
            has_reduction = True
        self.set_table_data(self.data)

        sorted_data = list(reversed(list(sorted(self.transpose_data, reverse=True))))
        deleted = set()
        for idx, first_row in enumerate(sorted_data):
            for second_row in sorted_data[idx + 1:]:
                if all(x <= y for x, y in zip(first_row, second_row)):
                    deleted.add(tuple(second_row))
        for elem in deleted:
            self.transpose_data.pop(self.transpose_data.index(list(elem)))
            has_reduction = True
        self.data = list(map(list, zip(*self.transpose_data)))
        self.set_table_data(self.data)
        self.save_table_values()

        return has_reduction

    def get_max_col_array(self):
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

    def get_intersect(self, a1, a2, b1, b2):
        """
        Returns the point of intersection of the lines passing through a2,a1 and b2,b1.
        a1: [x, y] a point on the first line
        a2: [x, y] another point on the first line
        b1: [x, y] a point on the second line
        b2: [x, y] another point on the second line
        """
        s = np.vstack([a1, a2, b1, b2])  # s for stacked
        h = np.hstack((s, np.ones((4, 1))))  # h for homogeneous
        l1 = np.cross(h[0], h[1])  # get first line
        l2 = np.cross(h[2], h[3])  # get second line
        x, y, z = np.cross(l1, l2)  # point of intersection
        if z == 0:  # lines are parallel
            return (float('inf'), float('inf'))
        return (x / z, y / z)

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

    def save_data_vectorsPQ(self):
        self.vector_p.setText(self.vector_p.toPlainText())
        self.vector_q.setText(self.vector_q.toPlainText())

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
        self.change_table_size_to(numrows, numcols)

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
                temp_row.append(int(item_val))
            self.data.append(temp_row)

        self.set_table_data(self.data)


def main():
    app = QtWidgets.QApplication(sys.argv)
    window = ExampleApp()
    window.show()
    app.exec_()


if __name__ == '__main__':
    main()
