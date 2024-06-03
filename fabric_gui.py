from PyQt5.QtWidgets import (
    QMainWindow, QWidget, QLabel, QLineEdit, QTextEdit, QVBoxLayout,
    QHBoxLayout, QPushButton, QRadioButton, QButtonGroup, QFileDialog,
    QMessageBox, QGroupBox, QGridLayout, QComboBox, QProgressBar,
    QTreeWidget, QTreeWidgetItem, QSplitter
)
from PyQt5.QtGui import QFont, QIcon
from PyQt5.QtCore import Qt, QThread, pyqtSignal
from fabric_core import FabricCore, FabricWorkerThread, handle_api_key_error, handle_network_error, handle_unsupported_file_format, handle_missing_required_data, handle_invalid_user_input, logger
from error_handling import InvalidAPIKeyError, NetworkConnectionError, UnsupportedFileFormatError, MissingRequiredDataError, InvalidUserInputError
import markdown_utils

class FabricExtractorGUI(QMainWindow):
    def __init__(self, app):
        super().__init__()
        self.app = app
        self.fabric_core = FabricCore()
        self.initUI()
        self.worker_thread = None
        self.wow_widget = None
        
    def clear_all(self):
        self.input_area.clear()
        self.output_area.clear()
        self.fabric_core.hide_wow_widget()

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
        self.pattern_combo.addItems(self.fabric_core.get_available_patterns())
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
        try:
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
                    handle_unsupported_file_format(self)
        except UnsupportedFileFormatError:
            # Error handling for unsupported file format
            pass
        except Exception as e:
            logger.exception("Error in select_file:")
            QMessageBox.critical(self, "Error", f"An unexpected error occurred: {str(e)}")

    def run_fabric_extraction(self):
        try:
            if self.worker_thread and self.worker_thread.isRunning():
                logger.debug("Worker thread is already running")
                return

            input_text = self.input_area.toPlainText().strip()
            logger.debug(f"Input text: {input_text}")

            if self.fabric_core.is_youtube_link(input_text):
                video_id = self.fabric_core.extract_video_id(input_text)
                if video_id:
                    logger.debug(f"Extracting transcript from YouTube video: {video_id}")
                    input_text = self.fabric_core.get_transcript_from_youtube(f"https://youtu.be/{video_id}")
                else:
                    logger.debug("Invalid YouTube link")
                    handle_invalid_user_input(self)
                    return
            elif input_text.lower().endswith((".mp3", ".wav", ".m4a")):
                logger.debug(f"Extracting transcript from audio file: {input_text}")
                input_text = self.fabric_core.get_transcript_from_audio(input_text)

            pattern = self.pattern_combo.currentText()
            model = self.model_combo.currentText()
            logger.debug(f"Selected pattern: {pattern}")
            logger.debug(f"Selected model: {model}")

            self.worker_thread = FabricWorkerThread(input_text, pattern, model)
            self.worker_thread.started.connect(self.show_progress_bar)
            self.worker_thread.finished.connect(self.handle_fabric_result)
            logger.debug("Starting worker thread")
            self.worker_thread.start()
        except InvalidUserInputError:
            # Error handling for invalid user input
            logger.exception("Invalid user input")
        except Exception as e:
            logger.exception("Error in run_fabric_extraction:")
            QMessageBox.critical(self, "Error", f"An unexpected error occurred: {str(e)}")

    def show_progress_bar(self):
        self.progress_bar.setVisible(True)
        self.progress_bar.setMaximum(0)
        self.progress_bar.setMinimum(0)
        self.progress_bar.setValue(-1)

    def update_progress_bar(self, progress):
        self.progress_bar.setValue(progress)

    def handle_fabric_result(self, output, error, json_data):
        try:
            logger.debug("Handling fabric result")
            if error:
                logger.error(f"Fabric extraction error: {error}")
                if "InvalidAPIKeyError" in error:
                    handle_api_key_error(self)
                elif "NetworkConnectionError" in error:
                    handle_network_error(self)
                else:
                    QMessageBox.critical(self, "Error", f"An error occurred during fabric extraction:\n\n{error}")
            else:
                logger.debug("Setting output text")
                self.output_area.setPlainText(output)
                if json_data:
                    logger.debug("Displaying WOW data")
                    self.fabric_core.display_wow_data(json_data)
                else:
                    logger.debug("Hiding WOW widget")
                    self.fabric_core.hide_wow_widget()
        except InvalidAPIKeyError:
            # Error handling for invalid API key
            pass
        except NetworkConnectionError:
            # Error handling for network connection error
            pass
        except Exception as e:
            logger.exception("Error in handle_fabric_result:")
            QMessageBox.critical(self, "Error", f"An unexpected error occurred: {str(e)}")

        logger.debug("Hiding progress bar")
        self.progress_bar.setVisible(False)

        if self.worker_thread:
            logger.debug("Waiting for worker thread to finish")
            self.worker_thread.wait()  # Wait for the worker thread to finish
            logger.debug("Worker thread finished")
            self.worker_thread = None

    def create_wow_widget(self):
        # GUI-specific WOW widget creation code
        pass

    def populate_wow_tree(self, parent_item, data):
        # GUI-specific WOW widget population code
        pass

    def clear_output(self):
        self.output_area.clear()
        self.fabric_core.hide_wow_widget()

    def clear_all(self):
        self.input_area.clear()
        self.output_area.clear()
        self.fabric_core.hide_wow_widget()

    def copy_output(self):
        text = self.output_area.toPlainText()
        self.fabric_core.copy_output(text)

    def apply_stylesheet(self):
        # GUI-specific stylesheet application code
        pass

    def update_pattern_info(self):
        # GUI-specific pattern information update code
        pass

    def handle_wow_pattern(self):
        if self.pattern_combo.currentText() == "get_wow_per_minute":
            self.show_wow_widget()
        else:
            self.fabric_core.hide_wow_widget()

    def show_wow_widget(self):
        # GUI-specific WOW widget display code
        pass