import os
import subprocess
import sys
from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QFileDialog, QSplitter, QScrollArea, QMessageBox, QFrame
)
from PySide6.QtCore import Qt, QThreadPool, QSize
from PySide6.QtGui import QIcon, QPixmap

from models.settings_model import AppSettings
from models.image_item import ImageItem
from services.image_loader import ImageLoader
from services.settings_service import SettingsService
from services.workers import CompressionWorker, PdfBuildWorker
from widgets.drop_zone import DropZone
from widgets.image_list_widget import ImageListWidget
from widgets.compression_panel import CompressionPanel
from widgets.pdf_settings_panel import PdfSettingsPanel
from widgets.status_panel import StatusPanel
from widgets.gradient_label import GradientLabel
from ui.theme import DARK_QSS, LIGHT_QSS
from utils.logger import get_logger

APP_DATA_DIR = os.path.join(os.path.expanduser("~"), ".pixpdfstudio")
THUMB_DIR = os.path.join(APP_DATA_DIR, "thumbnails")
COMPRESSED_DIR = os.path.join(APP_DATA_DIR, "compressed")
RESOURCES_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "resources")
LOGO_PATH = os.path.join(RESOURCES_DIR, "icon.png")

logger = get_logger("MainWindow")


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PixPDF Studio — Smart Image Compression & PDF Creator")
        self.resize(1280, 800)
        if os.path.exists(LOGO_PATH):
            self.setWindowIcon(QIcon(LOGO_PATH))

        self.settings_service = SettingsService()
        self.app_settings: AppSettings = self.settings_service.load()
        if not self.app_settings.pdf.output_dir:
            self.app_settings.pdf.output_dir = os.path.join(os.path.expanduser("~"), "Desktop")

        self.image_loader = ImageLoader(THUMB_DIR)
        self.thread_pool = QThreadPool.globalInstance()
        self.thread_pool.setMaxThreadCount(max(2, os.cpu_count() or 4))

        self.active_compression_worker = None

        self._build_ui()
        self._apply_theme(self.app_settings.theme)

    def _build_ui(self):
        central = QWidget()
        self.setCentralWidget(central)
        root_layout = QVBoxLayout(central)
        root_layout.setContentsMargins(20, 16, 20, 8)
        root_layout.setSpacing(14)

        root_layout.addLayout(self._build_header())

        splitter = QSplitter(Qt.Horizontal)
        splitter.addWidget(self._build_left_column())
        splitter.addWidget(self._build_right_column())
        splitter.setSizes([760, 420])
        root_layout.addWidget(splitter)

        self.status_panel = StatusPanel()
        self.statusBar().addPermanentWidget(self.status_panel, 1)

    def _build_header(self) -> QHBoxLayout:
        layout = QHBoxLayout()
        layout.setSpacing(14)

        logo_badge = QFrame()
        logo_badge.setObjectName("LogoBadge")
        logo_badge.setFixedSize(46, 46)
        logo_layout = QVBoxLayout(logo_badge)
        logo_layout.setContentsMargins(0, 0, 0, 0)

        if os.path.exists(LOGO_PATH):
            logo_icon = QLabel()
            pixmap = QPixmap(LOGO_PATH).scaled(
                46, 46, Qt.KeepAspectRatio, Qt.SmoothTransformation
            )
            logo_icon.setPixmap(pixmap)
            logo_icon.setAlignment(Qt.AlignCenter)
            logo_icon.setStyleSheet("background: transparent;")
            logo_badge.setObjectName("LogoBadgeImage")
        else:
            logo_icon = QLabel("🖼️")
            logo_icon.setAlignment(Qt.AlignCenter)
            logo_icon.setStyleSheet("font-size: 22px; background: transparent;")
        logo_layout.addWidget(logo_icon)

        title_box = QVBoxLayout()
        title_box.setSpacing(4)
        title = GradientLabel("PixPDF Studio", ["#4C9EFF", "#7C5CFF", "#FF6FD8"])

        subtitle_row = QHBoxLayout()
        subtitle_row.setSpacing(6)
        subtitle_row.setContentsMargins(0, 0, 0, 0)
        subtitle_dot = QLabel("●")
        subtitle_dot.setObjectName("SubtitleDot")
        subtitle = QLabel("Smart Image Compression & PDF Creator")
        subtitle.setObjectName("SubtitleLabel")
        subtitle_row.addWidget(subtitle_dot)
        subtitle_row.addWidget(subtitle)
        subtitle_row.addStretch()

        title_box.addWidget(title)
        title_box.addLayout(subtitle_row)

        layout.addWidget(logo_badge)
        layout.addLayout(title_box)
        layout.addStretch()

        credits_badge = QFrame()
        credits_badge.setObjectName("CreditsBadge")
        credits_layout = QHBoxLayout(credits_badge)
        credits_layout.setContentsMargins(12, 6, 12, 6)
        credits_layout.setSpacing(6)
        credits_dot = QLabel("✦")
        credits_dot.setObjectName("CreditsDot")
        credits_text = QLabel("Crafted by <b>Na7iD</b> &amp; <b>Niki</b>")
        credits_text.setObjectName("CreditsText")
        credits_layout.addWidget(credits_dot)
        credits_layout.addWidget(credits_text)
        layout.addWidget(credits_badge)

        self.theme_button = QPushButton("Light Mode" if self.app_settings.theme == "Dark" else "Dark Mode")
        self.theme_button.setObjectName("SecondaryButton")
        self.theme_button.clicked.connect(self._toggle_theme)
        layout.addWidget(self.theme_button)

        return layout

    def _build_left_column(self) -> QWidget:
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setSpacing(12)

        self.drop_zone = DropZone()
        self.drop_zone.files_dropped.connect(self._on_files_dropped)
        self.drop_zone.mousePressEvent = lambda event: self._browse_files()
        layout.addWidget(self.drop_zone)

        action_row = QHBoxLayout()
        select_files_btn = QPushButton("انتخاب فایل‌ها")
        select_files_btn.clicked.connect(self._browse_files)
        select_folder_btn = QPushButton("انتخاب پوشه")
        select_folder_btn.setObjectName("SecondaryButton")
        select_folder_btn.clicked.connect(self._browse_folder)
        clear_btn = QPushButton("حذف همه")
        clear_btn.setObjectName("SecondaryButton")
        clear_btn.clicked.connect(self._clear_all)
        action_row.addWidget(select_files_btn)
        action_row.addWidget(select_folder_btn)
        action_row.addWidget(clear_btn)
        layout.addLayout(action_row)

        self.image_list = ImageListWidget()
        layout.addWidget(self.image_list, 1)

        convert_row = QHBoxLayout()
        self.convert_button = QPushButton("Convert to PDF")
        self.convert_button.clicked.connect(self._start_pipeline)
        convert_row.addStretch()
        convert_row.addWidget(self.convert_button)
        layout.addLayout(convert_row)

        return widget

    def _build_right_column(self) -> QWidget:
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QScrollArea.NoFrame)
        scroll.verticalScrollBar().setSingleStep(14)

        container = QWidget()
        layout = QVBoxLayout(container)
        layout.setSpacing(12)

        self.compression_panel = CompressionPanel(self.app_settings.compression)
        self.compression_panel.settings_changed.connect(self._persist_settings)
        layout.addWidget(self.compression_panel)

        self.pdf_settings_panel = PdfSettingsPanel(self.app_settings.pdf)
        self.pdf_settings_panel.settings_changed.connect(self._persist_settings)
        layout.addWidget(self.pdf_settings_panel)

        layout.addStretch()
        scroll.setWidget(container)
        return scroll

    def _browse_files(self):
        files, _ = QFileDialog.getOpenFileNames(
            self, "انتخاب تصاویر", self.app_settings.last_directory,
            "Images (*.jpg *.jpeg *.png *.webp *.bmp *.tiff *.tif)"
        )
        if files:
            self.app_settings.last_directory = os.path.dirname(files[0])
            self._add_images(files)

    def _browse_folder(self):
        folder = QFileDialog.getExistingDirectory(self, "انتخاب پوشه")
        if folder:
            self.app_settings.last_directory = folder
            files = self.image_loader.scan_folder(folder)
            self._add_images(files)

    def _on_files_dropped(self, paths: list[str]):
        all_files = []
        for path in paths:
            if os.path.isdir(path):
                all_files.extend(self.image_loader.scan_folder(path))
            elif self.image_loader.is_supported(path):
                all_files.append(path)
        self._add_images(all_files)

    def _add_images(self, files: list[str]):
        start_index = self.image_list.count()
        for i, path in enumerate(files):
            try:
                item = self.image_loader.load(path, start_index + i)
                self.image_list.add_item(item)
            except Exception as exc:
                logger.error(f"Failed to load {path}: {exc}")
        self.status_panel.set_status(f"{self.image_list.count()} تصویر بارگذاری شد")

    def _clear_all(self):
        self.image_list.clear()
        self.status_panel.set_status("آماده")

    def _start_pipeline(self):
        items = self.image_list.all_items()
        if not items:
            QMessageBox.warning(self, "خطا", "ابتدا حداقل یک تصویر اضافه کنید.")
            return

        os.makedirs(COMPRESSED_DIR, exist_ok=True)
        self.status_panel.set_status("در حال فشرده‌سازی...")

        worker = CompressionWorker(items, self.app_settings.compression, COMPRESSED_DIR)
        worker.signals.item_compressed.connect(self._on_item_compressed)
        worker.signals.progress.connect(self.status_panel.set_progress)
        worker.signals.finished.connect(lambda: self._on_compression_finished(items))
        worker.signals.error.connect(self._on_error)
        self.active_compression_worker = worker
        self.thread_pool.start(worker)

    def _on_item_compressed(self, item: ImageItem):
        self.image_list.update_item_widget(item)

    def _on_compression_finished(self, items: list[ImageItem]):
        self.status_panel.set_status("در حال ساخت PDF...")
        worker = PdfBuildWorker(items, self.app_settings.pdf)
        worker.signals.progress.connect(self.status_panel.set_progress)
        worker.signals.pdf_finished.connect(self._on_pdf_finished)
        worker.signals.error.connect(self._on_error)
        self.thread_pool.start(worker)

    def _on_pdf_finished(self, output_path: str):
        self.status_panel.set_status(f"PDF ساخته شد: {output_path}")
        self._persist_settings()

        reply = QMessageBox.question(
            self, "موفقیت", f"فایل PDF با موفقیت ساخته شد:\n{output_path}\n\nباز شود؟",
            QMessageBox.Yes | QMessageBox.No
        )
        if reply == QMessageBox.Yes:
            self._open_path(output_path)

    def _open_path(self, path: str):
        try:
            if sys.platform.startswith("win"):
                os.startfile(path)
            elif sys.platform == "darwin":
                subprocess.call(["open", path])
            else:
                subprocess.call(["xdg-open", path])
        except Exception as exc:
            logger.error(f"Failed to open {path}: {exc}")

    def _on_error(self, message: str):
        logger.error(message)
        self.status_panel.set_status("خطا رخ داد")
        QMessageBox.critical(self, "خطا", message)

    def _toggle_theme(self):
        new_theme = "Light" if self.app_settings.theme == "Dark" else "Dark"
        self.app_settings.theme = new_theme
        self.theme_button.setText("Light Mode" if new_theme == "Dark" else "Dark Mode")
        self._apply_theme(new_theme)
        self._persist_settings()

    def _apply_theme(self, theme: str):
        self.setStyleSheet(DARK_QSS if theme == "Dark" else LIGHT_QSS)

    def _persist_settings(self):
        self.settings_service.save(self.app_settings)

    def closeEvent(self, event):
        self._persist_settings()
        super().closeEvent(event)
