from PySide6.QtWidgets import QWidget, QHBoxLayout, QLabel, QProgressBar
from PySide6.QtCore import QTimer
from utils.system_monitor import SystemMonitor


class StatusPanel(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.monitor = SystemMonitor()

        layout = QHBoxLayout(self)
        layout.setContentsMargins(8, 4, 8, 4)

        self.progress_bar = QProgressBar()
        self.progress_bar.setFixedWidth(220)
        self.progress_bar.setValue(0)

        self.status_label = QLabel("آماده")
        self.cpu_label = QLabel("CPU: 0%")
        self.ram_label = QLabel("RAM: 0 MB")

        layout.addWidget(self.status_label)
        layout.addStretch()
        layout.addWidget(self.progress_bar)
        layout.addWidget(self.cpu_label)
        layout.addWidget(self.ram_label)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self._update_stats)
        self.timer.start(1500)

    def _update_stats(self):
        self.cpu_label.setText(f"CPU: {self.monitor.cpu_percent():.0f}%")
        self.ram_label.setText(f"RAM: {self.monitor.ram_usage_mb():.0f} MB")

    def set_progress(self, current: int, total: int):
        percent = int((current / total) * 100) if total else 0
        self.progress_bar.setValue(percent)

    def set_status(self, text: str):
        self.status_label.setText(text)
