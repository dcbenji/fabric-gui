#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys
import json
import os
import re
import requests
import markdown
import logging
import subprocess
import markdown_utils
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QLabel, QLineEdit, QTextEdit, QVBoxLayout, QHBoxLayout, QPushButton, QRadioButton, QButtonGroup, QFileDialog, QMessageBox, QGroupBox, QGridLayout, QComboBox, QProgressBar, QTreeWidget, QTreeWidgetItem, QSplitter
from PyQt5.QtGui import QFont, QIcon
from PyQt5.QtCore import Qt, QThread, pyqtSignal
from config import load_config, save_config, get_api_key, set_api_key, get_api_endpoint, set_api_endpoint, get_default_model, set_default_model, get_temperature, set_temperature, get_max_tokens, set_max_tokens, get_theme, set_theme
from gui_utils import FabricExtractorGUI  # Add this import statement

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

if __name__ == '__main__':
    config = load_config()
    app = QApplication(sys.argv)
    app.setStyleSheet(open("styles.py", "r").read())
    main_window = FabricExtractorGUI(config)
    main_window.show()
    result = app.exec_()
    save_config(config)
    sys.exit(result)