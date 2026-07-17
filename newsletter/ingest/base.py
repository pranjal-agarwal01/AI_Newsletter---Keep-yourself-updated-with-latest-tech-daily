"""Common interface every source adapter implements."""
from __future__ import annotations

from typing import Protocol

from ..models import RawItem


class SourceAdapter(Protocol):
    name: str

    def fetch(self) -> list[RawItem]:
        """Return the latest items from this source. Must not raise on
        per-item problems — skip bad entries and return what parsed."""
        ...
