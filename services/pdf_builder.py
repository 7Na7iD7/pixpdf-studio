import os
import math
from typing import List, Callable, Optional
from PIL import Image
from models.image_item import ImageItem
from models.settings_model import PdfSettings

MM_TO_PT = 2.834645669

PAGE_SIZES_MM = {
    "A4": (210, 297),
    "A5": (148, 210),
    "Letter": (215.9, 279.4),
    "Legal": (215.9, 355.6),
}


class PdfBuilder:
    def build(
        self,
        items: List[ImageItem],
        settings: PdfSettings,
        progress_callback: Optional[Callable[[int, int], None]] = None,
    ) -> str:
        output_path = os.path.join(settings.output_dir, settings.output_name)
        page_w_mm, page_h_mm = self._resolve_page_size(items, settings)

        if settings.orientation == "Landscape" and page_w_mm < page_h_mm:
            page_w_mm, page_h_mm = page_h_mm, page_w_mm
        elif settings.orientation == "Portrait" and page_w_mm > page_h_mm:
            page_w_mm, page_h_mm = page_h_mm, page_w_mm

        dpi = self._quality_to_dpi(settings.pdf_quality)
        page_w_px = int(page_w_mm / 25.4 * dpi)
        page_h_px = int(page_h_mm / 25.4 * dpi)
        margin_px = int(settings.margin_mm / 25.4 * dpi)
        spacing_px = int(settings.spacing_mm / 25.4 * dpi)

        per_page = max(1, settings.images_per_page)
        cols = math.ceil(math.sqrt(per_page))
        rows = math.ceil(per_page / cols)

        pages = []
        total = len(items)
        for start in range(0, total, per_page):
            chunk = items[start:start + per_page]
            page = Image.new("RGB", (page_w_px, page_h_px), "white")
            usable_w = page_w_px - 2 * margin_px - (cols - 1) * spacing_px
            usable_h = page_h_px - 2 * margin_px - (rows - 1) * spacing_px
            cell_w = usable_w // cols
            cell_h = usable_h // rows

            for i, item in enumerate(chunk):
                r = i // cols
                c = i % cols
                x = margin_px + c * (cell_w + spacing_px)
                y = margin_px + r * (cell_h + spacing_px)
                source_path = item.compressed_path or item.path
                with Image.open(source_path) as im:
                    im = im.convert("RGB")
                    placed = self._place_image(im, cell_w, cell_h, settings.alignment)
                    offset_x = x + (cell_w - placed.width) // 2
                    offset_y = y + (cell_h - placed.height) // 2
                    page.paste(placed, (offset_x, offset_y))

                if progress_callback:
                    progress_callback(start + i + 1, total)

            pages.append(page)

        if not pages:
            raise ValueError("No images to build PDF")

        os.makedirs(settings.output_dir, exist_ok=True)
        first, rest = pages[0], pages[1:]
        first.save(output_path, "PDF", save_all=True, append_images=rest, resolution=dpi)
        return output_path

    def _resolve_page_size(self, items: List[ImageItem], settings: PdfSettings):
        if settings.page_size == "Original Size" and items:
            with Image.open(items[0].compressed_path or items[0].path) as im:
                w_px, h_px = im.size
                dpi = im.info.get("dpi", (96, 96))[0] or 96
                return w_px / dpi * 25.4, h_px / dpi * 25.4
        return PAGE_SIZES_MM.get(settings.page_size, PAGE_SIZES_MM["A4"])

    def _quality_to_dpi(self, quality: str) -> int:
        mapping = {
            "Maximum": 300,
            "High": 200,
            "Medium": 150,
            "Small Size": 96,
        }
        return mapping.get(quality, 150)

    def _place_image(self, im: Image.Image, cell_w: int, cell_h: int, alignment: str) -> Image.Image:
        if alignment == "Stretch" or alignment == "Fill":
            return im.resize((cell_w, cell_h), Image.LANCZOS)

        ratio = min(cell_w / im.width, cell_h / im.height)
        if alignment == "Fit":
            new_w = max(int(im.width * ratio), 1)
            new_h = max(int(im.height * ratio), 1)
            return im.resize((new_w, new_h), Image.LANCZOS)

        new_w = max(int(im.width * ratio), 1)
        new_h = max(int(im.height * ratio), 1)
        return im.resize((new_w, new_h), Image.LANCZOS)
