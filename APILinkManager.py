import json
import os

from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtGui import QStandardItemModel, QStandardItem
from PyQt5.QtWidgets import QDialog, QTableView, QHBoxLayout, QVBoxLayout, QPushButton

from module import get_link_file


class APILinkManager(QDialog):
    console = pyqtSignal(str, str)

    def __init__(self):
        super().__init__()
        self.setStyleSheet(open('stylesheet/default.qss').read())
        self.data_json = []
        self.open_config()

        self.table = QTableView()
        self.model = QStandardItemModel()
        self.model.setHorizontalHeaderLabels(['Index', 'Name', 'Link', 'Delete'])
        self.model.itemChanged.connect(self.data_change)
        self.table.setModel(self.model)
        self.import_data(self.data_json)
        header = self.table.horizontalHeader()
        header.setSectionResizeMode(0, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(1, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(2, QtWidgets.QHeaderView.Stretch)
        header.setSectionResizeMode(3, QtWidgets.QHeaderView.ResizeToContents)

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

        layout = QVBoxLayout()
        layout.addWidget(self.table)
        layout.addLayout(bar)
        self.setLayout(layout)

    def open_config(self):
        if os.path.isfile(get_link_file()):
            f = open(get_link_file(), "r", encoding="utf-8")
            data = f.read()
            f.close()
            try:
                self.data_json = json.loads(data)
            except Exception as ex:
                print(ex)
                self.console.emit("Get API Link: ", str(ex))
                self.data_json = []

        data_new = {'id': -1, 'name': "example", 'link': "example.com"}
        self.data_json.append(data_new)

    def import_data(self, data_list):
        row = self.model.invisibleRootItem()
        for data in data_list:
            item1 = QStandardItem()
            if data['id'] == -1:
                item1.setText("*")
            else:
                item1.setText(str(data['id']))
            item1.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
            item1.setEditable(False)
            item2 = QStandardItem()
            item2.setText(data['name'])
            item3 = QStandardItem()
            item3.setText(data['link'])
            item4 = QStandardItem()
            item4.setText("")
            item4.setCheckable(True)
            item4.setEditable(False)
            item4.setTextAlignment(Qt.AlignCenter)
            if "delete" in data:
                if data['delete']:
                    item4.setCheckState(Qt.Checked)
                else:
                    item4.setCheckState(Qt.Unchecked)

            row.appendRow([item1, item2, item3, item4])

    def cancel(self):
        self.close()

    def data_change(self, arg: QStandardItem):
        id2 = self.model.item(arg.row(), 0)
        name = self.model.item(arg.row(), 1)
        link = self.model.item(arg.row(), 2)
        delete = self.model.item(arg.row(), 3)
        if id2.text() != "*":
            for data in self.data_json:
                if str(data['id']) == id2.text():
                    data['delete'] = delete.checkState() == Qt.Checked
                    data['name'] = name.text()
                    data['link'] = link.text()

        else:
            for data in self.data_json:
                if data['id'] == -1:
                    index = max(self.data_json, key=lambda item: item['id'])
                    if isinstance(index["id"], int):
                        data['id'] = index["id"] + 1
                    else:
                        data['id'] = 1
                    data['name'] = name.text()
                    data['link'] = link.text()
            data_new = {'id': -1, 'name': "example", 'link': "example.com"}
            self.data_json.append(data_new)

        self.model.clear()
        self.model.setHorizontalHeaderLabels(['ID', 'Name', 'Link', 'Delete'])

        header = self.table.horizontalHeader()
        header.setSectionResizeMode(0, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(1, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(2, QtWidgets.QHeaderView.Stretch)
        header.setSectionResizeMode(3, QtWidgets.QHeaderView.ResizeToContents)
        self.import_data(self.data_json)

    def apply(self):
        for data in self.data_json:
            if data["id"] == -1:
                self.data_json.remove(data)
            elif "delete" in data:
                if data['delete']:
                    self.data_json.remove(data)

        formatted_json = json.dumps(self.data_json, sort_keys=True, indent=4)
        fout = open(get_link_file(), "w", encoding="utf-8")
        fout.write(formatted_json)
        fout.close()
        print("save output to: " + get_link_file())
        self.accept()
