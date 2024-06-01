import os

def get_available_patterns(self):
    patterns_dir = "/Users/ben/fabric/patterns"
    patterns = []
    if os.path.isdir(patterns_dir):
        for item in os.listdir(patterns_dir):
            item_path = os.path.join(patterns_dir, item)
            if os.path.isdir(item_path):
                patterns.append(item)
    return patterns

def update_pattern_info(self):
    pattern = self.pattern_combo.currentText()
    pattern_dir = os.path.join("/Users/ben/fabric/patterns", pattern)

    if self.readme_radio.isChecked():
        readme_path = os.path.join(pattern_dir, "README.md")
        if os.path.exists(readme_path):
            with open(readme_path, "r") as file:
                content = file.read()
                markdown_command = ["pipx", "run", "markdown2", "-x", "fenced-code-blocks"]
                markdown_process = subprocess.Popen(
                    markdown_command,
                    stdin=subprocess.PIPE,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    text=True,
                )
                html, _ = markdown_process.communicate(content)
                self.info_area.setHtml(html)
        else:
            self.info_area.setPlainText("README.md not available for this pattern.")
    else:
        system_path = os.path.join(pattern_dir, "system.md")
        if os.path.exists(system_path):
            with open(system_path, "r") as file:
                content = file.read()
                self.info_area.setPlainText(content)
        else:
            self.info_area.setPlainText("system.md not available for this pattern.")