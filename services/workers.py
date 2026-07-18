from PySide6.QtCore import QObject, QRunnable, Signal, Slot
from models.image_item import ImageItem
from models.settings_model import CompressionSettings, PdfSettings
from services.compressor import Compressor
from services.pdf_builder import PdfBuilder
from services.metadata import MetadataService


class WorkerSignals(QObject):
    item_compressed = Signal(object)
    progress = Signal(int, int)
    finished = Signal()
    error = Signal(str)
    pdf_finished = Signal(str)


class CompressionWorker(QRunnable):
    def __init__(self, items: list[ImageItem], settings: CompressionSettings, output_dir: str):
        super().__init__()
        self.items = items
        self.settings = settings
        self.output_dir = output_dir
        self.signals = WorkerSignals()
        self._cancelled = False
        self._paused = False

    def cancel(self):
        self._cancelled = True

    def pause(self):
        self._paused = True

    def resume(self):
        self._paused = False

    @Slot()
    def run(self):
        compressor = Compressor(self.output_dir)
        total = len(self.items)
        try:
            for index, item in enumerate(self.items):
                while self._paused and not self._cancelled:
                    pass
                if self._cancelled:
                    break
                compressed = compressor.compress(item, self.settings)
                self.signals.item_compressed.emit(compressed)
                self.signals.progress.emit(index + 1, total)
            self.signals.finished.emit()
        except Exception as e:
            self.signals.error.emit(str(e))


class PdfBuildWorker(QRunnable):
    def __init__(self, items: list[ImageItem], settings: PdfSettings):
        super().__init__()
        self.items = items
        self.settings = settings
        self.signals = WorkerSignals()

    @Slot()
    def run(self):
        try:
            builder = PdfBuilder()
            output_path = builder.build(
                self.items,
                self.settings,
                progress_callback=lambda cur, tot: self.signals.progress.emit(cur, tot),
            )
            MetadataService().apply(output_path, self.settings)
            self.signals.pdf_finished.emit(output_path)
        except Exception as e:
            self.signals.error.emit(str(e))
