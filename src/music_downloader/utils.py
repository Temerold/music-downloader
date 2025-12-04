def sanitize_url(url: str) -> str:
    """Removes all whitespace characters from a URL string.

    Args:
        url (str): URL string to sanitize.

    Returns:
        str: Sanitized URL string with all whitespace removed.
    """

    return "".join(url.split())
