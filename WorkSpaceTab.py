from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QSplitter

from APIConfigure import APIConfigure
from APIResult import APIResult


class WorkSpaceTab(QSplitter):
    def __init__(self):
        super().__init__()

        self.setOrientation(Qt.Horizontal)

        configure = APIConfigure()
        self.addWidget(configure)

        result = APIResult()
        self.addWidget(result)

        self.setStretchFactor(0, 1)
        self.setStretchFactor(1, 2)
        self.setContentsMargins(10, 10, 10, 10)
