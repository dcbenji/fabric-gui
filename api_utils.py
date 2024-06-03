import json
import logging
import subprocess
from PyQt5.QtCore import QThread, pyqtSignal
from fabric_core import FabricCore

logger = logging.getLogger(__name__)

class FabricWorkerThread(QThread):
    finished = pyqtSignal(str, str, dict)

    def __init__(self, input_text, pattern, model):
        super().__init__()
        self.fabric_core = FabricCore()
        self.input_text = input_text
        self.pattern = pattern
        self.model = model

    def run(self):
        try:
            logger.debug("Starting fabric extraction")
            output, error, json_data = self.fabric_core.run_fabric_extraction(self.input_text, self.pattern, self.model)
            if self.pattern == "get_wow_per_minute":
                self.finished.emit(output, error, json_data)
            else:
                self.finished.emit(output, error, {})
        except Exception as e:
            logger.exception("An error occurred during fabric extraction.")
            self.finished.emit("", str(e), {})
        finally:
            self.quit()