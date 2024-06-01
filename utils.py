import os
from PyQt5.QtWidgets import QApplication

def apply_stylesheet(self):
    stylesheet_path = os.path.join(os.path.dirname(__file__), "fabric_style.qss")
    with open(stylesheet_path, "r") as file:
        stylesheet = file.read()
        self.setStyleSheet(stylesheet)

def clear_output(self):
    self.output_area.clear()
    if self.wow_widget:
        self.wow_widget.hide()

def clear_all(self):
    self.input_area.clear()
    self.output_area.clear()
    if self.wow_widget:
        self.wow_widget.hide()

def copy_output(self):
    text = self.output_area.toPlainText()
    QApplication.clipboard().setText(text)