from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import *

from APILinkManager import APILinkManager
from FileTreeView import FileTreeView
from WorkSpaceTab import WorkSpaceTab
from module import get_icon_link
from PyQt5.QtCore import pyqtSignal


class Application(QMainWindow):
    api_data_change = pyqtSignal()

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Http Request")
        self.menu()

        self.l_tab_widget = QTabWidget()
        self.l_tab_widget.setTabsClosable(True)
        self.l_tab_widget.addTab(WorkSpaceTab(self), "New request")
        self.l_tab_widget.tabCloseRequested.connect(lambda index: self.l_tab_widget.removeTab(index))

        l_file_tree_view = FileTreeView()
        l_file_tree_view.on_menu_select.connect(self.on_tree_view_action)

        q_splitter = QSplitter()
        q_splitter.addWidget(l_file_tree_view)
        q_splitter.addWidget(self.l_tab_widget)

        q_splitter.setStretchFactor(0, 1)
        q_splitter.setStretchFactor(1, 2)
        q_splitter.setContentsMargins(10, 10, 10, 10)

        self.setCentralWidget(q_splitter)

    def menu(self):
        main_menu = QMenuBar()

        # Create new action
        new_action = QAction(QIcon(get_icon_link('note_add.svg')), '&New...', self)
        new_action.setShortcut('Ctrl+N')
        new_action.setStatusTip('New document')
        new_action.triggered.connect(self.new_call)

        # Create new action
        open_action = QAction(QIcon(get_icon_link('description.svg')), '&Open', self)
        open_action.setShortcut('Ctrl+O')
        open_action.setStatusTip('Open document')
        # openAction.triggered.connect(self.openCall)

        # Create new action
        save_action = QAction(QIcon(get_icon_link('description.svg')), '&Save', self)
        save_action.setShortcut('Ctrl+S')
        save_action.setStatusTip('Save document')
        # openAction.triggered.connect(self.openCall)

        # Create exit action
        exit_action = QAction(QIcon(get_icon_link('exit_to_app.svg')), '&Exit', self)
        exit_action.setShortcut('Ctrl+Q')
        exit_action.setStatusTip('Exit application')
        # exitAction.triggered.connect(self.exitCall)

        file_menu = main_menu.addMenu('&File')
        file_menu.addAction(new_action)
        file_menu.addAction(open_action)
        file_menu.addSeparator()
        file_menu.addAction(save_action)
        file_menu.addSeparator()
        file_menu.addAction(exit_action)

        # Create preference action
        api_link_action = QAction(QIcon(get_icon_link('link.svg')), '&API link manager', self)
        api_link_action.setShortcut('Ctrl+L')
        api_link_action.setStatusTip('API link manager')
        api_link_action.triggered.connect(self.api_link_manager)

        pref_menu = main_menu.addMenu('&Preferences')
        pref_menu.addAction(api_link_action)

        # Create preference action
        run_action = QAction(QIcon(get_icon_link('play_arrow.svg')), '&Run', self)
        run_action.setShortcut('Ctrl+R')
        run_action.setStatusTip('Run API call')
        # exitAction.triggered.connect(self.exitCall)

        # Create preference action
        run_save_action = QAction(QIcon(get_icon_link('play_circle_outline.svg')), '&Run && Save', self)
        run_save_action.setShortcut('Ctrl+Shift+R')
        run_save_action.setStatusTip('Run and Save API call')
        # exitAction.triggered.connect(self.exitCall)

        # Create preference action
        clear_action = QAction(QIcon(get_icon_link('refresh.svg')), '&Reset', self)
        clear_action.setShortcut('Ctrl+Shift+C')
        clear_action.setStatusTip('Reset param')
        # exitAction.triggered.connect(self.exitCall)

        # Create preference action
        format_action = QAction(QIcon(get_icon_link('format_indent_increase.svg')), '&Format', self)
        format_action.setShortcut('Ctrl+B')
        format_action.setStatusTip('Format result')
        # exitAction.triggered.connect(self.exitCall)

        run_menu = main_menu.addMenu('&Run')
        run_menu.addAction(run_action)
        run_menu.addAction(run_save_action)
        run_menu.addSeparator()
        run_menu.addAction(clear_action)
        run_menu.addAction(format_action)

        # Create preference action
        close_tab_action = QAction(QIcon(get_icon_link('close.svg')), '&Close Tab', self)
        close_tab_action.setShortcut('Ctrl+W')
        close_tab_action.setStatusTip('Close Tab')
        # exitAction.triggered.connect(self.exitCall)

        # Create preference action
        close_all_action = QAction(QIcon(get_icon_link('clear_all.svg')), '&Close All Tab', self)
        close_all_action.setShortcut('Ctrl+Shift+W')
        close_all_action.setStatusTip('Close All Tab')
        # exitAction.triggered.connect(self.exitCall)

        # Create preference action
        close_others_action = QAction(QIcon(get_icon_link('tab.svg')), '&Close Others Tab', self)
        close_others_action.setShortcut('Ctrl+Alt+W')
        close_others_action.setStatusTip('Close Others Tab')
        # exitAction.triggered.connect(self.exitCall)

        workspace_menu = main_menu.addMenu('&Workspace')
        workspace_menu.addAction(close_tab_action)
        workspace_menu.addAction(close_all_action)
        workspace_menu.addAction(close_others_action)

        # Create preference action
        shortcut_action = QAction(QIcon(get_icon_link('keyboard.svg')), '&Shortcut', self)
        shortcut_action.setShortcut('')
        shortcut_action.setStatusTip('Application shortcut')
        # exitAction.triggered.connect(self.exitCall)

        # Create preference action
        about_action = QAction(QIcon(get_icon_link('live_help.svg')), '&About', self)
        about_action.setShortcut('')
        about_action.setStatusTip('Application information')
        # exitAction.triggered.connect(self.exitCall)

        help_menu = main_menu.addMenu('&Help')
        help_menu.addAction(about_action)
        help_menu.addAction(shortcut_action)

        self.setMenuBar(main_menu)

    def new_call(self):
        self.l_tab_widget.addTab(WorkSpaceTab(self), "New request")
        self.l_tab_widget.setCurrentIndex(self.l_tab_widget.count() - 1)

    def api_link_manager(self):
        api_link = APILinkManager()
        api_link.setGeometry(self.x() + self.width() / 2 - 300, self.y() + self.height() / 2 - 200, 600, 400)
        if api_link.exec():
            self.api_data_change.emit()

    def change_tab_name(self, name: str):
        self.l_tab_widget.setTabText(self.l_tab_widget.currentIndex(), name)

    def on_tree_view_action(self, action: str, data: dict):
        if action == "open":
            is_opened = False
            for i in range(self.l_tab_widget.count()):
                if self.l_tab_widget.tabText(i) == data['name']:
                    self.l_tab_widget.setCurrentIndex(i)
                    is_opened = True
                    return is_opened
            if not is_opened:
                self.l_tab_widget.addTab(WorkSpaceTab(self, data), data['name'])
                self.l_tab_widget.setCurrentIndex(self.l_tab_widget.count() - 1)
                return is_opened
