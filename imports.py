import sys
import os
import subprocess
import re
import logging
import json
from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QTextEdit,
    QPushButton,
    QComboBox,
    QFileDialog,
    QWidget,
    QProgressBar,
    QGridLayout,
    QGroupBox,
    QMessageBox,
    QSplitter,
    QRadioButton,
    QTreeWidget,
    QTreeWidgetItem,
)
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt, QThread, pyqtSignal