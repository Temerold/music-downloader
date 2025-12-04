import logging
import os
import shutil
import sys
from pathlib import Path
from typing import Any, cast

import click
from PIL import Image

from music_downloader.core import Track
from music_downloader.logging.logging import excepthook
from music_downloader.metadata import apply_metadata
from music_downloader.sources.core import Source
from music_downloader.sources.registry import identify_source

logging.basicConfig(
    filename="logs.log",
    encoding="utf-8",
    datefmt="%Y-%m-%d %H:%M:%S",
    format="%(asctime)s:%(levelname)s:%(message)s",
    level=logging.INFO,
)
sys.excepthook = lambda type, value, traceback: excepthook(
    logging.getLogger(__name__), type, value, traceback
)


class MetadataRetrievalError(Exception):
    """Track metadata retrieval failed and returned no or unusable data."""


def save_track_album_art(track: Track) -> Path:
    logging.info("[%s] Saving track album art...]", track.url)
    temp_filepath = cast(Path, track.metadata["album_art"])
    filepath = cast(Path, track.filepath).parent / "cover.png"
    image = Image.open(temp_filepath)
    image.save(filepath)
    shutil.move(temp_filepath, filepath)
    logging.info("[%s] Saved track album art as %s", track.url, filepath)
    return filepath


def process_track(url: str, options: dict[str, Any]) -> None:
    logging.info("[%s] Processing URL...", url)
    track: Track = get_track_object_from_url(url)
    source: Source = cast(Source, track.source)

    logging.info("[%s] Downloading and saving track...]", url)
    track.filepath = source.save_track(track, options)
    logging.info("[%s] Saved file as %s]", url, track.filepath)

    track.metadata["album_art"] = save_track_album_art(track)
    apply_metadata(track, options)


def get_track_object_from_url(url: str) -> Track:
    """Returns a `Track` object for the given URL populated with metadata.

    Args:
        url (str): URL of the track to process.
    Returns:
        Track: A `Track` object populated with metadata such as title and artist.
    Raises:
        UnknownSourceError: The URL is empty or the source isn't found in the source
            map.
        MetadataRetrievalError: Metadata retrieval failed and returned no or unusable
            data.
    """

    source: Source = identify_source(url)
    track = Track(url=url, source=source)

    try:
        track.raw_source_metadata = source.get_metadata(track)
        for key in track.metadata.keys():
            if key in track.raw_source_metadata.keys():
                track.metadata[key] = track.raw_source_metadata[key]
    except Exception as exc:
        raise MetadataRetrievalError(
            f"Metadata retrieval failed for URL: {url}"
        ) from exc

    logging.info("[%s] Identified URL as %s", url, track)
    return track


@click.command()
@click.argument("urls", nargs=-1)
@click.option("--album_art_adjustment", "-c", default="fit", type=str)
@click.option(
    "--output_template",
    "-o",
    default=f"{Path(os.environ["USERPROFILE"]) / "Music"}\\%(artist)s - %(title)s\\%(title)s.%(ext)s",
    type=str,
)
def download(urls: tuple, album_art_adjustment: str, output_template: str) -> None:
    options: dict[str, Any] = {
        "album_art_adjustment": album_art_adjustment,
        "output_template": output_template,
    }
    for url in urls:
        try:
            process_track(url, options)
        except Exception as exc:
            logging.error(
                "Exception encountered when processing URL %s.", url, exc_info=exc
            )
        else:
            logging.info("[%s] Successfully processed track", url)


if __name__ == "__main__":
    download(("https://www.youtube.com/watch?v=dQw4w9WgXcQ",))
