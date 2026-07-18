import os
import sys
import tempfile
import unittest
from PIL import Image

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from models.image_item import ImageItem
from models.settings_model import CompressionSettings, PdfSettings
from services.compressor import Compressor
from services.pdf_builder import PdfBuilder
from services.image_loader import ImageLoader


class TestServices(unittest.TestCase):
    def setUp(self):
        self.tmp_dir = tempfile.mkdtemp()
        self.image_path = os.path.join(self.tmp_dir, "sample.png")
        Image.new("RGB", (400, 300), "red").save(self.image_path)

    def test_image_loader_loads_metadata(self):
        loader = ImageLoader(os.path.join(self.tmp_dir, "thumbs"))
        item = loader.load(self.image_path, 0)
        self.assertEqual(item.width, 400)
        self.assertEqual(item.height, 300)
        self.assertTrue(item.original_size > 0)

    def test_compressor_creates_output(self):
        loader = ImageLoader(os.path.join(self.tmp_dir, "thumbs"))
        item = loader.load(self.image_path, 0)
        compressor = Compressor(os.path.join(self.tmp_dir, "compressed"))
        settings = CompressionSettings(mode="Smart Compression", quality=80)
        result = compressor.compress(item, settings)
        self.assertTrue(os.path.exists(result.compressed_path))
        self.assertTrue(result.compressed_size > 0)

    def test_pdf_builder_creates_pdf(self):
        loader = ImageLoader(os.path.join(self.tmp_dir, "thumbs"))
        item = loader.load(self.image_path, 0)
        compressor = Compressor(os.path.join(self.tmp_dir, "compressed"))
        settings = CompressionSettings()
        item = compressor.compress(item, settings)

        pdf_settings = PdfSettings(
            output_name="test.pdf",
            output_dir=self.tmp_dir,
            page_size="A4",
        )
        builder = PdfBuilder()
        output_path = builder.build([item], pdf_settings)
        self.assertTrue(os.path.exists(output_path))

    def test_compressor_applies_crop_box(self):
        loader = ImageLoader(os.path.join(self.tmp_dir, "thumbs"))
        item = loader.load(self.image_path, 0)
        item.crop_box = (50, 50, 250, 200)
        compressor = Compressor(os.path.join(self.tmp_dir, "compressed_crop"))
        settings = CompressionSettings()
        result = compressor.compress(item, settings)

        with Image.open(result.compressed_path) as cropped:
            self.assertEqual(cropped.size, (200, 150))

    def test_pdf_builder_generates_preview_pages(self):
        loader = ImageLoader(os.path.join(self.tmp_dir, "thumbs"))
        item = loader.load(self.image_path, 0)
        compressor = Compressor(os.path.join(self.tmp_dir, "compressed"))
        settings = CompressionSettings()
        item = compressor.compress(item, settings)

        pdf_settings = PdfSettings(
            output_name="preview.pdf",
            output_dir=self.tmp_dir,
            page_size="A4",
        )
        builder = PdfBuilder()
        pages = builder.generate_preview_pages([item], pdf_settings)
        self.assertEqual(len(pages), 1)
        self.assertGreater(pages[0].width, 0)
        self.assertGreater(pages[0].height, 0)


if __name__ == "__main__":
    unittest.main()
