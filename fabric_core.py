import os
import re
import subprocess
import markdown_utils
import logging
import json
from PyQt5.QtCore import QThread, pyqtSignal
from error_handling import (
    handle_api_key_error,
    handle_network_error,
    handle_unsupported_file_format,
    handle_missing_required_data,
    handle_invalid_user_input,
    InvalidAPIKeyError,
    NetworkConnectionError,
    UnsupportedFileFormatError,
    MissingRequiredDataError,
    InvalidUserInputError
)

logger = logging.getLogger(__name__)

class FabricWorkerThread(QThread):
    started = pyqtSignal()
    progress = pyqtSignal(int)
    finished = pyqtSignal(str, str, dict)

    def __init__(self, input_text, pattern, model):
        super().__init__()
        self.input_text = input_text
        self.pattern = pattern
        self.model = model

    def run(self):
        try:
            logger.debug("Worker thread started")
            self.started.emit()
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
            logger.debug(f"Output: {self.output}")
            logger.debug(f"Error: {self.error}")

            if self.pattern == "get_wow_per_minute":
                try:
                    json_output = json.loads(self.output)
                    logger.debug(f"JSON output: {json_output}")
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
            logger.debug("Worker thread finished")
            self.quit()

class FabricCore:
    def __init__(self):
        pass

    def get_available_patterns(self):
        patterns_dir = "/Users/ben/fabric/patterns"
        patterns = []
        if os.path.isdir(patterns_dir):
            for item in os.listdir(patterns_dir):
                item_path = os.path.join(patterns_dir, item)
                if os.path.isdir(item_path):
                    patterns.append(item)
        return patterns

    def is_youtube_link(self, link):
        youtube_regex = re.compile(r'(https?://)?(www\.)?(youtube|youtu|youtube-nocookie)\.(com|be)/(watch\?v=|embed/|v/|.+\?v=)?([^&=%\?]{11})')
        return youtube_regex.match(link)

    def extract_video_id(self, link):
        youtube_regex = re.compile(r'(https?://)?(www\.)?(youtube|youtu|youtube-nocookie)\.(com|be)/(watch\?v=|embed/|v/|.+\?v=)?([^&=%\?]{11})')
        match = youtube_regex.match(link)
        if match:
            return match.group(6)
        return None

    def get_transcript_from_youtube(self, video_url):
        yt_command = ["yt", "--transcript", video_url]
        yt_result = subprocess.run(
            yt_command,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )
        if yt_result.returncode == 0:
            return yt_result.stdout
        else:
            raise subprocess.CalledProcessError(yt_result.returncode, yt_command, yt_result.stderr)

    def get_transcript_from_audio(self, audio_file):
        ts_command = ["ts", audio_file]
        ts_result = subprocess.run(
            ts_command,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )
        if ts_result.returncode == 0:
            return ts_result.stdout
        else:
            raise subprocess.CalledProcessError(ts_result.returncode, ts_command, ts_result.stderr)

    def run_fabric_extraction(self, input_text, pattern, model):
        try:
            worker_thread = FabricWorkerThread(input_text, pattern, model)
            worker_thread.started.connect(self.show_progress_bar)
            worker_thread.progress.connect(self.update_progress_bar)
            worker_thread.finished.connect(self.handle_fabric_result)
            worker_thread.start()
            return worker_thread
        except InvalidAPIKeyError:
            handle_api_key_error()
        except NetworkConnectionError:
            handle_network_error()
        except UnsupportedFileFormatError:
            handle_unsupported_file_format()
        except MissingRequiredDataError:
            handle_missing_required_data()
        except InvalidUserInputError:
            handle_invalid_user_input()
        except Exception as e:
            logger.exception("Error in run_fabric_extraction:")
            raise e

    def display_wow_data(self, json_data):
        pass

    def hide_wow_widget(self):
        pass

    def copy_output(self, text):
        markdown_utils.copy_raw_markdown(text)

    def show_progress_bar(self):
        # Placeholder method, to be implemented in the GUI
        pass

    def update_progress_bar(self, progress):
        # Placeholder method, to be implemented in the GUI
        pass

    def handle_fabric_result(self, output, error, json_data):
        # Placeholder method, to be implemented in the GUI
        pass