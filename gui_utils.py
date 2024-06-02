import os
import re
import subprocess
import markdown_utils
import logging
logger = logging.getLogger(__name__)
from PyQt5.QtWidgets import QMainWindow, QWidget, QLabel, QLineEdit, QTextEdit, QVBoxLayout, QHBoxLayout, QPushButton, QRadioButton, QButtonGroup, QFileDialog, QMessageBox, QGroupBox, QGridLayout, QComboBox, QProgressBar, QTreeWidget, QTreeWidgetItem, QSplitter
from PyQt5.QtGui import QFont, QIcon
from PyQt5.QtCore import Qt, QThread, pyqtSignal
from api_utils import FabricWorkerThread

class FabricExtractorGUI(QMainWindow):
    def __init__(self, app):
        super().__init__()
        self.app = app
        self.initUI()
        self.worker_thread = None
        self.wow_widget = None

    def initUI(self):
        self.setWindowTitle("Fabric Extractor")
        self.setWindowIcon(QIcon("icons/fabric.png"))

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        main_layout = QHBoxLayout()
        main_layout.setSpacing(20)
        main_layout.setContentsMargins(20, 20, 20, 20)

        left_layout = self.create_left_layout()
        right_layout = self.create_right_layout()

        splitter = QSplitter(Qt.Horizontal)
        left_widget = QWidget()
        left_widget.setLayout(left_layout)
        right_widget = QWidget()
        right_widget.setLayout(right_layout)
        splitter.addWidget(left_widget)
        splitter.addWidget(right_widget)

        main_layout.addWidget(splitter)
        central_widget.setLayout(main_layout)

        self.apply_stylesheet()

        self.pattern_combo.currentIndexChanged.connect(self.update_pattern_info)
        self.pattern_combo.currentIndexChanged.connect(self.handle_wow_pattern)
        
    def create_left_layout(self):
        left_layout = QVBoxLayout()
        left_layout.setSpacing(20)

        input_group = self.create_input_group()
        settings_group = self.create_settings_group()
        button_layout = self.create_button_layout()
        output_group = self.create_output_group()

        left_layout.addWidget(input_group)
        left_layout.addWidget(settings_group)
        left_layout.addLayout(button_layout)
        left_layout.addWidget(output_group)
        left_layout.addWidget(self.progress_bar)

        return left_layout

    def create_right_layout(self):
        right_layout = QVBoxLayout()
        right_layout.setSpacing(10)

        info_group = self.create_info_group()

        right_layout.addWidget(info_group)

        return right_layout

    def create_input_group(self):
        input_group = QGroupBox("Input")
        input_layout = QVBoxLayout()
        input_layout.setSpacing(10)
        self.input_area = QTextEdit()
        self.input_area.setPlaceholderText("Enter your text, YouTube video URL, or select an audio file...")
        input_layout.addWidget(self.input_area)
        file_button = QPushButton(QIcon("icons/file.png"), "Select File")
        file_button.clicked.connect(self.select_file)
        input_layout.addWidget(file_button)
        input_group.setLayout(input_layout)
        return input_group

    def create_settings_group(self):
        settings_group = QGroupBox("Settings")
        settings_layout = QGridLayout()
        settings_layout.setSpacing(10)
        pattern_label = QLabel("Pattern:")
        self.pattern_combo = QComboBox()
        self.pattern_combo.addItems(self.get_available_patterns())
        settings_layout.addWidget(pattern_label, 0, 0)
        settings_layout.addWidget(self.pattern_combo, 0, 1)
        model_label = QLabel("Model:")
        self.model_combo = QComboBox()
        self.models = [
            "gemma:latest",
            "llama3:latest",
            "llama3:70b",
            "claude-3-opus-20240229",
            "claude-3-sonnet-20240229",
            "claude-3-haiku-20240307",
        ]
        self.model_combo.addItems(self.models)
        self.model_combo.setCurrentText("llama3:latest")
        settings_layout.addWidget(model_label, 1, 0)
        settings_layout.addWidget(self.model_combo, 1, 1)
        settings_group.setLayout(settings_layout)
        return settings_group

    def create_button_layout(self):
        button_layout = QHBoxLayout()
        button_layout.setSpacing(10)
        extract_button = QPushButton(QIcon("icons/extract.png"), "Extract")
        extract_button.clicked.connect(self.run_fabric_extraction)
        button_layout.addWidget(extract_button)
        clear_all_button = QPushButton(QIcon("icons/clear_all.png"), "Clear All")
        clear_all_button.clicked.connect(self.clear_all)
        button_layout.addWidget(clear_all_button)
        return button_layout

    def create_output_group(self):
        output_group = QGroupBox("Output")
        output_layout = QVBoxLayout()
        output_layout.setSpacing(10)
        self.output_area = QTextEdit()
        self.output_area.setReadOnly(True)
        output_layout.addWidget(self.output_area)
        output_button_layout = QHBoxLayout()
        output_button_layout.setSpacing(10)
        clear_output_button = QPushButton(QIcon("icons/clear_output.png"), "Clear Output")
        clear_output_button.clicked.connect(self.clear_output)
        output_button_layout.addWidget(clear_output_button)
        copy_button = QPushButton(QIcon("icons/copy.png"), "Copy")
        copy_button.clicked.connect(self.copy_output)
        output_button_layout.addWidget(copy_button)
        output_layout.addLayout(output_button_layout)
        output_group.setLayout(output_layout)

        self.progress_bar = QProgressBar()
        self.progress_bar.setMinimumSize(200, 20)
        self.progress_bar.setValue(0)
        self.progress_bar.setTextVisible(False)

        return output_group

    def create_info_group(self):
        info_group = QGroupBox("Pattern Information")
        info_layout = QVBoxLayout()
        self.info_area = QTextEdit()
        self.info_area.setReadOnly(True)
        info_layout.addWidget(self.info_area)

        self.readme_radio = QRadioButton("README.md")
        self.readme_radio.setChecked(True)
        self.readme_radio.toggled.connect(self.update_pattern_info)
        self.system_radio = QRadioButton("system.md")
        self.system_radio.toggled.connect(self.update_pattern_info)

        radio_layout = QHBoxLayout()
        radio_layout.addWidget(self.readme_radio)
        radio_layout.addWidget(self.system_radio)
        info_layout.addLayout(radio_layout)

        info_group.setLayout(info_layout)
        return info_group

    def select_file(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Select File",
            "",
            "Text Files (*.txt);;Audio Files (*.mp3 *.wav *.m4a);;All Files (*)",
        )
        if file_path:
            if file_path.lower().endswith((".txt", ".md")):
                with open(file_path, "r") as file:
                    content = file.read()
                self.input_area.setPlainText(content)
            elif file_path.lower().endswith((".mp3", ".wav", ".m4a")):
                self.input_area.setPlainText(file_path)
            else:
                QMessageBox.warning(self, "Invalid File", "Please select a valid text or audio file.")

    def get_available_patterns(self):
        patterns_dir = "/Users/ben/fabric/patterns"
        patterns = []
        if os.path.isdir(patterns_dir):
            for item in os.listdir(patterns_dir):
                item_path = os.path.join(patterns_dir, item)
                if os.path.isdir(item_path):
                    patterns.append(item)
        return patterns

    def run_fabric_extraction(self):
        if self.worker_thread and self.worker_thread.isRunning():
            return

        input_text = self.input_area.toPlainText().strip()

        if self.is_youtube_link(input_text):
            video_id = self.extract_video_id(input_text)
            if video_id:
                yt_command = ["yt", "--transcript", f"https://youtu.be/{video_id}"]
                yt_result = subprocess.run(
                    yt_command,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    text=True,
                )
                input_text = yt_result.stdout
            else:
                return
        elif input_text.lower().endswith((".mp3", ".wav", ".m4a")):
            ts_command = ["ts", input_text]
            ts_result = subprocess.run(
                ts_command,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
            )
            if ts_result.returncode == 0:
                input_text = ts_result.stdout
            else:
                QMessageBox.critical(self, "Error", f"An error occurred during audio transcription:\n\n{ts_result.stderr}")
                return

        pattern = self.pattern_combo.currentText()
        model = self.model_combo.currentText()

        self.worker_thread = FabricWorkerThread(input_text, pattern, model)
        self.worker_thread.finished.connect(self.handle_fabric_result)
        self.progress_bar.setVisible(True)
        self.progress_bar.setMaximum(0)
        self.progress_bar.setMinimum(0)
        self.progress_bar.setValue(-1)
        self.worker_thread.start()

    def is_youtube_link(self, link):
        youtube_regex = re.compile(r'(https?://)?(www\.)?(youtube|youtu|youtube-nocookie)\.(com|be)/(watch\?v=|embed/|v/|.+\?v=)?([^&=%\?]{11})')
        return youtube_regex.match(link)

    def extract_video_id(self, link):
        youtube_regex = re.compile(r'(https?://)?(www\.)?(youtube|youtu|youtube-nocookie)\.(com|be)/(watch\?v=|embed/|v/|.+\?v=)?([^&=%\?]{11})')
        match = youtube_regex.match(link)
        if match:
            return match.group(6)
        return None

    def handle_fabric_result(self, output, error, json_data):
        try:
            logger.debug("Handling fabric result")
            if error:
                logger.error(f"Fabric extraction error: {error}")
                QMessageBox.critical(self, "Error", f"An error occurred during fabric extraction:\n\n{error}")
            else:
                logger.debug("Setting output text")
                self.output_area.setPlainText(output)
                if json_data:
                    logger.debug("Displaying WOW data")
                    self.display_wow_data(json_data)
                else:
                    logger.debug("Hiding WOW widget")
                    self.hide_wow_widget()
        except Exception as e:
            logger.exception("Error in handle_fabric_result:")
            QMessageBox.critical(self, "Error", f"An error occurred while processing the result:\n\n{str(e)}")

        logger.debug("Hiding progress bar")
        self.progress_bar.setVisible(False)
        
        if self.worker_thread:
            self.worker_thread.wait()  # Wait for the worker thread to finish
            logger.debug("Resetting worker thread")
            self.worker_thread = None

    def display_wow_data(self, json_data):
        if not self.wow_widget:
            self.create_wow_widget()

        self.wow_widget.clear()
        self.populate_wow_tree(self.wow_widget.invisibleRootItem(), json_data)
        self.wow_widget.show()

    def create_wow_widget(self):
        self.wow_widget = QTreeWidget()
        self.wow_widget.setHeaderLabels(["Key", "Value"])
        self.wow_widget.setColumnCount(2)
        self.wow_widget.header().setSectionResizeMode(QTreeWidget.ResizeToContents)
        self.wow_widget.header().setStretchLastSection(False)

    def populate_wow_tree(self, parent_item, data):
        if isinstance(data, dict):
            for key, value in data.items():
                item = QTreeWidgetItem(parent_item, [str(key)])
                self.populate_wow_tree(item, value)
        elif isinstance(data, list):
            for i, value in enumerate(data):
                item = QTreeWidgetItem(parent_item, [str(i)])
                self.populate_wow_tree(item, value)
        else:
            item = QTreeWidgetItem(parent_item, [str(data)])
            parent_item.addChild(item)

    def hide_wow_widget(self):
        if self.wow_widget:
            self.wow_widget.hide()

    def clear_output(self):
        self.output_area.clear()
        self.hide_wow_widget()

    def clear_all(self):
        self.input_area.clear()
        self.output_area.clear()
        self.hide_wow_widget()

    def copy_output(self):
        text = self.output_area.toPlainText()
        markdown_utils.copy_raw_markdown(text)

    def apply_stylesheet(self):
        stylesheet_path = os.path.join(os.path.dirname(__file__), "styles.py")
        with open(stylesheet_path, "r") as file:
            stylesheet = file.read()
            self.setStyleSheet(stylesheet)

    def update_pattern_info(self):
        pattern = self.pattern_combo.currentText()
        pattern_dir = os.path.join("/Users/ben/fabric/patterns", pattern)

        if self.readme_radio.isChecked():
            readme_path = os.path.join(pattern_dir, "README.md")
            if os.path.exists(readme_path):
                with open(readme_path, "r") as file:
                    content = file.read()
                    html = markdown_utils.render_markdown(content)
                    self.info_area.setHtml(html)
            else:
                self.info_area.setPlainText("README.md not available for this pattern.")
        else:
            system_path = os.path.join(pattern_dir, "system.md")
            if os.path.exists(system_path):
                with open(system_path, "r") as file:
                    content = file.read()
                    html = markdown_utils.render_markdown(content)
                    self.info_area.setHtml(html)
            else:
                self.info_area.setPlainText("system.md not available for this pattern.")

    def handle_wow_pattern(self):
        if self.pattern_combo.currentText() == "get_wow_per_minute":
            self.show_wow_widget()
        else:
            self.hide_wow_widget()

    def show_wow_widget(self):
        if self.wow_widget:
            self.wow_widget.show()