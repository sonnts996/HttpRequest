from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QSizePolicy, QGridLayout, QLabel


def label_widget(text, widget, label_size=0, type_label=0):
    box = QGridLayout()
    label = QLabel()
    label.setText(text)
    if label_size != 0:
        label.setMinimumWidth(label_size)
        label.setMaximumWidth(label_size)

    label.setSizePolicy(QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed))
    widget.setSizePolicy(QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed))

    if type_label == 0:
        box.addWidget(label, 0, 0, alignment=Qt.AlignLeft)
        box.addWidget(widget, 0, 1)
    else:
        box.addWidget(label, 0, 0, alignment=Qt.AlignLeft)
        box.addWidget(widget, 1, 0)
    return box
