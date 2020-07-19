from PyQt5 import QtCore
from PyQt5.QtCore import *
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import *
from PyQt5 import QtGui


def label_widget(label, widget, label_size=0, type_label=0):
    l_hbox = QGridLayout()
    l = QLabel()
    l.setText(label)
    if label_size != 0:
        l.setMinimumWidth(label_size)
        l.setMaximumWidth(label_size)

    l.setSizePolicy(QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed))
    widget.setSizePolicy(QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed))

    if type_label == 0:
        l_hbox.addWidget(l, 0, 0, alignment=Qt.AlignLeft)
        l_hbox.addWidget(widget, 0, 1)
    else:
        l_hbox.addWidget(l, 0, 0, alignment=Qt.AlignLeft)
        l_hbox.addWidget(widget, 1, 0)
    return l_hbox


class Application(QMainWindow):
    def __init__(self, *args, **kwargs):
        super().__init__()

        self.setWindowTitle("Http Request")
        self.menu()

        q_splitter = QSplitter(Qt.Horizontal)
        q_splitter.addWidget(self.left_pane())
        q_splitter.addWidget(self.right_pane())
        q_splitter.setStretchFactor(0, 1)
        q_splitter.setStretchFactor(1, 2)
        q_splitter.setContentsMargins(10, 10, 10, 10)
        self.setCentralWidget(q_splitter)

    def left_pane(self):
        w_widget_tab = QTabWidget()
        w_json_edit = QTextEdit()
        l_hbox = QHBoxLayout()
        w_group = QWidget()
        w_group.setLayout(l_hbox)

        w_widget_tab.addTab(w_group, "UI")
        w_widget_tab.addTab(w_json_edit, "JSON")

        w_run = QPushButton()
        w_run.setText("Run")
        w_clear = QPushButton()
        w_clear.setText("Reset")

        l_action = QHBoxLayout()
        l_action.addWidget(w_run, alignment=Qt.AlignLeft)
        l_action.addWidget(w_clear, alignment=Qt.AlignRight)

        w_group2 = QWidget()
        w_group2.setLayout(l_action)
        w_group2.setMaximumHeight(50)

        q_splitter = QSplitter(Qt.Vertical)
        q_splitter.addWidget(self.header())
        q_splitter.addWidget(w_widget_tab)
        q_splitter.addWidget(w_group2)
        q_splitter.setStretchFactor(0, 1)
        q_splitter.setStretchFactor(1, 2)
        q_splitter.setStretchFactor(2, 1)
        q_splitter.setStretchFactor(3, 1)
        return q_splitter

    def header(self):
        self.w_api = QLineEdit()

        w_api_type = QComboBox()
        w_api_type.addItem("POST")
        w_api_type.addItem("GET")

        w_api_link = QComboBox()
        w_api_link.addItem("PHARMACY_RELEASE")
        w_api_link.addItem("PHARMACY_BETA")

        w_api_param = QComboBox()
        w_api_param.addItem("Param")
        w_api_param.addItem("JSON")

        w_description = QTextEdit()
        w_description.setMinimumHeight(50)
        w_description.setSizePolicy(QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed))

        l_vbox = QVBoxLayout()
        l_vbox.addWidget(self.w_api, alignment=Qt.AlignTop)
        l_vbox.addLayout(label_widget("Protocol: ", w_api_type, 120))
        l_vbox.addLayout(label_widget("API Link: ", w_api_link, 120))
        l_vbox.addLayout(label_widget("Parameter type: ", w_api_param, 120))
        l_vbox.addLayout(label_widget("Description: ", w_description, 0, 1))

        gr_header = QGroupBox()
        gr_header.setLayout(l_vbox)
        gr_header.setTitle("API")
        gr_header.setMaximumHeight(300)
        return gr_header

    def right_pane(self):
        w_url = QLabel()
        w_url.setText("Url: ")
        w_url.setTextInteractionFlags(Qt.TextSelectableByMouse)
        w_url.setCursor(QtGui.QCursor(QtCore.Qt.IBeamCursor))

        w_status_code = QLabel()
        w_status_code.setText("0 - No API call")

        l_status = QHBoxLayout()
        l_status.addWidget(w_url, alignment=Qt.AlignLeft)
        l_status.addWidget(w_status_code, alignment=Qt.AlignRight)

        self.w_console = QTextEdit()

        w_gr_vbox_console = QVBoxLayout()
        w_gr_vbox_console.addLayout(l_status)
        w_gr_vbox_console.addWidget(self.w_console)

        w_gr_console = QGroupBox()
        w_gr_console.setTitle("Console")
        w_gr_console.setLayout(w_gr_vbox_console)

        w_format = QPushButton()
        w_format.setText("Format")

        w_format_field = QLineEdit()

        l_hbox = QHBoxLayout()
        l_hbox.addLayout(label_widget("String object: ", w_format_field))
        l_hbox.addWidget(w_format, alignment=Qt.AlignRight)

        w_gr_vbox_result = QVBoxLayout()
        w_gr_vbox_result.addLayout(l_hbox)

        self.w_result = QTextEdit()
        w_gr_vbox_result.addWidget(self.w_result)

        w_gr_result = QGroupBox()
        w_gr_result.setTitle("Result")
        w_gr_result.setLayout(w_gr_vbox_result)

        l_right = QSplitter(Qt.Vertical)
        l_right.addWidget(w_gr_console)
        l_right.addWidget(w_gr_result)
        l_right.setStretchFactor(0, 1)
        l_right.setStretchFactor(1, 2)

        return l_right

    def menu(self):
        mainMenu = QMenuBar()

        # Create new action
        newAction = QAction(QIcon('new.png'), '&New', self)
        newAction.setShortcut('Ctrl+N')
        newAction.setStatusTip('New document')
        # newAction.triggered.connect(self.newCall)

        # Create new action
        openAction = QAction(QIcon('open.png'), '&Open', self)
        openAction.setShortcut('Ctrl+O')
        openAction.setStatusTip('Open document')
        # openAction.triggered.connect(self.openCall)

        # Create exit action
        exitAction = QAction(QIcon('exit.png'), '&Exit', self)
        exitAction.setShortcut('Ctrl+Q')
        exitAction.setStatusTip('Exit application')
        # exitAction.triggered.connect(self.exitCall)

        fileMenu = mainMenu.addMenu('&File')
        fileMenu.addAction(newAction)
        fileMenu.addAction(openAction)
        fileMenu.addAction(exitAction)

        self.setMenuBar(mainMenu)
