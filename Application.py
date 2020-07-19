from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import *
from PyQt5 import QtCore
from PyQt5 import QtGui
from FileTreeView import FileTreeView
from WorkSpaceTab import WorkSpaceTab


class Application(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Http Request")
        self.menu()

        self.l_tab_widget = QTabWidget()
        self.l_tab_widget.setTabsClosable(True)
        self.l_tab_widget.addTab(WorkSpaceTab(), "New request")

        l_file_tree_view = FileTreeView()

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
        new_action = QAction(QIcon('icons/note_add.svg'), '&New...', self)
        new_action.setShortcut('Ctrl+N')
        new_action.setStatusTip('New document')
        new_action.triggered.connect(self.new_call)

        # Create new action
        open_action = QAction(QIcon('icons/description.svg'), '&Open', self)
        open_action.setShortcut('Ctrl+O')
        open_action.setStatusTip('Open document')
        # openAction.triggered.connect(self.openCall)

        # Create new action
        save_action = QAction(QIcon('icons/description.svg'), '&Save', self)
        save_action.setShortcut('Ctrl+S')
        save_action.setStatusTip('Save document')
        # openAction.triggered.connect(self.openCall)

        # Create exit action
        exit_action = QAction(QIcon('icons/exit_to_app.svg'), '&Exit', self)
        exit_action.setShortcut('Ctrl+Q')
        exit_action.setStatusTip('Exit application')
        # exitAction.triggered.connect(self.exitCall)

        # Create preference action
        pref_action = QAction(QIcon('icons/settings.svg'), '&Preferences', self)
        pref_action.setShortcut('Ctrl+P')
        pref_action.setStatusTip('Open preferences')
        # exitAction.triggered.connect(self.exitCall)

        file_menu = main_menu.addMenu('&File')
        file_menu.addAction(new_action)
        file_menu.addAction(open_action)
        file_menu.addSeparator()
        file_menu.addAction(save_action)
        file_menu.addSeparator()
        file_menu.addAction(pref_action)
        file_menu.addSeparator()
        file_menu.addAction(exit_action)

        # Create preference action
        run_action = QAction(QIcon('icons/play_arrow.svg'), '&Run', self)
        run_action.setShortcut('Ctrl+R')
        run_action.setStatusTip('Run API call')
        # exitAction.triggered.connect(self.exitCall)

        # Create preference action
        run_save_action = QAction(QIcon('icons/play_circle_outline.svg'), '&Run && Save', self)
        run_save_action.setShortcut('Ctrl+Shift+R')
        run_save_action.setStatusTip('Run and Save API call')
        # exitAction.triggered.connect(self.exitCall)

        # Create preference action
        clear_action = QAction(QIcon('icons/refresh.svg'), '&Reset', self)
        clear_action.setShortcut('Ctrl+Shift+C')
        clear_action.setStatusTip('Reset param')
        # exitAction.triggered.connect(self.exitCall)

        # Create preference action
        format_action = QAction(QIcon('icons/format_indent_increase.svg'), '&Format', self)
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
        close_tab_action = QAction(QIcon('icons/close.svg'), '&Close Tab', self)
        close_tab_action.setShortcut('Ctrl+W')
        close_tab_action.setStatusTip('Close Tab')
        # exitAction.triggered.connect(self.exitCall)

        # Create preference action
        close_all_action = QAction(QIcon('icons/clear_all.svg'), '&Close All Tab', self)
        close_all_action.setShortcut('Ctrl+Shift+W')
        close_all_action.setStatusTip('Close All Tab')
        # exitAction.triggered.connect(self.exitCall)

        # Create preference action
        close_others_action = QAction(QIcon('icons/tab.svg'), '&Close Others Tab', self)
        close_others_action.setShortcut('Ctrl+Alt+W')
        close_others_action.setStatusTip('Close Others Tab')
        # exitAction.triggered.connect(self.exitCall)

        workspace_menu = main_menu.addMenu('&Workspace')
        workspace_menu.addAction(close_tab_action)
        workspace_menu.addAction(close_all_action)
        workspace_menu.addAction(close_others_action)

        # Create preference action
        shortcut_action = QAction(QIcon('icons/keyboard.svg'), '&Shortcut', self)
        shortcut_action.setShortcut('')
        shortcut_action.setStatusTip('Application shortcut')
        # exitAction.triggered.connect(self.exitCall)

        # Create preference action
        about_action = QAction(QIcon('icons/live_help.svg'), '&About', self)
        about_action.setShortcut('')
        about_action.setStatusTip('Application information')
        # exitAction.triggered.connect(self.exitCall)

        help_menu = main_menu.addMenu('&Help')
        help_menu.addAction(about_action)
        help_menu.addAction(shortcut_action)

        self.setMenuBar(main_menu)

    def icon(self):
        # set app icon
        app_icon = QtGui.QIcon()
        app_icon.addFile('icons/description.svg', QtCore.QSize(24, 24))
        app_icon.addFile('icons/exit_to_app.png', QtCore.QSize(24, 24))
        app_icon.addFile('icons/note_add.png', QtCore.QSize(24, 24))
        app_icon.addFile('icons/settings.png', QtCore.QSize(24, 24))
        self.setWindowIcon(app_icon)

    def new_call(self):
        self.l_tab_widget.addTab(WorkSpaceTab(), "New request")
