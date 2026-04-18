"""Paths and static app configuration shared by UI modules."""

from pathlib import Path

PACKAGE_DIR = Path(__file__).resolve().parent
PROJECT_DIR = PACKAGE_DIR.parent

UI_CACHE_FILE = PROJECT_DIR / "ui_translations_cache.json"

PAGE_TITLE = "AI Courtroom Battle Simulator"
PAGE_ICON = "⚖️"
