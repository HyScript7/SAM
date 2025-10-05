import pathlib

import discord
from discord.ext import commands

from .public import logging_api  # noqa - Making sure this is initialized

from .internal.database import init_db
from .internal.logger_config import logger


async def setup(bot: commands.Bot):
    await init_db()
    logger.info(
        "SAM: Script's Advanced Moderation loaded!"
    )
    logger.info("Script's Advanced Moderation is licensed under the BSD 3-Clause License.")
    logger.info("You can find the full license text in the LICENSE file under {}".format(pathlib.Path(__file__).resolve().parent.joinpath("LICENSE")))
