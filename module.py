import json
import os
from PyQt5.QtCore import Qt, QEvent
from PyQt5.QtGui import QTextDocument, QFontMetrics
from PyQt5.QtWidgets import QSizePolicy, QGridLayout, QLabel, QTextEdit
from pygments import *
from pygments import lexers, formatters


def get_icon_link(icon_name):
    return "icons/dark/" + icon_name


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


def get_user_folder():
    return os.path.expanduser('~')


def get_app_folder():
    data = get_user_folder() + "\\HttpRequest"

    if not os.path.exists(data):
        os.makedirs(data)

    return data


def get_data_folder():
    data = get_app_folder() + "\\data"

    if not os.path.exists(data):
        os.makedirs(data)

    return data


def get_config_folder():
    data = get_app_folder() + "\\config"

    if not os.path.exists(data):
        os.makedirs(data)

    return data


def get_link_file():
    data = get_config_folder() + "\\api_link.json"
    return data


def color_json(obj):
    doc = QTextDocument()
    doc.setDefaultStyleSheet(open('stylesheet/json_style.css').read())
    if isinstance(obj, str):
        doc.setHtml(string_to_html(obj))
    else:
        doc.setHtml(json_to_html(obj))
    return doc


def json_to_html(obj):
    formatted_json = json.dumps(obj, sort_keys=True, indent=4, ensure_ascii=False)
    colorful_json = highlight(formatted_json, lexers.JsonLexer(), formatters.HtmlFormatter())
    return colorful_json


def string_to_html(obj):
    formatted_json = obj
    try:
        js = json.loads(obj)
        formatted_json = json.dumps(js, sort_keys=True, indent=4, ensure_ascii=False)
    except Exception as ex:
        print(ex)
    finally:
        colorful_json = highlight(formatted_json, lexers.JsonLexer(), formatters.HtmlFormatter())
        return colorful_json
