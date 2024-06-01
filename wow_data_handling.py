from PyQt5.QtWidgets import QTreeWidget, QTreeWidgetItem

def display_wow_data(self, json_data):
    if not self.wow_widget:
        self.wow_widget = QTreeWidget()
        self.wow_widget.setHeaderLabels(["Key", "Value"])
        self.wow_widget.setColumnCount(2)
    else:
        self.wow_widget.clear()

    self.populate_wow_tree(self.wow_widget.invisibleRootItem(), json_data)
    self.wow_widget.show()

def populate_wow_tree(self, parent_item, data):
    if isinstance(data, dict):
        for key, value in data.items():
            item = QTreeWidgetItem(parent_item, [str(key)])
            self.populate_wow_tree(item, value)
    elif isinstance(data, list):
        for i, value in enumerate(data):
            item = QTreeWidgetItem(parent_item, [str(i)])
            self.populate_wow_tree(item, value)
    else:
        item = QTreeWidgetItem(parent_item, [str(data)])
        parent_item.addChild(item)

def handle_wow_pattern(self):
    if self.pattern_combo.currentText() == "get_wow_per_minute":
        if self.wow_widget:
            self.wow_widget.show()
    else:
        if self.wow_widget:
            self.wow_widget.hide()