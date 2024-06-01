from PyQt5.QtWidgets import QVBoxLayout, QGroupBox, QTextEdit, QPushButton, QGridLayout, QLabel, QComboBox, QHBoxLayout, QProgressBar, QRadioButton
from PyQt5.QtGui import QIcon

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