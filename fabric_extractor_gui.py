from PyQt5.QtWidgets import QMainWindow, QWidget, QHBoxLayout
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt

class FabricExtractorGUI(QMainWindow):
    def __init__(self):
        super().__init__()
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