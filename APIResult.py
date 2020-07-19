from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QWidget, QLabel, QHBoxLayout, QTextEdit, QVBoxLayout, QGroupBox, QPushButton, QLineEdit, \
    QSplitter, QCheckBox, QSizePolicy
from PyQt5 import QtCore
from PyQt5 import QtGui

from module import label_widget


class APIResult(QSplitter):
    def __init__(self):
        super().__init__()
        self.setOrientation(Qt.Vertical)
        self.component()

    def component(self):
        w_url = QLabel()
        w_url.setText("Url: ")
        w_url.setTextInteractionFlags(Qt.TextSelectableByMouse)
        w_url.setCursor(QtGui.QCursor(QtCore.Qt.IBeamCursor))

        w_status_code = QLabel()
        w_status_code.setText("0 - No API call")

        l_status = QHBoxLayout()
        l_status.addWidget(w_url, alignment=Qt.AlignLeft)
        l_status.addWidget(w_status_code, alignment=Qt.AlignRight)

        w_console = QTextEdit()

        w_gr_vbox_console = QVBoxLayout()
        w_gr_vbox_console.addLayout(l_status)
        w_gr_vbox_console.addWidget(w_console)

        w_gr_console = QGroupBox()
        w_gr_console.setTitle("Console")
        w_gr_console.setLayout(w_gr_vbox_console)

        w_format = QPushButton()
        w_format.setText("Format")
        w_format.setIcon(QIcon('icons/format_indent_increase.svg'))
        w_format.setToolTip("Format result (Ctrl+B)")

        w_format_field = QPushButton()
        w_format_field.setSizePolicy(QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed))

        w_format_label = QCheckBox()
        w_format_label.setText("String object: ")

        l_hbox = QHBoxLayout()
        l_hbox.addWidget(w_format_label, alignment=Qt.AlignLeft)
        l_hbox.addWidget(w_format_field)
        l_hbox.addWidget(w_format, alignment=Qt.AlignRight)

        w_gr_vbox_result = QVBoxLayout()
        w_gr_vbox_result.addLayout(l_hbox)

        w_result = QTextEdit()
        w_gr_vbox_result.addWidget(w_result)

        w_gr_result = QGroupBox()
        w_gr_result.setTitle("Result")
        w_gr_result.setLayout(w_gr_vbox_result)

        self.addWidget(w_gr_console)
        self.addWidget(w_gr_result)
        self.setStretchFactor(0, 1)
        self.setStretchFactor(1, 2)
