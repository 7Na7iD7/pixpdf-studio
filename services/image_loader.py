import os
import hashlib
from pathlib import Path
from typing import List
from PIL import Image
from models.image_item import ImageItem

SUPPORTED_EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp", ".bmp", ".tiff", ".tif"}


class ImageLoader:
    def __init__(self, thumbnail_dir: str):
        self.thumbnail_dir = thumbnail_dir
        os.makedirs(self.thumbnail_dir, exist_ok=True)

    def is_supported(self, path: str) -> bool:
        return Path(path).suffix.lower() in SUPPORTED_EXTENSIONS

    def scan_folder(self, folder: str) -> List[str]:
        result = []
        for root, _, files in os.walk(folder):
            for f in files:
                full_path = os.path.join(root, f)
                if self.is_supported(full_path):
                    result.append(full_path)
        return result

    def load(self, path: str, index: int) -> ImageItem:
        size = os.path.getsize(path)
        with Image.open(path) as img:
            width, height = img.size
            fmt = img.format or Path(path).suffix.replace(".", "").upper()
        item = ImageItem(
            path=path,
            original_size=size,
            width=width,
            height=height,
            format=fmt,
            order_index=index,
        )
        item.thumbnail_path = self._make_thumbnail(path)
        return item

    def _make_thumbnail(self, path: str) -> str:
        digest = hashlib.md5(path.encode("utf-8")).hexdigest()
        thumb_path = os.path.join(self.thumbnail_dir, f"{digest}.png")
        if os.path.exists(thumb_path):
            return thumb_path
        with Image.open(path) as img:
            img = img.convert("RGB")
            img.thumbnail((200, 200))
            img.save(thumb_path, "PNG")
        return thumb_path

    def find_duplicates(self, items: List[ImageItem]) -> List[List[ImageItem]]:
        hashes = {}
        for item in items:
            h = self._file_hash(item.path)
            hashes.setdefault(h, []).append(item)
        return [group for group in hashes.values() if len(group) > 1]

    def _file_hash(self, path: str) -> str:
        hasher = hashlib.md5()
        with open(path, "rb") as f:
            while chunk := f.read(65536):
                hasher.update(chunk)
        return hasher.hexdigest()
