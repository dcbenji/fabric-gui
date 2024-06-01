import sys
from PyQt5.QtWidgets import QApplication
from fabric_extractor_gui import FabricExtractorGUI

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = FabricExtractorGUI()
    window.show()
    sys.exit(app.exec_())