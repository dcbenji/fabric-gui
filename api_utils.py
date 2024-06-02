import json
import logging
import subprocess
from PyQt5.QtCore import QThread, pyqtSignal

logger = logging.getLogger(__name__)

class FabricWorkerThread(QThread):
    finished = pyqtSignal(str, str, dict)

    def __init__(self, input_text, pattern, model):
        super().__init__()
        self.input_text = input_text
        self.pattern = pattern
        self.model = model

    def run(self):
        try:
            logger.debug("Starting fabric extraction")
            fabric_command = [
                "fabric",
                "--model",
                self.model,
                "-sp",
                self.pattern,
            ]
            logger.debug(f"Running fabric command: {fabric_command}")
            self.fabric_result = subprocess.run(
                fabric_command,
                input=self.input_text,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
            )
            logger.debug("Fabric extraction completed")
            self.output = self.fabric_result.stdout
            self.error = self.fabric_result.stderr

            if self.pattern == "get_wow_per_minute":
                try:
                    json_output = json.loads(self.output)
                    self.finished.emit(self.output, self.error, json_output)
                except json.JSONDecodeError as e:
                    logger.exception("Error decoding JSON output")
                    self.finished.emit("", str(e), {})
            else:
                self.finished.emit(self.output, self.error, {})

        except Exception as e:
            logger.exception("An error occurred during fabric extraction.")
            self.finished.emit("", str(e), {})

        finally:
            self.quit()