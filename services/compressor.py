import os
from pathlib import Path
from PIL import Image, ImageOps
from models.image_item import ImageItem
from models.settings_model import CompressionSettings

QUALITY_PRESETS = {
    "Lossless": 100,
    "Smart Compression": 85,
    "High Quality": 92,
    "Maximum Compression": 65,
}


class Compressor:
    def __init__(self, output_dir: str):
        self.output_dir = output_dir
        os.makedirs(self.output_dir, exist_ok=True)

    def compress(self, item: ImageItem, settings: CompressionSettings) -> ImageItem:
        with Image.open(item.path) as img:
            img = ImageOps.exif_transpose(img)

            if item.rotation:
                img = img.rotate(-item.rotation, expand=True)
            if item.flipped_h:
                img = ImageOps.mirror(img)
            if item.flipped_v:
                img = ImageOps.flip(img)
            if item.grayscale:
                img = ImageOps.grayscale(img)

            if img.mode in ("RGBA", "P") and settings.mode != "Lossless":
                img = img.convert("RGB")

            if not settings.keep_original_resolution and settings.resolution_scale < 100:
                new_w = int(img.width * settings.resolution_scale / 100)
                new_h = int(img.height * settings.resolution_scale / 100)
                img = img.resize((max(new_w, 1), max(new_h, 1)), Image.LANCZOS)

            quality = settings.quality
            out_name = f"{Path(item.path).stem}_compressed.jpg"
            out_path = os.path.join(self.output_dir, out_name)

            save_kwargs = {"quality": quality, "optimize": True}
            if settings.mode == "Lossless":
                if img.mode != "RGB":
                    img = img.convert("RGB")
                img.save(out_path, "PNG".replace("PNG", "JPEG"), quality=100, optimize=True)
            else:
                img.save(out_path, "JPEG", **save_kwargs)

        item.compressed_path = out_path
        item.compressed_size = os.path.getsize(out_path)
        return item

    def resolve_quality(self, mode: str) -> int:
        return QUALITY_PRESETS.get(mode, 85)
