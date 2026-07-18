from dataclasses import dataclass
from pathlib import Path
from typing import Optional


@dataclass
class ImageItem:
    path: str
    original_size: int = 0
    compressed_size: int = 0
    width: int = 0
    height: int = 0
    format: str = ""
    thumbnail_path: Optional[str] = None
    compressed_path: Optional[str] = None
    order_index: int = 0
    rotation: int = 0
    grayscale: bool = False
    flipped_h: bool = False
    flipped_v: bool = False

    @property
    def name(self) -> str:
        return Path(self.path).name

    @property
    def reduction_percent(self) -> float:
        if self.original_size == 0 or self.compressed_size == 0:
            return 0.0
        return round((1 - (self.compressed_size / self.original_size)) * 100, 1)
