/* Overall Application */
@font-face {
  font-family: "IBM Plex Sans";
  src: url("fonts/IBMPlexSans-Regular.ttf") format("truetype"),
       url("fonts/IBMPlexSans-Bold.ttf") format("truetype");
  font-weight: normal;
  font-style: normal;
}

QMainWindow {
  background-color: #262626;
}

QWidget {
  background-color: transparent;
  color: #F4F4F4;
  font-family: "IBM Plex Sans", sans-serif;
  font-size: 14px;
}

/* Group Boxes */
QGroupBox {
  border: 1px solid #393939;
  border-radius: 4px;
  padding: 15px;
}

QGroupBox::title {
  font-size: 14px;
  font-weight: bold;
  margin-bottom: 10px;
}

/* Text Input and Output */
QTextEdit {
  background-color: #161616;
  border: 1px solid #393939;
  border-radius: 4px;
  padding: 10px;
  font-family: "IBM Plex Mono", monospace;  /* Assuming you have this font */
}

/* Buttons */
QPushButton {
    background-color: #0F62FE;
    color: white;
    border: none;
    border-radius: 4px;
    padding: 8px 15px;
}

QPushButton:hover {
    background-color: #0353E9;
}

QPushButton:pressed {
    background-color: #0530AD;
}

/* Combo Boxes */
QComboBox {
    background-color: #393939;
    border: 1px solid #393939;
    border-radius: 4px;
    padding: 8px;
    min-height: 32px;
}

QComboBox QAbstractItemView {
    background-color: #393939;
    selection-background-color: #0F62FE;
}

QComboBox::drop-down {
    border: none;
}

QComboBox::down-arrow {
    image: url(../icons/chevron-down.svg);
    width: 16px;
    height: 16px;
    margin-right: 10px;
}

/* Progress Bar */
QProgressBar {
    border-radius: 2px;
    background-color: #393939;
    text-align: center;
}

QProgressBar::chunk {
    background-color: #0F62FE;
    border-radius: 2px;
}

/* Tree Widget for WOW Data */
QTreeWidget {
    background-color: #262626;
    alternate-background-color: #2E2E2E;
    border: 1px solid #393939;
    border-radius: 4px;
    padding: 10px;
}

QTreeWidget::item {
    color: #F4F4F4;
}

QTreeWidget::item:selected {
    background-color: #0F62FE;
}

QTreeWidget::branch {
    background-color: #393939;
}

QTreeWidget::branch:selected {
    background-color: #0F62FE;
}

QTreeWidget::branch:hover {
    background-color: #0353E9;
}

/* Radio Buttons */
QRadioButton {
    spacing: 5px;
}

QRadioButton::indicator {
    width: 16px;
    height: 16px;
}

QRadioButton::indicator:unchecked {
    image: url(../icons/radio-unchecked.svg);
}

QRadioButton::indicator:checked {
    image: url(../icons/radio-checked.svg);
}

/* Splitter */
QSplitter::handle {
    background-color: #393939;
    width: 1px;
}

QSplitter::handle:hover {
    background-color: #0F62FE;
}