import json
import os
from dataclasses import asdict
from models.settings_model import AppSettings, CompressionSettings, PdfSettings

CONFIG_DIR = os.path.join(os.path.expanduser("~"), ".pixpdfstudio")
CONFIG_PATH = os.path.join(CONFIG_DIR, "settings.json")


class SettingsService:
    def load(self) -> AppSettings:
        if not os.path.exists(CONFIG_PATH):
            return AppSettings()
        try:
            with open(CONFIG_PATH, "r", encoding="utf-8") as f:
                data = json.load(f)
            settings = AppSettings()
            settings.compression = CompressionSettings(**data.get("compression", {}))
            settings.pdf = PdfSettings(**data.get("pdf", {}))
            settings.theme = data.get("theme", "Dark")
            settings.accent_color = data.get("accent_color", "#4C9EFF")
            settings.last_directory = data.get("last_directory", "")
            return settings
        except Exception:
            return AppSettings()

    def save(self, settings: AppSettings):
        os.makedirs(CONFIG_DIR, exist_ok=True)
        data = {
            "compression": asdict(settings.compression),
            "pdf": asdict(settings.pdf),
            "theme": settings.theme,
            "accent_color": settings.accent_color,
            "last_directory": settings.last_directory,
        }
        with open(CONFIG_PATH, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
