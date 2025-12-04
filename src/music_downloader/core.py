from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from music_downloader.sources.core import Source


class Track:
    """A music track with optional metadata and at minimum a URL.

    Args:
        url (str): Track URL.
        source (Source | None, optional): What service the URL points to represented as
            a `Source` object. Defaults to None.
        raw_source_metadata (dict[str, Any] | None, optional): Raw metadata as returned
            by the source. Defaults to None.
        filepath (Path | None, optional): Where the track is stored locally. Defaults to
            None.
        title (str | None, optional): Track title. Defaults to None.
        artist (str | None, optional): Track artist. Defaults to None.
        album (str | None, optional): Track album. Defaults to None.
        album_artist (str | None, optional): Track album artist. Defaults to None.
        album_art (Path | None, optional): Track album art filepath. Default to None.
    """

    def __init__(
        self,
        url: str,
        source: Source | None = None,
        raw_source_metadata: dict[str, Any] | None = None,
    ) -> None:
        self.url: str = url
        self.source: Source | None = source
        self.raw_source_metadata: dict[str, Any] | None = raw_source_metadata
        self.filepath: Path | None = None

        self.metadata: dict[str, str | Path | None] = {
            "album": None,
            "album_artist": None,
            "album_art": None,
            "artist": None,
            "disc": None,
            "genre": None,
            "synopsis": None,
            "title": None,
            "track": None,
            "date": None,
        }

    def __str__(self) -> str:
        """Returns a string representation of the track, including title, artist.

        Returns:
            str: String representation of the track, including title, artist.
        """

        return f"{self.metadata["artist"]} – {self.metadata["title"]}"

    def get_metadata(self) -> dict[str, str | Path | None]:
        """Returns a dictionary of the track's metadata.

        Returns:
            dict[str, str]: A dictionary containing the track's metadata
                attributes and their corresponding values if they're not `None`.
        """

        return {key: value for key, value in self.metadata.items() if value is not None}
