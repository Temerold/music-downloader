from datetime import datetime
from pathlib import Path
from typing import Any, cast
from urllib.request import urlretrieve

import yt_dlp

from music_downloader.core import Track
from music_downloader.sources.core import Source

"""
FFmpeg-recognized tags used as `dict` keys are found at
https://wiki.multimedia.cx/index.php/FFmpeg_Metadata

Values of type `tuple[Any, Any]`: (yt_dlp key, default value if key not found)
Values of type `Any`: static value not dependent on yt_dlp metadata
"""
TRACK_METADATA_ATTRIBUTE_MAP: dict[str, tuple[Any, Any] | Any] = {
    "artist": ("uploader", None),
    "album": ("title", None),
    "album_artist": ("uploader", None),
    # "genre": ("categories", None),
    "date": ("upload_date", None),
    # "synopsis": ("description", None),
    "title": ("title", None),
    "track": "1/1",  # Handle it as a single
    "disc": "1/1",  # Handle it as a single
}


class YtDlpSource(Source):
    def get_metadata(self, track) -> dict[str, Any]:
        return get_metadata(track)

    def save_track(self, track, options: dict[str, Any]) -> Path:
        return save_track(track, options)


def ffmpeg_from_yt_dlp_keys(metadata: dict[str, Any]) -> dict[str, Any]:
    metadata = metadata.copy()
    for ffmpeg_key, yt_dlp_value in TRACK_METADATA_ATTRIBUTE_MAP.items():
        if not isinstance(yt_dlp_value, tuple):
            metadata[ffmpeg_key] = yt_dlp_value
            continue
        if yt_dlp_value[0] in metadata:
            metadata[ffmpeg_key] = metadata[yt_dlp_value[0]]

    return metadata


def get_metadata(track: Track) -> dict[str, Any]:
    with yt_dlp.YoutubeDL() as ydl:
        metadata: dict[str, Any] = cast(
            dict, ydl.extract_info(track.url, download=False)
        )
    metadata["album_art"] = save_temp_album_art(metadata["thumbnail"])
    metadata["date"] = format_date(metadata["upload_date"])

    return ffmpeg_from_yt_dlp_keys(metadata)


def format_date(yyyymmdd) -> str:
    return datetime.strptime(yyyymmdd, "%Y%m%d").strftime("%Y-%m-%d")


def remap_template_keys(template: str) -> str:
    yt_dlp_template: str = template
    for ffmpeg_attribute, yt_dlp_attribute in TRACK_METADATA_ATTRIBUTE_MAP.items():
        if isinstance(yt_dlp_attribute, tuple):
            yt_dlp_attribute: Any = yt_dlp_attribute[0]
        yt_dlp_template = yt_dlp_template.replace(
            f"%({ffmpeg_attribute})s", f"%({yt_dlp_attribute})s"
        )

    return yt_dlp_template


def save_temp_album_art(url: str) -> Path:
    return Path(urlretrieve(url)[0])


def save_track(track: Track, options: dict[str, Any]) -> Path:
    yt_dlp_output_template: str = remap_template_keys(options["output_template"])

    ydl_opts: dict[str, str | Any] = {
        "format": "bestaudio",
        "outtmpl": yt_dlp_output_template,
        "noplaylist": True,
        "postprocessors": [
            {
                "key": "FFmpegExtractAudio",
                "preferredcodec": "mp3",
                "preferredquality": "192",
            }
        ],
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([track.url])

        info_dict: dict[str, Any] = cast(
            dict, ydl.extract_info(track.url, download=True)
        )
        try:
            return Path(info_dict["requested_downloads"][0]["filepath"])
        except (KeyError, IndexError) as exc:
            raise KeyError(
                f"Could not determine filepath of downloaded track: {track}"
            ) from exc
