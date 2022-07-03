from typing import Optional

from .table import DISCORD_TO_UNICODE, UNICODE_TO_DISCORD


def name_to_unicode(name: str) -> Optional[str]:
    """
    Get unicode characters from discord emoji name.

    Parameters
    ----------
    name : str
        Name of the emoji to get.
        `:` will be ignored.

    Returns
    -------
    Unicode for the found emoji.
    Returns None, if not found.
    """

    real_name = name.strip(":")
    unicode_bytes = DISCORD_TO_UNICODE.get(real_name)
    if not unicode_bytes:
        return None
    return unicode_bytes.decode("utf-8")


def unicode_to_name(emoji: str, put_colons: bool = False) -> Optional[str]:
    """
    Get discord emoji name from unicode characters.

    Parameters
    ----------
    emoji : str
        Emoji to get name.
    put_colons : bool, optional
        Whether put colons to name.

    Returns
    -------
    The found emoji's name on Discord.
    Returns None, if not found.
    """

    unicode_bytes = emoji.encode("utf-8")
    names = UNICODE_TO_DISCORD.get(unicode_bytes)
    if not names:
        return None
    if put_colons:
        return f":{names[0]}:"
    return names[0]


def unicode_to_all_names(emoji: str, put_colons: bool = False) -> Optional[list[str]]:
    """
    Get list of discord emoji names from unicode characters.

    Parameters
    ----------
    emoji : str
        Emoji to get names.
    put_colons : bool, optional
        Whether put colons to names.

    Returns
    -------
    The found emoji's names on Discord.
    Returns None, if not found.
    """

    unicode_bytes = emoji.encode("utf-8")
    names = UNICODE_TO_DISCORD.get(unicode_bytes)
    if not names:
        return None
    if put_colons:
        names = [f":{n}:" for n in names]
    return names


def unicode_to_image(emoji: str) -> Optional[str]:
    """
    Get URL to emoji image from unicode characters.

    Parameters
    ----------
    emoji : str
        Emoji to get image URL.

    Returns
    -------
    URL to emoji image.
    Returns None, if not found.
    """

    if not unicode_to_name(emoji):
        return None
    hex_words = [hex(ord(x))[2:] for x in emoji]
    if "200d" not in hex_words:
        hex_words = [x for x in hex_words if x != "fe0f"]
    return (
        "https://raw.githubusercontent.com/twitter/twemoji/master/assets/72x72/%s.png"
        % ("-".join(hex_words),)
    )


def name_to_image(name: str) -> Optional[str]:
    """
    Get URL to emoji image from discord emoji name.

    Parameters
    ----------
    name : str
        Name of the emoji to get.
        `:` will be ignored.

    Returns
    -------
    URL to emoji image.
    Returns None, if not found.
    """

    emoji = name_to_unicode(name)
    if not emoji:
        return None
    return unicode_to_image(emoji)
