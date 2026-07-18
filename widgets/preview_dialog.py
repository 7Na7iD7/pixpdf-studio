from io import BytesIO
from typing import List
from PySide6.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QScrollArea
from PySide6.QtGui import QPixmap
from PySide6.QtCore import Qt
from PIL import Image


class PdfPreviewDialog(QDialog):
    def __init__(self, pages: List[Image.Image], parent=None):
        super().__init__(parent)
        self.pages = pages
        self.current_index = 0
        self.proceed = False

        self.setWindowTitle("پیش‌نمایش PDF")
        self.setMinimumSize(640, 760)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(16, 16, 16, 16)
        layout.setSpacing(10)

        title = QLabel("پیش‌نمایش قبل از ذخیره نهایی")
        title.setObjectName("TitleLabel")
        layout.addWidget(title)

        self.page_label = QLabel()
        self.page_label.setObjectName("SubtitleLabel")
        layout.addWidget(self.page_label)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        self.image_label = QLabel()
        self.image_label.setAlignment(Qt.AlignCenter)
        scroll.setWidget(self.image_label)
        layout.addWidget(scroll, 1)

        nav_row = QHBoxLayout()
        self.prev_btn = QPushButton("◀ صفحه قبل")
        self.prev_btn.setObjectName("SecondaryButton")
        self.prev_btn.clicked.connect(self._show_prev)

        self.next_btn = QPushButton("صفحه بعد ▶")
        self.next_btn.setObjectName("SecondaryButton")
        self.next_btn.clicked.connect(self._show_next)

        nav_row.addWidget(self.prev_btn)
        nav_row.addStretch()
        nav_row.addWidget(self.next_btn)
        layout.addLayout(nav_row)

        action_row = QHBoxLayout()
        cancel_btn = QPushButton("انصراف")
        cancel_btn.setObjectName("SecondaryButton")
        cancel_btn.clicked.connect(self.reject)

        proceed_btn = QPushButton("ذخیره PDF نهایی")
        proceed_btn.clicked.connect(self._confirm)

        action_row.addStretch()
        action_row.addWidget(cancel_btn)
        action_row.addWidget(proceed_btn)
        layout.addLayout(action_row)

        self._render_current_page()

    def _render_current_page(self):
        if not self.pages:
            return
        page = self.pages[self.current_index]
        buffer = BytesIO()
        page.save(buffer, format="PNG")
        pixmap = QPixmap()
        pixmap.loadFromData(buffer.getvalue(), "PNG")

        scaled = pixmap.scaledToWidth(560, Qt.SmoothTransformation)
        self.image_label.setPixmap(scaled)
        self.page_label.setText(f"صفحه {self.current_index + 1} از {len(self.pages)}")
        self.prev_btn.setEnabled(self.current_index > 0)
        self.next_btn.setEnabled(self.current_index < len(self.pages) - 1)

    def _show_prev(self):
        if self.current_index > 0:
            self.current_index -= 1
            self._render_current_page()

    def _show_next(self):
        if self.current_index < len(self.pages) - 1:
            self.current_index += 1
            self._render_current_page()

    def _confirm(self):
        self.proceed = True
        self.accept()
