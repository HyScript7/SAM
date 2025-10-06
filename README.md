# Script's Advanced Moderation

A drag & drop solution for moderation in your custom bots.

Originally developed by [@HyScript7](https://github.com/HyScript7) for The CodeVerse Hub discord server owned by [Aditya](https://github.com/youngcoder45/).

## Features

* Auto Mod
* Logging + Logging API
  * Allows you to hook into SAM's logging system and replace it with your own or forward your own log events to it.
* Mod Notes
* Punishments (ban, kick, timeout)
* Voice (mute, deafen, move)
* Warnings

## Installation

Build & install the package using uv, or download it from pip.

Load the module using discord.py's `discord.ext.commands.Bot.load_extension` with the package name as the only parameter.

## License

Redistribution and use in source and binary forms, with or without modification, are permitted provided that the conditions listed in the LICENSE file are met.
