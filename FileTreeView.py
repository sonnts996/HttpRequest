import os

from PyQt5 import QtGui
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon, QStandardItem
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLineEdit, QPushButton, QSizePolicy, QTreeView, QMenu, \
    QAction

from module import get_icon_link, get_data_folder
from PyQt5.QtCore import pyqtSignal


class FileTreeView(QWidget):
    on_menu_select = pyqtSignal(str, dict)

    def __init__(self):
        super().__init__()
        self.list_file = []
        self.get_data_file()

        v_box = QVBoxLayout()
        v_box.addLayout(self.finder())
        v_box.addWidget(self.tree_view())
        self.setLayout(v_box)

    def finder(self):
        w_find = QLineEdit()
        w_find.setSizePolicy(QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed))

        w_find_button = QPushButton()
        w_find_button.setText("Find")
        w_find_button.setFixedWidth(50)

        h_box = QHBoxLayout()
        h_box.addWidget(w_find)
        h_box.addWidget(w_find_button, 1)
        return h_box

    def get_data_file(self):
        self.list_file = self.create_list(get_data_folder())

    def create_list(self, dir):
        lst = os.listdir(path=dir)
        list_file = []
        for f in lst:
            path = dir + "\\" + f
            file = {}
            if os.path.isdir(path):
                file["dir"] = dir
                file["name"] = f
                file["isDir"] = True
                file["child"] = self.create_list(path)
            else:
                file["dir"] = dir
                file["name"] = f
                file["isDir"] = False

            list_file.append(file)
        return list_file

    def tree_view(self):
        self.tree = QTreeView()
        self.tree.setSizePolicy(QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding))

        self.tree.setContextMenuPolicy(Qt.CustomContextMenu)
        self.tree.customContextMenuRequested.connect(self.openMenu)

        self.model = QtGui.QStandardItemModel()
        self.model.setHorizontalHeaderLabels(['List API'])
        self.tree.header().setDefaultSectionSize(180)
        self.tree.setModel(self.model)
        self.import_data(self.model.invisibleRootItem(), self.list_file)
        self.tree.expandAll()

        return self.tree

    def import_data(self, parent_item, list):
        for i in list:
            if i["isDir"]:
                item = QStandardItem(i["name"])
                item.setEditable(False)
                item.setIcon(QIcon(get_icon_link("folder_yellow.svg")))
                item.setData(i)
                parent_item.appendRow(item)
                self.import_data(item, i["child"])
            else:
                item = QStandardItem(i["name"])
                item.setEditable(False)
                item.setIcon(QIcon(get_icon_link("text_snippet.svg")))
                item.setData(i)
                parent_item.appendRow(item)

    def openMenu(self, position):
        indexes = self.tree.selectedIndexes()
        level = 0
        data = {}
        if len(indexes) > 0:
            index = indexes[0]
            item = self.model.itemFromIndex(index)
            data = item.data()
            if data['isDir']:
                level = 1
            else:
                level = 2

        menu = QMenu()
        menu.setStyleSheet(open('stylesheet/default.qss').read())

        # Create preference action
        rename_action = QAction(QIcon(get_icon_link('edit.svg')), '&Rename', self)
        rename_action.setStatusTip('Rename')
        # exitAction.triggered.connect(self.exitCall)

        # Create preference action
        new_action = QAction(QIcon(get_icon_link('create_new_folder.svg')), '&New Folder', self)
        new_action.setStatusTip('New Folder')
        # exitAction.triggered.connect(self.exitCall)

        # Create preference action
        refresh_action = QAction(QIcon(get_icon_link('refresh.svg')), '&Refresh', self)
        refresh_action.setStatusTip('Refresh')
        # exitAction.triggered.connect(self.exitCall)

        # Create preference action
        delete_action = QAction(QIcon(get_icon_link('delete_forever.svg')), '&Delete', self)
        delete_action.setStatusTip('Delete')
        # exitAction.triggered.connect(self.exitCall)

        # Create preference action
        open_action = QAction(QIcon(get_icon_link('open_in_new.svg')), '&Open', self)
        open_action.setStatusTip('Open file')
        # open_action.triggered.connect(self.open_file)

        # Create preference action
        expand_action = QAction(QIcon(), '&Expand', self)
        expand_action.setStatusTip('Expand')
        # exitAction.triggered.connect(self.exitCall)

        # Create preference action
        collapse_action = QAction(QIcon(), '&Collapse', self)
        collapse_action.setStatusTip('Collapse')
        # exitAction.triggered.connect(self.exitCall)

        # Create preference action
        copy_action = QAction(QIcon(get_icon_link('content_copy.svg')), '&Copy', self)
        copy_action.setStatusTip('Copy')
        # exitAction.triggered.connect(self.exitCall)

        # Create preference action
        move_action = QAction(QIcon(get_icon_link('zoom_out_map.svg')), '&Move', self)
        move_action.setStatusTip('Move')
        # exitAction.triggered.connect(self.exitCall)

        if level == 1:
            menu.addAction(rename_action)
            menu.addAction(new_action)
            menu.addSeparator()
            menu.addAction(refresh_action)
            menu.addAction(expand_action)
            menu.addAction(collapse_action)
            menu.addSeparator()
            menu.addAction(delete_action)
        elif level == 2:
            menu.addAction(open_action)
            menu.addAction(refresh_action)
            menu.addSeparator()
            menu.addAction(rename_action)
            menu.addAction(copy_action)
            menu.addAction(move_action)
            menu.addSeparator()
            menu.addAction(delete_action)
        else:
            menu.addAction(new_action)
            menu.addAction(refresh_action)

        action = menu.exec_(self.tree.viewport().mapToGlobal(position))
        if action == open_action:
            self.on_menu_select.emit("open", data)
