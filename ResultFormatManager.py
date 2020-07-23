from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QStandardItemModel, QStandardItem
from PyQt5.QtWidgets import QDialog, QTableView, QPushButton, QHBoxLayout, QVBoxLayout
from PyQt5.QtCore import pyqtSignal


class ResultFormatManager(QDialog):
    apply_done = pyqtSignal()

    def __init__(self, data: list):
        super().__init__()
        self.setStyleSheet(open('stylesheet/default.qss').read())
        # self.setWindowFlag(Qt.WindowMinimizeButtonHint, True)
        self.setAttribute(Qt.WA_QuitOnClose)
        self.data_json = data
        self.data_json.append("")

        layout = QVBoxLayout()
        self.setLayout(layout)

        self.table = QTableView()
        self.model = QStandardItemModel()
        self.model.setHorizontalHeaderLabels(['Object name'])
        self.model.itemChanged.connect(self.data_change)
        self.table.setModel(self.model)
        self.import_data(self.data_json)
        header = self.table.horizontalHeader()
        header.setSectionResizeMode(0, QtWidgets.QHeaderView.Stretch)

        apply = QPushButton()
        apply.setText("Apply")
        apply.pressed.connect(self.apply)
        cancel = QPushButton()
        cancel.setText("Cancel")
        cancel.pressed.connect(self.cancel)

        bar = QHBoxLayout()
        bar.addStretch()
        bar.addWidget(cancel, alignment=Qt.AlignRight)
        bar.addWidget(apply, alignment=Qt.AlignRight)

        layout.addWidget(self.table)
        layout.addLayout(bar)

    def import_data(self, data_list):
        row = self.model.invisibleRootItem()
        for data in data_list:
            item1 = QStandardItem()
            item1.setText(data)
            item1.setData(data)
            item1.setEditable(True)
            row.appendRow(item1)

    def cancel(self):
        self.close()

    def data_change(self, arg: QStandardItem):
        data = arg.data()
        text = arg.text()

        if data != "" or text != "":
            index = self.data_json.index(data)
            self.data_json.insert(index, text)
        if data != "" and text != "":
            self.data_json.remove(data)

        self.model.clear()
        self.model.setHorizontalHeaderLabels(['Object name'])
        header = self.table.horizontalHeader()
        header.setSectionResizeMode(0, QtWidgets.QHeaderView.Stretch)
        self.import_data(self.data_json)

    def apply(self):
        self.apply_done.emit()
        self.accept()

    def data(self):
        return self.data_json

    def set_data(self, data: list):
        self.data_json = data
