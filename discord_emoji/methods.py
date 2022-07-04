from typing import Optional

from .table import (
    DISCORD_TO_UNICODE,
    TONE_TO_UNICODE,
    UNICODE_TO_DISCORD,
    UNICODE_TO_TONE,
)


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
        unicode_bytes = _add_tone_marker_to_unicode(real_name)
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

    names = unicode_to_all_names(emoji, put_colons)
    if not names:
        return None
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

    # Remove variation bytes on single emojis (without zero-width joiner)
    if b"\xe2\x80\x8d" not in unicode_bytes:
        unicode_bytes = unicode_bytes.replace(b"\xef\xb8\x8f", b"")
        unicode_bytes = unicode_bytes.replace(b"\xef\xb8\x8f", b"")

    names = UNICODE_TO_DISCORD.get(unicode_bytes)
    if not names:
        names = _add_tone_marker_to_names(emoji)
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


def _add_tone_marker_to_unicode(name: str) -> Optional[bytes]:
    """
    Check emoji name for tone marker, then add to emoji unicode bytes.
    """

    name_words = name.split("_")
    if len(name_words) == 0:
        return None
    # Tone marker should be last word in emoji name
    emoji_tone = TONE_TO_UNICODE.get(name_words.pop())
    if not emoji_tone:
        return None
    # Get the default emoji name without tone marker
    name = "_".join(name_words)
    unicode_bytes = DISCORD_TO_UNICODE.get(name)
    if not unicode_bytes:
        return None
    # Tone marker unicode should go before first zero-width separator
    # if it exists in the unicode emoji
    first_sep = unicode_bytes.find(b"\xe2\x80\x8d")
    if first_sep < 0:
        unicode_bytes += emoji_tone
    else:
        unicode_bytes = (
            unicode_bytes[:first_sep] + emoji_tone + unicode_bytes[first_sep:]
        )
    return unicode_bytes


def _add_tone_marker_to_names(emoji: str) -> Optional[list[str]]:
    """
    Check emoji unicode for tone marker, then add to emoji names.
    """

    if len(emoji) == 1:
        return None
    # Check for tone marker in 2nd unicode character
    emoji_tone = UNICODE_TO_TONE.get(emoji[1].encode("utf-8"))
    if not emoji_tone:
        return None
    # Get emoji unicode without tone marker
    emoji = emoji[:1] + emoji[2:]
    unicode_bytes = emoji.encode("utf-8")
    names = UNICODE_TO_DISCORD.get(unicode_bytes)
    if not names:
        return None
    # Add tone marker as last word in emoji names
    return [f"{name}_{emoji_tone}" for name in names]
