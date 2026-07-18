from dataclasses import dataclass, field


@dataclass
class CompressionSettings:
    mode: str = "Smart Compression"
    quality: int = 85
    keep_original_resolution: bool = True
    resolution_scale: int = 100


@dataclass
class PdfSettings:
    output_name: str = "Output.pdf"
    output_dir: str = ""
    page_size: str = "A4"
    orientation: str = "Auto"
    margin_mm: int = 10
    spacing_mm: int = 5
    images_per_page: int = 1
    alignment: str = "Center"
    pdf_quality: str = "High"
    title: str = ""
    author: str = ""
    subject: str = ""
    keywords: str = ""
    creator: str = "PixPDF Studio"
    password: str = ""
    allow_print: bool = True
    allow_copy: bool = True
    allow_edit: bool = False


@dataclass
class AppSettings:
    compression: CompressionSettings = field(default_factory=CompressionSettings)
    pdf: PdfSettings = field(default_factory=PdfSettings)
    theme: str = "Dark"
    accent_color: str = "#4C9EFF"
    last_directory: str = ""
