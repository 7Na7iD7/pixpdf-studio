from PySide6.QtWidgets import QFrame, QVBoxLayout, QLabel
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QDragEnterEvent, QDropEvent


class DropZone(QFrame):
    files_dropped = Signal(list)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("DropZone")
        self.setAcceptDrops(True)
        self.setMinimumHeight(160)

        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignCenter)

        icon_label = QLabel("📥")
        icon_label.setAlignment(Qt.AlignCenter)
        icon_label.setStyleSheet("font-size: 40px;")

        title = QLabel("تصاویر را اینجا رها کنید")
        title.setAlignment(Qt.AlignCenter)
        title.setObjectName("TitleLabel")

        subtitle = QLabel("یا کلیک کنید برای انتخاب فایل / پوشه")
        subtitle.setAlignment(Qt.AlignCenter)
        subtitle.setObjectName("SubtitleLabel")

        layout.addWidget(icon_label)
        layout.addWidget(title)
        layout.addWidget(subtitle)

    def dragEnterEvent(self, event: QDragEnterEvent):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()

    def dropEvent(self, event: QDropEvent):
        paths = [url.toLocalFile() for url in event.mimeData().urls()]
        self.files_dropped.emit(paths)

    def mousePressEvent(self, event):
        self.clicked()

    def clicked(self):
        pass
