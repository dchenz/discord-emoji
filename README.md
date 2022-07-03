# discord-emoji
[![PyPI](https://img.shields.io/pypi/v/discord-emoji)](https://pypi.org/project/discord-emoji)
[![PyPI - Downloads](https://img.shields.io/badge/dynamic/json?label=downloads&query=%24.total_downloads&url=https%3A%2F%2Fapi.pepy.tech%2Fapi%2Fprojects%2Fdiscord-emoji)](https://pepy.tech/project/discord-emoji/)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

This library converts between unicode emojis and their Discord names. It also provides URLs to [Twemoji](https://github.com/twitter/twemoji) image assets used by Discord.

## Usage

```python
>>> import discord_emoji
>>> discord_emoji.name_to_unicode("thinking")
'🤔'
>>> discord_emoji.name_to_unicode(":thinking:")
'🤔'
>>> discord_emoji.unicode_to_name("🤔")
'thinking'
>>> discord_emoji.unicode_to_name("🤔", put_colons=True)
':thinking:'
>>> discord_emoji.unicode_to_all_names("🤔")
['thinking', 'thinking_face']
>>> discord_emoji.name_to_image("thinking")
'https://raw.githubusercontent.com/twitter/twemoji/master/assets/72x72/1f914.png'
>>> discord_emoji.unicode_to_image("🤔")
'https://raw.githubusercontent.com/twitter/twemoji/master/assets/72x72/1f914.png'
```

## Licence

Please see [LICENSE](https://github.com/sevenc-nanashi/discord-emoji/blob/main/LICENSE).
