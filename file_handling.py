from PyQt5.QtWidgets import QFileDialog, QMessageBox

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