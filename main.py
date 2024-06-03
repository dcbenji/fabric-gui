#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import logging
from PyQt5.QtWidgets import QApplication
from config import load_config, save_config
from fabric_gui import FabricExtractorGUI

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