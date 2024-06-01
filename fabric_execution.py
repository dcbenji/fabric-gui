import re
import subprocess
from PyQt5.QtWidgets import QMessageBox
from fabric_worker_thread import FabricWorkerThread

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
    if error:
        logger.error(f"Fabric extraction error: {error}")
        QMessageBox.critical(self, "Error", f"An error occurred during fabric extraction:\n\n{error}")
    else:
        if json_data:
            self.display_wow_data(json_data)
        else:
            self.output_area.setPlainText(output)

    self.progress_bar.setVisible(False)
    self.worker_thread = None