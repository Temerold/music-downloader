import re
from urllib.parse import urlparse

from music_downloader.sources.core import Source, UnknownSourceError
from music_downloader.sources.yt_dlp import YtDlpSource
from music_downloader.utils import sanitize_url

SOURCE_MAP: dict[str, Source] = {
    # Default source if otherwise not explicitly defined. yt-dlp handles pretty much
    # everything.
    "*": YtDlpSource(),
    "youtube.com": YtDlpSource(),
    "music.youtube.com": YtDlpSource(),
    "youtu.be": YtDlpSource(),
    "soundcloud.com": YtDlpSource(),
}


def identify_source(url: str) -> Source:
    """Identifies track source based on the given URL.

    Args:
        url (str): URL to identify source with.
    Returns:
        Source: Corresponding `Source` object for `url`.
    Raises:
        UnknownSourceError: URL is empty or the source isn't found in source map.
    """

    url = sanitize_url(url)
    if not url:
        raise UnknownSourceError("Source URL empty")

    # Ensure `url` has a scheme for proper parsing. HTTP was chosen arbitrarily and will
    # not affect the definition of `url_netloc`.
    if not re.search(".*//", url):
        url = f"http://{url}"

    url_netloc: str = urlparse(url).netloc.lower().lstrip("www.")

    return SOURCE_MAP.get(url_netloc, SOURCE_MAP["*"])
