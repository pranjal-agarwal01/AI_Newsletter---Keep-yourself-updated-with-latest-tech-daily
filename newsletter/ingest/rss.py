"""RSS/Atom adapter: pulls the newest entries from configured blog feeds."""
from __future__ import annotations

import logging
import re
import time
from datetime import datetime, timezone

import feedparser

from ..models import RawItem

log = logging.getLogger(__name__)

TAG_RE = re.compile(r"<[^>]+>")


def _strip_html(text: str) -> str:
    return TAG_RE.sub(" ", text or "").strip()


def _entry_datetime(entry) -> datetime | None:
    parsed = entry.get("published_parsed") or entry.get("updated_parsed")
    if not parsed:
        return None
    return datetime.fromtimestamp(time.mktime(parsed), tz=timezone.utc)


class RssAdapter:
    name = "rss"

    def __init__(self, config: dict):
        self.feeds = config.get("feeds", [])
        self.max_items_per_feed = config.get("max_items_per_feed", 15)

    def fetch(self) -> list[RawItem]:
        items: list[RawItem] = []
        for feed in self.feeds:
            try:
                parsed = feedparser.parse(feed["url"])
                for entry in parsed.entries[: self.max_items_per_feed]:
                    url = entry.get("link")
                    title = entry.get("title", "").strip()
                    if not url or not title:
                        continue
                    items.append(
                        RawItem(
                            source=feed["name"],
                            title=title,
                            url=url,
                            published_at=_entry_datetime(entry),
                            raw_text=_strip_html(entry.get("summary", ""))[:4000],
                        )
                    )
                log.info("rss: %s -> %d entries", feed["name"], len(parsed.entries[: self.max_items_per_feed]))
            except Exception:
                log.exception("rss: feed failed, skipping: %s", feed.get("url"))
        return items
