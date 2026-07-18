from PySide6.QtWidgets import QLabel
from PySide6.QtGui import QPainter, QLinearGradient, QFont, QFontMetrics, QColor, QPen, QBrush
from PySide6.QtCore import Qt


class GradientLabel(QLabel):
    def __init__(self, text: str, colors: list[str], parent=None):
        super().__init__(parent)
        self._text = text
        self._colors = colors
        self.setAttribute(Qt.WA_TranslucentBackground)

        font = QFont()
        font.setPointSize(16)
        font.setWeight(QFont.DemiBold)
        self.setFont(font)

        metrics = QFontMetrics(font)
        self.setFixedHeight(metrics.height() + 4)
        self.setMinimumWidth(metrics.horizontalAdvance(text) + 4)

    def setText(self, text: str):
        self._text = text
        metrics = QFontMetrics(self.font())
        self.setMinimumWidth(metrics.horizontalAdvance(text) + 4)
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setRenderHint(QPainter.TextAntialiasing)

        gradient = QLinearGradient(0, 0, self.width(), 0)
        step = 1.0 / max(1, len(self._colors) - 1)
        for i, color in enumerate(self._colors):
            gradient.setColorAt(min(1.0, i * step), QColor(color))

        painter.setPen(Qt.NoPen)
        painter.setBrush(gradient)
        painter.setFont(self.font())

        path_rect = self.rect()
        painter.save()
        painter.setPen(QPen(QBrush(gradient), 1))
        painter.drawText(path_rect, Qt.AlignVCenter | Qt.AlignLeft, self._text)
        painter.restore()
