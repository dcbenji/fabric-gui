/* Overall Application */

@font-face {
    font-family: "Inter";
    src: url(../fonts/Inter-Regular.ttf); /* Relative path to fonts folder */
}

@font-face {
    font-family: "Inter";
    src: url(../fonts/Inter-Bold.ttf); /* Relative path to fonts folder */
    font-weight: bold;
}

QMainWindow {
    background-color: #161616; /* Carbon dark background */
}

QWidget {
    background-color: transparent;
    color: #FFFFFF;
    font-family: "Inter", sans-serif; /* Elegant sans-serif font */
    font-size: 14px;
}

/* Group Boxes */
QGroupBox {
    border: 1px solid #393939; /* Subtle Carbon border */
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
    background-color: #262626; /* Darker background */
    border: 1px solid #393939;
    border-radius: 4px;
    padding: 10px;
    font-family: "IBM Plex Mono", monospace; /* Monospace for code */
}

/* Buttons */
QPushButton {
    background-color: #0F62FE; /* IBM Carbon blue */
    color: white;
    border: none;
    border-radius: 4px;
    padding: 8px 15px;
}

QPushButton:hover {
    background-color: #0353E9; /* Slightly darker on hover */
}

/* Combo Boxes */
QComboBox {
    background-color: #262626;
    border: 1px solid #393939;
    border-radius: 4px;
    padding: 8px;
    min-height: 32px; /* Consistent with button height */
}

QComboBox QAbstractItemView {
    background-color: #262626;
    selection-background-color: #0F62FE;
}

/* Removed QComboBox::down-arrow rule */ 

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
    color: #FFFFFF;
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
