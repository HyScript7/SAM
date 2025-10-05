# Script's Advanced Moderation

A drag & drop solution for moderation in your custom bots.

Developed for The CodeVerse Hub by Aditya.

## Features

* Auto Mod
* Logging + Logging API
  * Allows you to hook into SAM's logging system and replace it with your own or forward your own log events to it.
* Mod Notes
* Punishments (ban, kick, timeout)
* Voice (mute, deafen, move)
* Warnings

## Installation

Move the `sam` module from `modules` into your cogs, extensions or modules directory (wherever you keep discord.py extensions).

Load the module using discord.py's `discord.ext.commands.Bot.load_extension`.

## License

Redistribution and use in source and binary forms, with or without modification, are permitted provided that the conditions listed in the LICENSE file are met.
