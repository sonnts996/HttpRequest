import json
import os

from PyQt5.QtCore import Qt, QEvent
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtGui import QIcon, QStandardItemModel, QStandardItem
from PyQt5.QtWidgets import QWidget, QTabWidget, QTextEdit, QHBoxLayout, QPushButton, QSplitter, QLineEdit, QComboBox, \
    QSizePolicy, QVBoxLayout, QGroupBox, QTreeView, QLabel

import Application
from module import label_widget, get_icon_link, color_json, get_link_file, get_data_folder
from modules import httprequest
from modules.JSONEditor import JSONEditor


class APIConfigure(QSplitter):
    console = pyqtSignal(str, str)
    result = pyqtSignal(dict, bool)

    def __init__(self, parent: Application, data=None):
        super().__init__()
        self.w_widget_tab = QTabWidget()
        self.model = QStandardItemModel()
        self.w_description = QTextEdit()
        self.file_name = QLineEdit()
        self.folder = QComboBox()
        self.w_api_param = QComboBox()
        self.w_api_link = QComboBox()
        self.w_api_type = QComboBox()
        self.w_api = QLineEdit()
        self.w_group = QTreeView()
        self.w_json_edit = JSONEditor()

        self.level = 0
        self.api_data = {}
        self.api_json = []
        self.list_folder = []
        self.is_json_parse_err = False
        self.json_param = {}
        self.file_data = data

        if data is not None:
            try:
                self.api_data = json.loads(open(data['dir'] + "\\" + data['name']).read())
            except Exception as ex:
                self.console.emit("Load data:", str(ex))
                print(ex)

        self.setOrientation(Qt.Vertical)
        self.component()

        parent.api_data_change.connect(self.load_api)

    def component(self):
        self.w_json_edit.setLineWrapMode(QTextEdit.NoWrap)
        self.w_json_edit.setAcceptRichText(True)
        if 'config' in self.api_data:
            if 'param' in self.api_data['config']:
                self.json_param = self.api_data['config']['param']
                self.w_json_edit.setDocument(color_json(self.api_data['config']['param']))
                self.parse_param_to_table()
        self.w_json_edit.installEventFilter(self)

        self.w_widget_tab.addTab(self.w_group, "UI")
        self.w_widget_tab.addTab(self.w_json_edit, "JSON")
        self.w_widget_tab.currentChanged.connect(self.tab_selected)

        w_run = QPushButton()
        w_run.setIcon(QIcon(get_icon_link('play_arrow.svg')))
        w_run.setText("Run")
        w_run.setToolTip("Run API call (Ctrl+R)")
        w_run.pressed.connect(self.run_api_without_save)

        w_run_save = QPushButton()
        w_run_save.setIcon(QIcon(get_icon_link('play_circle_outline.svg')))
        w_run_save.setText("Run && Save")
        w_run_save.setToolTip("Run and Save API call (Ctrl++Shift+R)")
        w_run_save.pressed.connect(self.run_api_save)

        w_sync = QPushButton()
        w_sync.setText("Sync")
        w_sync.setIcon(QIcon(get_icon_link('refresh.svg')))
        w_sync.setToolTip("Sync param (Ctrl+Shift+C)")
        w_sync.pressed.connect(self.sync_param)

        l_action = QHBoxLayout()
        l_action.addWidget(w_run, alignment=Qt.AlignLeft)
        l_action.addWidget(w_run_save, alignment=Qt.AlignLeft)
        l_action.addStretch()
        l_action.addWidget(w_sync, alignment=Qt.AlignRight)

        w_group2 = QWidget()
        w_group2.setLayout(l_action)
        w_group2.setMaximumHeight(50)

        self.addWidget(self.header())
        self.addWidget(self.w_widget_tab)
        self.addWidget(w_group2)
        self.setStretchFactor(0, 1)
        self.setStretchFactor(1, 2)
        self.setStretchFactor(2, 1)
        self.setStretchFactor(3, 1)

    def header(self):
        if 'config' in self.api_data:
            if 'api' in self.api_data['config']:
                self.w_api.setText(self.api_data['config']['api'])

        self.w_api.textChanged.connect(self.api_text_change)

        self.w_api_type.addItem("POST")
        self.w_api_type.addItem("GET")
        if 'config' in self.api_data:
            if 'protocol' in self.api_data['config']:
                if self.api_data['config']['protocol'] == 'POST':
                    self.w_api_type.setCurrentIndex(0)
                elif self.api_data['config']['protocol'] == 'GET':
                    self.w_api_type.setCurrentIndex(1)

        self.load_api()

        self.w_api_param.addItem("Param")
        self.w_api_param.addItem("JSON")
        if 'config' in self.api_data:
            if 'type' in self.api_data['config']:
                if self.api_data['config']['type'] == 'Param':
                    self.w_api_param.setCurrentIndex(0)
                elif self.api_data['config']['type'] == 'JSON':
                    self.w_api_param.setCurrentIndex(1)

        self.list_folder = []
        file = {"dir": get_data_folder(), "name": "root", "isDir": True}
        self.list_folder.append(file)
        self.load_folder(get_data_folder())
        if self.file_data is not None:
            if self.file_data['name'] == 'root':
                for data in self.list_folder:
                    self.folder.addItem(data['name'], data)
                self.folder.setCurrentIndex(0)
            else:
                index = 0
                count = 0
                for data in self.list_folder:
                    self.folder.addItem(data['name'], data)
                    if self.file_data['dir'] == data['dir']:
                        index = count
                    count += 1
                self.folder.setCurrentIndex(index)
        else:
            for data in self.list_folder:
                self.folder.addItem(data['name'], data)

        self.file_name.setSizePolicy(QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed))
        if self.file_data is not None:
            self.file_name.setText(self.file_data['name'])

        save_box = QHBoxLayout()
        save_box.addWidget(self.folder)
        save_box.addWidget(self.file_name)

        save_label = QLabel()
        save_label.setText("Save: ")

        out_save_box = QVBoxLayout()
        out_save_box.addWidget(save_label, alignment=Qt.AlignTop)
        out_save_box.addLayout(save_box)

        self.w_description.setMinimumHeight(50)
        self.w_description.setSizePolicy(QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed))
        if 'save' in self.api_data:
            if 'description' in self.api_data['save']:
                self.w_description.setText(self.api_data['save']['description'])

        l_box = QVBoxLayout()
        l_box.addWidget(self.w_api, alignment=Qt.AlignTop)
        l_box.addLayout(label_widget("Protocol: ", self.w_api_type, 120))
        l_box.addLayout(label_widget("API Link: ", self.w_api_link, 120))
        l_box.addLayout(label_widget("Parameter type: ", self.w_api_param, 120))
        l_box.addLayout(out_save_box)
        l_box.addLayout(label_widget("Description: ", self.w_description, 0, 1))

        gr_header = QGroupBox()
        gr_header.setLayout(l_box)
        gr_header.setTitle("API")
        gr_header.setMaximumHeight(300)
        return gr_header

    def tab_selected(self, arg=None):
        if arg is not None:
            if arg == 0:
                self.try_sync_json_table()
            else:
                if not self.is_json_parse_err:
                    self.w_json_edit.setDocument(color_json(self.json_param))

    def sync_param(self):
        if self.w_widget_tab.currentIndex() == 0:
            self.w_json_edit.setDocument(color_json(self.json_param))
        elif self.w_widget_tab.currentIndex() == 1:
            self.try_sync_json_table()

    def try_sync_json_table(self):
        self.is_json_parse_err = False
        str_param = self.w_json_edit.toPlainText()
        try:
            if str_param == "" or str_param.isspace():
                self.json_param = {}
            else:
                self.json_param = json.loads(str_param)
            self.w_json_edit.setDocument(color_json(self.json_param))
            self.is_json_parse_err = False
        except Exception as ex:
            print(ex)
            self.console.emit("JSON Param", str(ex))
            self.is_json_parse_err = True
        finally:
            if self.is_json_parse_err:
                self.w_json_edit.setDocument(color_json(str_param))
            else:
                self.w_json_edit.setDocument(color_json(self.json_param))
            self.parse_param_to_table()
        return self.is_json_parse_err

    def parse_param_to_table(self):
        self.model = QStandardItemModel()
        self.model.setHorizontalHeaderLabels(['key', 'value'])
        self.model.itemChanged.connect(self.data_change)
        self.w_group.setModel(self.model)
        self.level = 0
        self.create_param_ui(self.model.invisibleRootItem(), self.json_param)
        self.w_group.expandAll()

    def create_param_ui(self, parent, obj):
        if not isinstance(obj, list):
            for key in obj:
                self.level += 1
                if isinstance(obj[key], dict) or isinstance(obj[key], list):
                    item = QStandardItem(key)
                    item.setEditable(False)
                    self.create_param_ui(item, obj[key])
                    parent.appendRow(item)
                else:
                    item = QStandardItem(key)
                    item.setEditable(False)
                    value = QStandardItem(str(obj[key]))
                    value.emitDataChanged()
                    data = {'key': key, "level": self.level}
                    value.setData(data)
                    parent.appendRow([item, value])
        else:
            for i in range(len(obj)):
                self.level += 1
                item = QStandardItem(str(i))
                item.setEditable(False)
                self.create_param_ui(item, obj[i])
                parent.appendRow(item)

    def data_change(self, arg: QStandardItem):
        data = arg.data()
        if "key" in data:
            if "level" in data:
                self.level = 0
                self.change(self.json_param, data['key'], arg.text(), data['level'])

    def change(self, obj, key, update, level):
        if level == self.level:
            if key in obj:
                obj[key] = update
        else:
            if not isinstance(obj, list):
                for k in obj:
                    self.level += 1
                    if isinstance(obj[k], dict) or isinstance(obj[k], list):
                        self.change(obj[k], key, update, level)
                    else:
                        if self.level == level:
                            obj[key] = update
            else:
                for i in range(len(obj)):
                    self.level += 1
                    self.change(obj[i], key, update, level)

    def load_api(self):
        if os.path.isfile(get_link_file()):
            f = open(get_link_file(), "r", encoding="utf-8")
            data = f.read()
            f.close()
            try:
                self.api_json = json.loads(data)
            except Exception as ex:
                print(ex)
                self.console.emit("Get API Link: ", str(ex))
                self.api_json = []

        self.w_api_link.clear()
        selection = 0
        link = {}
        if 'config' in self.api_data:
            if 'link' in self.api_data['config']:
                link = self.api_data['config']['link']
        count = 0
        for data in self.api_json:
            self.w_api_link.addItem(data['name'], data)
            count += 1
            if 'link' in link:
                if data['link'] == link['link']:
                    selection = count
        self.w_api_link.setCurrentIndex(selection)

    def load_folder(self, parent_dir):
        lst = os.listdir(path=parent_dir)
        for f in lst:
            path = parent_dir + "\\" + f
            file = {}
            if os.path.isdir(path):
                file["dir"] = parent_dir
                file["name"] = f
                file["isDir"] = True
                self.load_folder(path)
                self.list_folder.append(file)

    def api_text_change(self):
        text = self.w_api.text()
        if (self.file_name.text() in text or text in self.file_name.text()) and abs(
                len(text) - len(self.file_name.text())) <= 1:
            self.file_name.setText(self.w_api.text())
        elif self.file_name.text() == "":
            self.file_name.setText(self.w_api.text())

    def run_api(self, is_save: bool):
        api = self.w_api.text()
        if api != "":
            protocol = self.w_api_type.currentText()
            link = self.api_json[self.w_api_link.currentIndex()]
            type_api = self.w_api_param.currentText()
            param = self.json_param
            if self.json_param == {} and (
                    self.w_json_edit.toPlainText() != "" or self.w_json_edit.toPlainText() != "{}"):
                if not self.try_sync_json_table():
                    param = self.json_param
                else:
                    self.console.emit("Param arror", "Param json error!!!")
                    return 0

            data = {'api': api, "protocol": protocol, 'type': type_api, 'link': link, 'param': param}

            response = {}
            if protocol == "GET":
                response = httprequest.get(link['link'], api, param)
            elif protocol == "POST":
                if type_api == 'JSON':
                    response = httprequest.post(link['link'], api, param)
                elif type_api == 'Param':
                    response = httprequest.post_param(link['link'], api, param)

            self.api_data["config"] = data
            self.api_data['response'] = response
            self.api_data['save'] = {}
            self.api_data['save']['description'] = self.w_description.toPlainText()
            self.api_data['save']['folder'] = self.list_folder[self.folder.currentIndex()]
            self.api_data['save']['name'] = self.file_name.text()

            self.result.emit(self.api_data, is_save)
        else:
            self.console.emit("Run API:", "No API")

    def run_api_save(self):
        self.run_api(True)

    def run_api_without_save(self):
        self.run_api(False)


