from PySide6.QtWidgets import (
    QFrame, QVBoxLayout, QHBoxLayout, QLabel, QComboBox, QSlider, QCheckBox
)
from PySide6.QtCore import Qt, Signal
from models.settings_model import CompressionSettings


class CompressionPanel(QFrame):
    settings_changed = Signal()

    def __init__(self, settings: CompressionSettings, parent=None):
        super().__init__(parent)
        self.setObjectName("Card")
        self.settings = settings

        layout = QVBoxLayout(self)
        layout.setContentsMargins(16, 16, 16, 16)
        layout.setSpacing(10)

        title = QLabel("فشرده‌سازی هوشمند")
        title.setObjectName("TitleLabel")
        layout.addWidget(title)

        self.mode_combo = QComboBox()
        self.mode_combo.addItems(["Lossless", "Smart Compression", "High Quality", "Maximum Compression"])
        self.mode_combo.setCurrentText(settings.mode)
        self.mode_combo.currentTextChanged.connect(self._on_mode_changed)
        layout.addWidget(self.mode_combo)

        quality_row = QHBoxLayout()
        quality_label = QLabel("کیفیت")
        self.quality_value_label = QLabel(f"{settings.quality}%")
        quality_row.addWidget(quality_label)
        quality_row.addStretch()
        quality_row.addWidget(self.quality_value_label)
        layout.addLayout(quality_row)

        self.quality_slider = QSlider(Qt.Horizontal)
        self.quality_slider.setRange(50, 100)
        self.quality_slider.setSingleStep(5)
        self.quality_slider.setValue(settings.quality)
        self.quality_slider.valueChanged.connect(self._on_quality_changed)
        layout.addWidget(self.quality_slider)

        self.keep_resolution_checkbox = QCheckBox("حفظ رزولوشن اصلی")
        self.keep_resolution_checkbox.setChecked(settings.keep_original_resolution)
        self.keep_resolution_checkbox.stateChanged.connect(self._on_keep_resolution_changed)
        layout.addWidget(self.keep_resolution_checkbox)

        resolution_row = QHBoxLayout()
        resolution_label = QLabel("مقیاس رزولوشن")
        self.resolution_value_label = QLabel(f"{settings.resolution_scale}%")
        resolution_row.addWidget(resolution_label)
        resolution_row.addStretch()
        resolution_row.addWidget(self.resolution_value_label)
        layout.addLayout(resolution_row)

        self.resolution_slider = QSlider(Qt.Horizontal)
        self.resolution_slider.setRange(25, 100)
        self.resolution_slider.setSingleStep(5)
        self.resolution_slider.setValue(settings.resolution_scale)
        self.resolution_slider.setEnabled(not settings.keep_original_resolution)
        self.resolution_slider.valueChanged.connect(self._on_resolution_changed)
        layout.addWidget(self.resolution_slider)

    def _on_mode_changed(self, value: str):
        self.settings.mode = value
        self.settings_changed.emit()

    def _on_quality_changed(self, value: int):
        self.settings.quality = value
        self.quality_value_label.setText(f"{value}%")
        self.settings_changed.emit()

    def _on_keep_resolution_changed(self, state):
        checked = state == Qt.Checked.value if hasattr(Qt.Checked, "value") else bool(state)
        self.settings.keep_original_resolution = checked
        self.resolution_slider.setEnabled(not checked)
        self.settings_changed.emit()

    def _on_resolution_changed(self, value: int):
        self.settings.resolution_scale = value
        self.resolution_value_label.setText(f"{value}%")
        self.settings_changed.emit()
