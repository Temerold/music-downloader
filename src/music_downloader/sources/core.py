from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any

from music_downloader.core import Track


class UnknownSourceError(Exception):
    """Track source identification failed."""


class Source(ABC):
    @abstractmethod
    def get_metadata(self, track: Track) -> dict[str, Any]:
        raise NotImplementedError

    @abstractmethod
    def save_track(self, track: Track, options: dict[str, Any]) -> Path:
        raise NotImplementedError
