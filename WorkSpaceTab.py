from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QSplitter

import Application
from APIConfigure import APIConfigure
from APIResult import APIResult


class WorkSpaceTab(QSplitter):

    def __init__(self, parent: Application, data=None):
        super().__init__()

        self.p = parent
        self.setOrientation(Qt.Horizontal)

        self.result = APIResult(data)

        configure = APIConfigure(parent, data)
        configure.console.connect(self.console)
        configure.result.connect(self.result_api)

        self.addWidget(configure)
        self.addWidget(self.result)

        self.setStretchFactor(0, 1)
        self.setStretchFactor(1, 2)
        self.setContentsMargins(10, 10, 10, 10)

    def console(self, src="tab", arg=None):
        self.result.console(src, arg)

    def result_api(self, rs: dict, is_save: bool):
        self.result.result(rs, is_save)
        if is_save:
            self.p.change_tab_name(rs['save']['name'])
        else:
            self.p.change_tab_name(rs['config']['api'])
