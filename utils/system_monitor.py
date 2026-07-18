import psutil
import os


class SystemMonitor:
    def __init__(self):
        self.process = psutil.Process(os.getpid())

    def cpu_percent(self) -> float:
        return psutil.cpu_percent(interval=None)

    def ram_usage_mb(self) -> float:
        return round(self.process.memory_info().rss / (1024 * 1024), 1)
