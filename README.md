# Music Downloader

> [!Caution]
> Illegal usage of this tool to download copyrighted material without permission may violate copyright laws. Please ensure you have the right to download the relevant content before using this tool. The developers are not responsible for any misuse of this software.

A simple command-line tool to download and apply metadata (such as titles, albums, artists, and album covers) to music from various online sources such as YouTube and SoundCloud. Currently, all downloads are in MP3 format and the available sources are limited to those provided by the excellent [yt-dlp](https://github.com/yt-dlp/yt-dlp) library.

## Usage

This tool uses the [uv](https://docs.astral.sh/uv/) Python package and project manager and can be run with the following command:

```bash
uv run download <URL1> <URL2> <URL3> ...
```

### Options

> [!NOTE]
> TODO

## Contributing

Pull requests are welcome! For major changes, please open an issue first to discuss what you would like to change.

### Code style

This project uses [Google's style guides](https://google.github.io/styleguide/) and uses [Black](https://black.readthedocs.io/en/stable/), [isort](https://pycqa.github.io/isort/), [Pylint](https://pylint.readthedocs.io/en/latest/), and [Prettier](https://prettier.io/) to enforce them. Other tools are however welcome!

#### Changes made to the Google Python Style Guide

In accordance with the license used by the [Google Python Style Guide](https://google.github.io/styleguide/pyguide.html) ([Apache License, Version 2.0](https://www.apache.org/licenses/LICENSE-2.0)), all changes made to [`.pylintrc`](.pylintrc) have to be documented. The following changes have been made:

* `max-line-length` has been changed from 80 to 88
