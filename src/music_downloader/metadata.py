import logging
import shutil
import subprocess
from pathlib import Path
from typing import Any, Callable, cast

from PIL import Image
from PIL.ImageFile import ImageFile

from music_downloader.core import Track


def apply_album_art_metadata(filepath: Path, album_art_filepath: Path) -> None:
    temp_filepath: Path = filepath.with_suffix(".temp" + filepath.suffix)

    # fmt: off
    cmd = [
        "ffmpeg",
        "-i", str(filepath),
        "-i", str(album_art_filepath),
        "-map", "0:a",  # Map audio from `filepath`
        "-map", "1:v",  # Map album art from `album_art_filepath`
        "-c:a", "copy",  # Copy audio stream without re-encoding
        "-c:v:1", "png",  # Encode image as png for cover art
        "-id3v2_version", "3",
        "-metadata:s:v", "comment=Cover (front)" ,
        temp_filepath,
    ]
    # fmt: on

    subprocess.run(cmd, check=True)
    shutil.move(temp_filepath, filepath)


def apply_text_metadata(filepath: Path, metadata: dict[str, str | Path | None]) -> None:
    temp_filepath: Path = filepath.with_suffix(".temp" + filepath.suffix)

    # fmt: off
    cmd = [
        "ffmpeg",
        "-i", str(filepath),
        "-c", "copy",  # Copy audio stream without of re-encoding
        "-b:a", "320k",  # Force audio bitrate
    ]
    # fmt: on
    for key, value in metadata.items():
        if value is not None:
            cmd += ["-metadata", f"{key}={value}"]
    cmd += [str(temp_filepath)]

    subprocess.run(cmd, check=True)
    shutil.move(temp_filepath, filepath)


def crop_album_art(filepath: Path) -> None:
    image: ImageFile = Image.open(filepath)
    width: int = image.size[0]
    height: int = image.size[1]
    cropped_width: int = min(width, height)

    left: int = (width - cropped_width) // 2
    top: int = (height - cropped_width) // 2
    right: int = (width + cropped_width) // 2
    bottom: int = (height + cropped_width) // 2

    cropped_image: Image.Image = image.crop((left, top, right, bottom))
    cropped_image.save(filepath)


def fit_album_art(filepath: Path) -> None:
    # Convert to RGBA to make transperency possible
    image: Image.Image = Image.open(filepath).convert("RGBA")
    width: int = image.size[0]
    height: int = image.size[1]
    expanded_width: int = max(width, height)

    left: int = (expanded_width - width) // 2
    top: int = (expanded_width - height) // 2

    fitted_image: Image.Image = Image.new(
        "RGBA", (expanded_width, expanded_width), color=(0, 0, 0, 0)
    )  # Create a fully transparent background
    fitted_image.paste(image, (left, top), image)
    fitted_image.save(filepath)


def adjust_album_art(filepath: Path, adjustment) -> None:
    adjustment_function_map: dict[str, Callable] = {
        "crop": crop_album_art,
        "fit": fit_album_art,
    }
    adjustment_function_map[adjustment](filepath)


def apply_metadata(track: Track, options: dict[str, Any]) -> None:
    """Apply metadata to a track using FFmpeg."""

    logging.info("[%s] Applying metadata to track...", track.url)
    filepath = cast(Path, track.filepath)
    metadata: dict[str, str | Path | None] = track.get_metadata()
    apply_text_metadata(filepath, metadata)
    logging.info("[%s] Applied text metadata to track", track.url)

    album_art_filepath = cast(Path, metadata["album_art"])
    adjust_album_art(album_art_filepath, options["album_art_adjustment"])
    logging.info(
        "[%s] Adjusted album art metadata with adjustment %s...",
        track.url,
        options["album_art_adjustment"],
    )
    logging.info("[%s] Applied album art metadata to track...", track.url)
