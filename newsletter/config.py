"""Loads .env secrets, sources.yaml, and profile.json from the project root."""
from __future__ import annotations

import json
import os
from pathlib import Path

import yaml
from dotenv import load_dotenv

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DB_PATH = PROJECT_ROOT / "newsletter.db"
OUT_DIR = PROJECT_ROOT / "out"
TEMPLATES_DIR = Path(__file__).resolve().parent / "templates"

load_dotenv(PROJECT_ROOT / ".env")


def load_sources() -> dict:
    with open(PROJECT_ROOT / "sources.yaml", encoding="utf-8") as f:
        return yaml.safe_load(f)


def load_profile() -> dict:
    with open(PROJECT_ROOT / "profile.json", encoding="utf-8") as f:
        return json.load(f)


def env(name: str, default: str | None = None) -> str:
    value = os.environ.get(name, default)
    if value is None:
        raise RuntimeError(
            f"Missing required environment variable {name}. "
            f"Copy .env.example to .env and fill it in."
        )
    return value
