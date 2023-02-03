import easygui

import os
import csv
import sys

from random import randint

from Result import Result

from Window import Ui_Form
from PyQt5 import QtWidgets
from PyQt5.QtGui import QPen
from PyQt5.QtWidgets import QListWidgetItem, QTableWidgetItem
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtGui import QColor
from PyQt5.QtCore import Qt

import xlsxwriter


# Tab for showing raw data
# Option to reduce number of injections plotted

# Get data corresponding to selected items
def select_data():
    items = ui.listWidget.selectedItems()
    result_list = []
    for item in items:
        match = item.text()
        for result in results:
            if match == result.name:
                result_list.append(result)
    return result_list


def export_data():
    summary_table = [['Name', 'Slope', 'R-squared']]
    injection_export_table = [['Injection number', 'Injection length', 'Injection size', 'Concentration', 'Heat rate']]
    for result in select_data():
        summary_table.append([result.name, result.slope, result.rsquared])
        injection_export_table.append([])
    filename = easygui.filesavebox(msg='', title='Export data to Excel', default='', filetypes='.xlsx')
    if filename != None:
        workbook = xlsxwriter.Workbook(filename)

        # Create Excel sheet that contains all exported fits
        worksheet = workbook.add_worksheet('Summary')
        row = 0
        col = 0
        for name, slope, rsquared in (summary_table):
            if row > 0:
                workbook.add_worksheet(name)
            worksheet.write(row, col, name)
            worksheet.write(row, col + 1, slope)
            worksheet.write(row, col + 2, rsquared)
            row += 1

        workbook.close()


def retrieve_file():
    filenames = easygui.fileopenbox(default="*.itc", multiple=True)
    return filenames


# Plot graph by pulling data from a result object
def draw_graphs(result):
    # Scatter plot
    ui.graphWidget.plot(result.x, result.y, pen=None, symbol='o', symbolBrush=result.color, symbolSize=10)
    # Plot linear fit
    pen = QPen(result.color, 0.02, Qt.SolidLine, Qt.RoundCap)
    ui.graphWidget.plot(result.fit_x, result.fit_y, pen=pen)


def check_match(name):
    for result in results:
        if name == result.name:
            return True


def draw_item():
    ui.graphWidget.clear()
    for result in select_data():
        draw_graphs(result)


def close_file():
    ui.injection_table.clear()
    ui.slope_label.clear()
    ui.rsquared_label.clear()
    ui.results_widget.clear()
    ui.results_widget.setHorizontalHeaderLabels(['Conc.', 'Heat effect'])
    items = ui.listWidget.selectedItems()
    for item in items:
        match = item.text()
        for result in results:
            if match == result.name:
                ui.listWidget.takeItem(ui.listWidget.row(item))
                results.remove(result)


def update_data(result):
    ui.injection_table.setText(str(result.injection_sizes) + "\n" + str(result.injection_spacings))
    ui.slope_label.setText(f'Slope: {str(round(result.slope, 4))}')
    ui.rsquared_label.setText(f'R-squared: {str(round(result.rsquared, 4))}')
    ui.results_widget.setRowCount(len(result.injection_sizes) + 1)
    for i, x in enumerate(result.x):
        item = QTableWidgetItem(str(x))
        ui.results_widget.setItem(i, 0, item)
    for i, y in enumerate(result.y):
        item = QTableWidgetItem(str(y))
        ui.results_widget.setItem(i, 1, item)


# def convert_heat():
# Take syringe concentration and molecular weight, do conversion and return values to plot

def display_data(item):
    match = item.text()
    for result in results:
        if match == result.name:
            update_data(result)


def open_file():
    # Get .itc files
    files = retrieve_file()
    if files != None:
        for file in files:
            # Import ITC results text file and convert to list object
            with open(file) as f:
                content = csv.reader(f, delimiter=',')
                content_list = list(content)
            # basename -> get filename with extension
            # splitext -> split filename and extension
            filename = os.path.splitext(os.path.basename(file))[0]

            # Check if file is already open before continuing
            match_boolean = check_match(filename)
            if match_boolean:
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Critical)
                msg.setText(f'{filename} is already open')
                msg.exec_()
                break
            else:
                result = Result(filename, content_list, ui.check_ignore.isChecked(),
                                QColor(randint(25, 235), randint(25, 235), randint(25, 235), 80))
                item = QListWidgetItem(result.name)
                item.setBackground(result.color)
                ui.listWidget.addItem(item)
                results.append(result)
                draw_graphs(result)
                ui.listWidget.selectAll()


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = Ui_Form()
    ui.setupUi(Form)
    ui.graphWidget.setBackground('w')
    results = []
    ui.open_button.clicked.connect(open_file)
    ui.close_button.clicked.connect(close_file)
    ui.export_button.clicked.connect(export_data)
    ui.listWidget.itemSelectionChanged.connect(draw_item)
    ui.listWidget.itemClicked.connect(display_data)
    ui.results_widget.setColumnCount(2)
    ui.results_widget.setHorizontalHeaderLabels(['Conc.', 'Heat effect'])

    Form.show()
    sys.exit(app.exec_())
