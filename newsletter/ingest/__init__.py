"""Adapter registry: one entry per source type enabled in sources.yaml."""
from __future__ import annotations

from .arxiv import ArxivAdapter
from .base import SourceAdapter
from .hackernews import HackerNewsAdapter
from .rss import RssAdapter


def build_adapters(sources_config: dict) -> list[SourceAdapter]:
    adapters: list[SourceAdapter] = []
    if "rss" in sources_config:
        adapters.append(RssAdapter(sources_config["rss"]))
    if "hackernews" in sources_config:
        adapters.append(HackerNewsAdapter(sources_config["hackernews"]))
    if "arxiv" in sources_config:
        adapters.append(ArxivAdapter(sources_config["arxiv"]))
    return adapters
