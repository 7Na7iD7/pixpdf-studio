from PySide6.QtWidgets import QListWidget, QListWidgetItem, QWidget, QHBoxLayout, QVBoxLayout, QLabel, QAbstractItemView
from PySide6.QtGui import QPixmap
from PySide6.QtCore import Qt, QSize
from models.image_item import ImageItem


def format_size(num_bytes: int) -> str:
    for unit in ["B", "KB", "MB", "GB"]:
        if num_bytes < 1024:
            return f"{num_bytes:.1f} {unit}"
        num_bytes /= 1024
    return f"{num_bytes:.1f} TB"


class ImageRowWidget(QWidget):
    def __init__(self, item: ImageItem, parent=None):
        super().__init__(parent)
        self.item = item

        layout = QHBoxLayout(self)
        layout.setContentsMargins(8, 8, 8, 8)

        thumb = QLabel()
        thumb.setFixedSize(56, 56)
        thumb.setScaledContents(True)
        if item.thumbnail_path:
            thumb.setPixmap(QPixmap(item.thumbnail_path))
        layout.addWidget(thumb)

        info_layout = QVBoxLayout()
        name_label = QLabel(item.name)
        name_label.setStyleSheet("font-weight: 600;")

        details = f"{item.width}x{item.height} · {item.format} · {format_size(item.original_size)}"
        if item.compressed_size:
            details += f"  →  {format_size(item.compressed_size)} ({item.reduction_percent}% کاهش)"
        if item.is_cropped:
            details += "  ·  ✂ برش‌خورده"

        details_label = QLabel(details)
        details_label.setObjectName("SubtitleLabel")

        info_layout.addWidget(name_label)
        info_layout.addWidget(details_label)

        layout.addLayout(info_layout)
        layout.addStretch()

    def refresh(self):
        details = f"{self.item.width}x{self.item.height} · {self.item.format} · {format_size(self.item.original_size)}"
        if self.item.compressed_size:
            details += f"  →  {format_size(self.item.compressed_size)} ({self.item.reduction_percent}% کاهش)"


class ImageListWidget(QListWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setSelectionMode(QListWidget.ExtendedSelection)
        self.setDragDropMode(QListWidget.InternalMove)
        self.setSpacing(4)
        self.setVerticalScrollMode(QAbstractItemView.ScrollPerPixel)
        self.setHorizontalScrollMode(QAbstractItemView.ScrollPerPixel)
        self.verticalScrollBar().setSingleStep(14)

    def add_item(self, item: ImageItem):
        list_item = QListWidgetItem(self)
        list_item.setSizeHint(QSize(0, 72))
        row_widget = ImageRowWidget(item)
        list_item.setData(Qt.UserRole, item)
        self.addItem(list_item)
        self.setItemWidget(list_item, row_widget)

    def update_item_widget(self, item: ImageItem):
        for i in range(self.count()):
            list_item = self.item(i)
            stored = list_item.data(Qt.UserRole)
            if stored is item or stored.path == item.path:
                row_widget = ImageRowWidget(item)
                list_item.setData(Qt.UserRole, item)
                self.setItemWidget(list_item, row_widget)
                break

    def all_items(self) -> list[ImageItem]:
        result = []
        for i in range(self.count()):
            result.append(self.item(i).data(Qt.UserRole))
        return result

    def selected_items_data(self) -> list[ImageItem]:
        return [i.data(Qt.UserRole) for i in self.selectedItems()]
