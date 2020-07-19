from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QWidget, QTabWidget, QTextEdit, QHBoxLayout, QPushButton, QSplitter, QLineEdit, QComboBox, \
    QSizePolicy, QVBoxLayout, QGroupBox

from module import label_widget


class APIConfigure(QSplitter):
    def __init__(self):
        super().__init__()
        self.setOrientation(Qt.Vertical)
        self.component()

    def component(self):
        w_widget_tab = QTabWidget()
        w_json_edit = QTextEdit()
        l_box = QHBoxLayout()
        w_group = QWidget()
        w_group.setLayout(l_box)

        w_widget_tab.addTab(w_group, "UI")
        w_widget_tab.addTab(w_json_edit, "JSON")

        w_run = QPushButton()
        w_run.setIcon(QIcon('icons/play_arrow.svg'))
        w_run.setText("Run")
        w_run.setToolTip("Run API call (Ctrl+R)")

        w_run_save = QPushButton()
        w_run_save.setIcon(QIcon('icons/play_circle_outline.svg'))
        w_run_save.setText("Run && Save")
        w_run_save.setToolTip("Run and Save API call (Ctrl++Shift+R)")

        w_clear = QPushButton()
        w_clear.setText("Reset")
        w_clear.setIcon(QIcon('icons/refresh.svg'))
        w_clear.setToolTip("Reset param (Ctrl+Shift+C)")

        l_action = QHBoxLayout()
        l_action.addWidget(w_run, alignment=Qt.AlignLeft)
        l_action.addWidget(w_run_save, alignment=Qt.AlignLeft)
        l_action.addWidget(w_clear, alignment=Qt.AlignRight)

        w_group2 = QWidget()
        w_group2.setLayout(l_action)
        w_group2.setMaximumHeight(50)

        self.addWidget(self.header())
        self.addWidget(w_widget_tab)
        self.addWidget(w_group2)
        self.setStretchFactor(0, 1)
        self.setStretchFactor(1, 2)
        self.setStretchFactor(2, 1)
        self.setStretchFactor(3, 1)

    def header(self):
        w_api = QLineEdit()

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

        l_box = QVBoxLayout()
        l_box.addWidget(w_api, alignment=Qt.AlignTop)
        l_box.addLayout(label_widget("Protocol: ", w_api_type, 120))
        l_box.addLayout(label_widget("API Link: ", w_api_link, 120))
        l_box.addLayout(label_widget("Parameter type: ", w_api_param, 120))
        l_box.addLayout(label_widget("Description: ", w_description, 0, 1))

        gr_header = QGroupBox()
        gr_header.setLayout(l_box)
        gr_header.setTitle("API")
        gr_header.setMaximumHeight(300)
        return gr_header
