DARK_QSS = """
QWidget {
    background-color: #1E1F26;
    color: #E8E8ED;
    font-family: 'Segoe UI';
    font-size: 13px;
}
QMainWindow {
    background-color: #17181D;
}
QFrame#Card {
    background-color: #24252E;
    border-radius: 14px;
    border: 1px solid #2E2F3A;
}
QFrame#DropZone {
    background-color: #24252E;
    border: 2px dashed #4C9EFF;
    border-radius: 16px;
}
QLabel#TitleLabel {
    font-size: 20px;
    font-weight: 600;
    color: #FFFFFF;
}
QLabel#SubtitleLabel {
    color: #9A9BA5;
    font-size: 11px;
    font-weight: 500;
    letter-spacing: 0.5px;
}
QLabel#SubtitleDot {
    color: #7C5CFF;
    font-size: 8px;
}
QFrame#LogoBadge {
    background-color: qlineargradient(
        x1:0, y1:0, x2:1, y2:1,
        stop:0 #4C9EFF, stop:1 #7C5CFF
    );
    border-radius: 13px;
}
QFrame#CreditsBadge {
    background-color: #24252E;
    border: 1px solid #33344A;
    border-radius: 16px;
}
QLabel#CreditsDot {
    color: #7C5CFF;
    font-size: 13px;
    background: transparent;
}
QLabel#CreditsText {
    color: #B7B8C4;
    font-size: 12px;
    background: transparent;
}
QPushButton {
    background-color: #4C9EFF;
    color: #FFFFFF;
    border-radius: 10px;
    padding: 8px 18px;
    font-weight: 600;
    border: none;
}
QPushButton:hover {
    background-color: #6BAEFF;
}
QPushButton:pressed {
    background-color: #3B85DE;
}
QPushButton#SecondaryButton {
    background-color: #2E2F3A;
    color: #E8E8ED;
}
QPushButton#SecondaryButton:hover {
    background-color: #383946;
}
QListWidget {
    background-color: #24252E;
    border-radius: 12px;
    border: 1px solid #2E2F3A;
    padding: 6px;
}
QListWidget::item {
    border-radius: 8px;
    padding: 6px;
    margin: 2px;
}
QListWidget::item:selected {
    background-color: #33415C;
}
QSlider::groove:horizontal {
    height: 6px;
    background: #2E2F3A;
    border-radius: 3px;
}
QSlider::handle:horizontal {
    background: #4C9EFF;
    width: 16px;
    height: 16px;
    margin: -6px 0;
    border-radius: 8px;
}
QComboBox {
    background-color: #2E2F3A;
    border-radius: 8px;
    padding: 6px 10px;
    border: 1px solid #383946;
}
QLineEdit {
    background-color: #2E2F3A;
    border-radius: 8px;
    padding: 6px 10px;
    border: 1px solid #383946;
}
QProgressBar {
    background-color: #2E2F3A;
    border-radius: 8px;
    text-align: center;
    height: 14px;
}
QProgressBar::chunk {
    background-color: #4C9EFF;
    border-radius: 8px;
}
QStatusBar {
    background-color: #17181D;
    color: #9A9BA5;
}
QTabWidget::pane {
    border: 1px solid #2E2F3A;
    border-radius: 10px;
}
QTabBar::tab {
    background: #24252E;
    padding: 8px 16px;
    border-top-left-radius: 8px;
    border-top-right-radius: 8px;
    margin-right: 4px;
}
QTabBar::tab:selected {
    background: #4C9EFF;
    color: white;
}
QScrollBar:vertical {
    background: transparent;
    width: 10px;
    margin: 2px;
}
QScrollBar::handle:vertical {
    background: #3A3B47;
    border-radius: 5px;
    min-height: 30px;
}
QScrollBar::handle:vertical:hover {
    background: #4C9EFF;
}
QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
    height: 0px;
    background: none;
    border: none;
}
QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {
    background: none;
}
QScrollBar:horizontal {
    background: transparent;
    height: 10px;
    margin: 2px;
}
QScrollBar::handle:horizontal {
    background: #3A3B47;
    border-radius: 5px;
    min-width: 30px;
}
QScrollBar::handle:horizontal:hover {
    background: #4C9EFF;
}
QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal {
    width: 0px;
    background: none;
    border: none;
}
QScrollBar::add-page:horizontal, QScrollBar::sub-page:horizontal {
    background: none;
}
"""

