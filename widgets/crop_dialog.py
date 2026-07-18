from io import BytesIO
from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QGraphicsView, QGraphicsScene, QGraphicsPixmapItem, QGraphicsRectItem
)
from PySide6.QtGui import QPixmap, QPen, QColor, QBrush, QPainter
from PySide6.QtCore import Qt, QRectF, QPointF
from PIL import Image, ImageOps
from models.image_item import ImageItem


class CropView(QGraphicsView):
    def __init__(self, pixmap: QPixmap, parent=None):
        super().__init__(parent)
        self.setRenderHint(QPainter.Antialiasing)
        self.setRenderHint(QPainter.SmoothPixmapTransform)
        self.scene_ = QGraphicsScene(self)
        self.setScene(self.scene_)
        self.pixmap_item = QGraphicsPixmapItem(pixmap)
        self.scene_.addItem(self.pixmap_item)
        self.setSceneRect(QRectF(0, 0, pixmap.width(), pixmap.height()))
        self.rect_item = None
        self.origin = None
        self.setDragMode(QGraphicsView.NoDrag)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.origin = self.mapToScene(event.pos())
            if self.rect_item:
                self.scene_.removeItem(self.rect_item)
                self.rect_item = None
            pen = QPen(QColor("#00F0FF"))
            pen.setWidth(2)
            brush = QBrush(QColor(76, 158, 255, 60))
            self.rect_item = QGraphicsRectItem(QRectF(self.origin, self.origin))
            self.rect_item.setPen(pen)
            self.rect_item.setBrush(brush)
            self.scene_.addItem(self.rect_item)
        super().mousePressEvent(event)

    def mouseMoveEvent(self, event):
        if self.rect_item is not None and self.origin is not None:
            current = self.mapToScene(event.pos())
            rect = QRectF(self.origin, current).normalized()
            rect = rect.intersected(self.sceneRect())
            self.rect_item.setRect(rect)
        super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        self.origin = None
        super().mouseReleaseEvent(event)

    def current_rect(self) -> QRectF:
        if self.rect_item:
            return self.rect_item.rect()
        return QRectF()

    def clear_selection(self):
        if self.rect_item:
            self.scene_.removeItem(self.rect_item)
            self.rect_item = None


class CropDialog(QDialog):
    MAX_DISPLAY_DIM = 760

    def __init__(self, item: ImageItem, parent=None):
        super().__init__(parent)
        self.item = item
        self.result_box = item.crop_box
        self.setWindowTitle(f"برش تصویر — {item.name}")
        self.setMinimumSize(500, 500)

        with Image.open(item.path) as im:
            im = ImageOps.exif_transpose(im).convert("RGB")
            self.original_size = im.size
            scale = min(1.0, self.MAX_DISPLAY_DIM / max(im.size))
            self.scale = scale
            display_w = max(1, int(im.width * scale))
            display_h = max(1, int(im.height * scale))
            display_im = im.resize((display_w, display_h), Image.LANCZOS)

            buffer = BytesIO()
            display_im.save(buffer, format="PNG")
            pixmap = QPixmap()
            pixmap.loadFromData(buffer.getvalue(), "PNG")

        layout = QVBoxLayout(self)
        layout.setContentsMargins(16, 16, 16, 16)
        layout.setSpacing(10)

        hint = QLabel("با کشیدن ماوس روی تصویر، ناحیه‌ی موردنظر برای برش را انتخاب کنید")
        hint.setObjectName("SubtitleLabel")
        layout.addWidget(hint)

        self.view = CropView(pixmap)
        self.view.setFixedSize(pixmap.width() + 4, pixmap.height() + 4)
        layout.addWidget(self.view, alignment=Qt.AlignCenter)

        if item.crop_box:
            left, top, right, bottom = item.crop_box
            self.view.rect_item = QGraphicsRectItem(QRectF(
                left * scale, top * scale, (right - left) * scale, (bottom - top) * scale
            ))
            pen = QPen(QColor("#00F0FF"))
            pen.setWidth(2)
            self.view.rect_item.setPen(pen)
            self.view.rect_item.setBrush(QBrush(QColor(76, 158, 255, 60)))
            self.view.scene_.addItem(self.view.rect_item)

        button_row = QHBoxLayout()
        reset_btn = QPushButton("حذف برش")
        reset_btn.setObjectName("SecondaryButton")
        reset_btn.clicked.connect(self._reset)

        cancel_btn = QPushButton("انصراف")
        cancel_btn.setObjectName("SecondaryButton")
        cancel_btn.clicked.connect(self.reject)

        apply_btn = QPushButton("اعمال برش")
        apply_btn.clicked.connect(self._apply)

        button_row.addWidget(reset_btn)
        button_row.addStretch()
        button_row.addWidget(cancel_btn)
        button_row.addWidget(apply_btn)
        layout.addLayout(button_row)

    def _reset(self):
        self.view.clear_selection()
        self.result_box = None
        self.accept()

    def _apply(self):
        rect = self.view.current_rect()
        if rect.isEmpty() or rect.width() < 5 or rect.height() < 5:
            self.result_box = None
            self.accept()
            return

        left = max(0, int(rect.left() / self.scale))
        top = max(0, int(rect.top() / self.scale))
        right = min(self.original_size[0], int(rect.right() / self.scale))
        bottom = min(self.original_size[1], int(rect.bottom() / self.scale))

        self.result_box = (left, top, right, bottom)
        self.accept()
