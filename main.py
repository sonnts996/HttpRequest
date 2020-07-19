#!/usr/bin/python

import sys
from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow
from Application import Application


def main():
    for arg in sys.argv[1:]:
        print(arg)

    app = QApplication(sys.argv)
    window = Application()
    window.show()  # IMPORTANT!!!!! Windows are hidden by default.
    app.exec_()


if __name__ == "__main__":
    main()