LIGHT_QSS = """
QWidget {
    background-color: #F5F6FA;
    color: #1E1F26;
    font-family: 'Segoe UI';
    font-size: 13px;
}
QMainWindow {
    background-color: #EEF0F5;
}
QFrame#Card {
    background-color: #FFFFFF;
    border-radius: 14px;
    border: 1px solid #E0E1E8;
}
QFrame#DropZone {
    background-color: #FFFFFF;
    border: 2px dashed #4C9EFF;
    border-radius: 16px;
}
QLabel#TitleLabel {
    font-size: 20px;
    font-weight: 600;
    color: #111;
}
QLabel#SubtitleLabel {
    color: #6B6C76;
    font-size: 11px;
    font-weight: 500;
    letter-spacing: 0.5px;
}
QLabel#SubtitleDot {
    color: #7C5CFF;
    font-size: 8px;
}
QFrame#LogoBadge {
    background-color: qlineargradient(
        x1:0, y1:0, x2:1, y2:1,
        stop:0 #4C9EFF, stop:1 #7C5CFF
    );
    border-radius: 13px;
}
QFrame#CreditsBadge {
    background-color: #FFFFFF;
    border: 1px solid #E0E1E8;
    border-radius: 16px;
}
QLabel#CreditsDot {
    color: #7C5CFF;
    font-size: 13px;
    background: transparent;
}
QLabel#CreditsText {
    color: #565761;
    font-size: 12px;
    background: transparent;
}
QPushButton {
    background-color: #4C9EFF;
    color: #FFFFFF;
    border-radius: 10px;
    padding: 8px 18px;
    font-weight: 600;
    border: none;
}
QPushButton:hover {
    background-color: #6BAEFF;
}
QPushButton#SecondaryButton {
    background-color: #E4E6EE;
    color: #1E1F26;
}
QListWidget {
    background-color: #FFFFFF;
    border-radius: 12px;
    border: 1px solid #E0E1E8;
    padding: 6px;
}
QListWidget::item:selected {
    background-color: #D8E7FF;
}
QSlider::groove:horizontal {
    height: 6px;
    background: #E0E1E8;
    border-radius: 3px;
}
QSlider::handle:horizontal {
    background: #4C9EFF;
    width: 16px;
    height: 16px;
    margin: -6px 0;
    border-radius: 8px;
}
QComboBox, QLineEdit {
    background-color: #FFFFFF;
    border-radius: 8px;
    padding: 6px 10px;
    border: 1px solid #E0E1E8;
}
QProgressBar {
    background-color: #E0E1E8;
    border-radius: 8px;
    text-align: center;
    height: 14px;
}
QProgressBar::chunk {
    background-color: #4C9EFF;
    border-radius: 8px;
}
QStatusBar {
    background-color: #EEF0F5;
    color: #6B6C76;
}
QScrollBar:vertical {
    background: transparent;
    width: 10px;
    margin: 2px;
}
QScrollBar::handle:vertical {
    background: #C7C9D6;
    border-radius: 5px;
    min-height: 30px;
}
QScrollBar::handle:vertical:hover {
    background: #4C9EFF;
}
QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
    height: 0px;
    background: none;
    border: none;
}
QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {
    background: none;
}
QScrollBar:horizontal {
    background: transparent;
    height: 10px;
    margin: 2px;
}
QScrollBar::handle:horizontal {
    background: #C7C9D6;
    border-radius: 5px;
    min-width: 30px;
}
QScrollBar::handle:horizontal:hover {
    background: #4C9EFF;
}
QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal {
    width: 0px;
    background: none;
    border: none;
}
QScrollBar::add-page:horizontal, QScrollBar::sub-page:horizontal {
    background: none;
}
"""
