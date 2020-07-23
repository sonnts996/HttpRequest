import json
import os

from PyQt5.QtCore import Qt, QEvent
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QLabel, QHBoxLayout, QTextEdit, QVBoxLayout, QGroupBox, QPushButton, QSplitter, QCheckBox, \
    QSizePolicy, QMessageBox, QLineEdit

from ResultFormatManager import ResultFormatManager
from module import get_icon_link, color_json
from modules import httprequest
from modules.JSONEditor import JSONEditor


class APIResult(QSplitter):
    save_done = pyqtSignal()

    def __init__(self, data=None):
        super().__init__()
        self.w_format_field = QLineEdit()
        self.w_format_label = QCheckBox()
        self.w_result = JSONEditor()
        self.w_console = JSONEditor()
        self.w_status_code = QLabel()
        self.w_url = QLineEdit()
        self.format_manager = None
        self.api_data = {}
        self.file_data = data
        if data is not None:
            try:
                self.api_data = json.loads(open(data['dir'] + "\\" + data['name']).read())
            except Exception as ex:
                self.console.emit("Load data:", str(ex))
                print(ex)

        self.setOrientation(Qt.Vertical)
        self.component()

    def component(self):
        self.w_url.setText("Url: ")
        self.w_url.setSizePolicy(QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed))
        if "response" in self.api_data:
            if 'url' in self.api_data["response"]:
                self.w_url.setText(self.api_data["response"]['url'])

        self.w_status_code.setText("0 - No API call")
        if "response" in self.api_data:
            if 'status' in self.api_data["response"]:
                self.w_status_code.setText(self.print_status(self.api_data["response"]['status']))

        l_status = QHBoxLayout()
        l_status.addWidget(self.w_url)
        l_status.addWidget(self.w_status_code, alignment=Qt.AlignRight)

        if "response" in self.api_data:
            if 'header' in self.api_data["response"]:
                self.w_console.setDocument(color_json(self.api_data["response"]['header']))

        w_gr_vbox_console = QVBoxLayout()
        w_gr_vbox_console.addLayout(l_status)
        w_gr_vbox_console.addWidget(self.w_console)

        w_gr_console = QGroupBox()
        w_gr_console.setTitle("Console")
        w_gr_console.setLayout(w_gr_vbox_console)

        w_format = QPushButton()
        w_format.setText("Format")
        w_format.setIcon(QIcon(get_icon_link('format_indent_increase.svg')))
        w_format.setToolTip("Format result (Ctrl+B)")
        w_format.pressed.connect(self.format_result)

        self.w_format_field.setSizePolicy(QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed))
        if "config" in self.api_data:
            if 'format' in self.api_data['config']:
                self.w_format_field.setText(str(self.api_data['config']['format']))
        # self.w_format_field.pressed.connect(self.open_format_manager)
        self.w_format_field.installEventFilter(self)

        self.w_format_label.setText("String object: ")

        l_hbox = QHBoxLayout()
        l_hbox.addWidget(self.w_format_label, alignment=Qt.AlignLeft)
        l_hbox.addWidget(self.w_format_field)
        l_hbox.addWidget(w_format, alignment=Qt.AlignRight)

        w_gr_vbox_result = QVBoxLayout()
        w_gr_vbox_result.addLayout(l_hbox)

        if "response" in self.api_data:
            if 'content' in self.api_data["response"]:
                self.w_result.setDocument(color_json(self.api_data["response"]['content']))

        w_gr_vbox_result.addWidget(self.w_result)

        w_gr_result = QGroupBox()
        w_gr_result.setTitle("Result")
        w_gr_result.setLayout(w_gr_vbox_result)

        self.addWidget(w_gr_console)
        self.addWidget(w_gr_result)
        self.setStretchFactor(0, 1)
        self.setStretchFactor(1, 2)

    def console(self, src="", arg=None):
        if arg is not None:
            print(src, arg, sep=": ")
            s = src + ": " + arg + "\n"
            new = color_json(self.w_console.toPlainText() + "\n" + s)
            self.w_console.setDocument(new)

    def result(self, rs: dict, is_save: bool):
        self.api_data = rs
        result = color_json(rs["response"]['content'])
        self.w_result.setDocument(result)

        status = self.print_status(rs["response"]['status'])
        self.w_status_code.setText(status)

        self.w_url.setText(rs["response"]['url'])

        cons = color_json(dict(rs["response"]['header']))
        self.w_console.setDocument(cons)

        if is_save:
            if rs["response"]['status'] >= 400:
                self.show_ask_save_dialog(self.print_status(rs["response"]['status']), rs)
            else:
                self.save(rs)

    def show_ask_save_dialog(self, res: str, rs):
        msg = QMessageBox()
        msg.setStyleSheet(open('stylesheet/default.qss').read())
        msg.setIcon(QMessageBox.Warning)

        msg.setText("API call fail!!!")
        msg.setInformativeText(res)
        msg.setWindowTitle("API call fail. Do you want to save this response?")
        msg.addButton('Save All', QMessageBox.YesRole)
        msg.addButton('Save Config Only', QMessageBox.YesRole)
        msg.addButton('Cancel', QMessageBox.NoRole)

        chosen = msg.exec_()
        if chosen == 0:
            self.save(rs)
        elif chosen == 1:
            rs["response"] = []
            self.save(rs, False)

    def save(self, rs: dict, is_replace=True):
        path = rs['save']['name']
        if not path.lower().endswith(".json"):
            path = path + ".json"
        folder_name = rs['save']['folder']['name']
        if folder_name == "root":
            path = rs['save']['folder']['dir'] + "/" + path
        else:
            path = rs['save']['folder']['dir'] + "/" + folder_name + "/" + path

        if os.path.isfile(path):
            f = open(path, "r", encoding="utf-8")
            js = json.loads(f.read())
            f.close()
            if not is_replace:
                if 'response' in js:
                    rs['response'] = js['response']

            if 'config' in js:
                api = js['config']['api']
                if api != rs['config']['api']:
                    self.show_dialog(path, rs, rs['config']['api'], js['config']['api'])
                    return -1

        self.save_data(path, rs)

    def show_dialog(self, path, rs, your_api, their_api):
        msg = QMessageBox()
        msg.setStyleSheet(open('stylesheet/default.qss').read())
        msg.setIcon(QMessageBox.Information)

        msg.setText("The file already exists.")
        msg.setInformativeText(
            "The file already exists and the difference is found in the api section. Are you sure to continue saving?")
        msg.setWindowTitle("Save Warning!!!")
        detail = "Your API: " + your_api + '\n' + "Their API: " + their_api
        msg.setDetailedText(detail)
        msg.addButton('Save', QMessageBox.YesRole)
        msg.addButton('Auto Fix', QMessageBox.YesRole)
        msg.addButton('Cancel', QMessageBox.NoRole)

        retval = msg.exec_()
        if retval == 0:
            self.save_data(path, rs)
        elif retval == 1:
            path = path.replace(".json", "")
            path = path + "_" + your_api + ".json"
            self.save_data(path, rs)

    def save_data(self, path: str, rs):
        formatted_json = json.dumps(rs, sort_keys=True, indent=4)
        fout = open(path, "w", encoding="utf-8")
        fout.write(formatted_json)
        fout.close()
        print("save output to: " + path)
        self.console("save output to", path)
        self.save_done.emit()

    def print_status(self, r: int):
        return httprequest.print_response(r) + ": " + str(r)

    def format_result(self):
        result = self.api_data["response"]['content']
        if not self.w_format_label.isChecked():
            self.w_result.setDocument(color_json(result))
        else:
            if 'format' not in self.api_data['config']:
                self.w_result.setDocument(color_json(result))
            else:
                if not self.api_data['config']['format']:
                    self.w_result.setDocument(color_json(result))
                else:
                    pass

    def open_format_manager(self):
        data = []
        if "config" in self.api_data:
            if 'format' in self.api_data['config']:
                data = self.api_data['config']['format']
        if self.format_manager is None:
            self.format_manager = ResultFormatManager(data)
            self.format_manager.setModal(False)
            self.format_manager.setGeometry(self.x() + 300, self.y() + 200, 600, 400)
            self.format_manager.apply_done.connect(self.format_manager_done)
            self.format_manager.show()
        else:
            if not self.format_manager.isVisible():
                if "config" in self.api_data:
                    if 'format' in self.api_data['config']:
                        data = self.api_data['config']['format']
                        self.format_manager.set_data(data)
                self.format_manager.setVisible(True)

    def format_manager_done(self):
        data = self.format_manager.data()
        if "config" not in self.api_data:
            self.api_data['config'] = {}
        self.api_data['config']['format'] = data
        self.w_format_field.setText(str(data))

    def eventFilter(self, widget, event):
        if widget == self.w_format_field and event.type() == QEvent.FocusIn:
            self.open_format_manager()
            return True
        return False
