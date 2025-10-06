"""
######  ####### #     # ####### #     #  #####  ####### ######     #    ####### ### ####### #     #     #####   #####  ######  ### ######  #######
#     # #       ##   ## #     # ##    # #     #    #    #     #   # #      #     #  #     # ##    #    #     # #     # #     #  #  #     #    #
#     # #       # # # # #     # # #   # #          #    #     #  #   #     #     #  #     # # #   #    #       #       #     #  #  #     #    #
#     # #####   #  #  # #     # #  #  #  #####     #    ######  #     #    #     #  #     # #  #  #     #####  #       ######   #  ######     #
#     # #       #     # #     # #   # #       #    #    #   #   #######    #     #  #     # #   # #          # #       #   #    #  #          #
#     # #       #     # #     # #    ## #     #    #    #    #  #     #    #     #  #     # #    ##    #     # #     # #    #   #  #          #
######  ####### #     # ####### #     #  #####     #    #     # #     #    #    ### ####### #     #     #####   #####  #     # ### #          #

The only thing this file does is load the advanced moderation extension.
You should use your own bootstrap script to start your bot, this is purely for demonstration and testing purposes.
"""

import logging
import os

import discord
from discord.ext import commands
from dotenv import load_dotenv

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(name)s - %(message)s')
logger = logging.getLogger("bot")

load_dotenv()

token = os.environ.get("TOKEN", None)
if token is None:
    logger.error("No token has been provided. Quitting!")
    raise RuntimeError("No token provided, will not be able to login.")
prefix = os.environ.get("PREFIX", "!")


class DemoBot(commands.Bot):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.initial_extensions = kwargs.get("initial_extensions", [])

    async def setup_hook(self) -> None:
        for extension in self.initial_extensions:
            try:
                await bot.load_extension(extension)
            except Exception as e:
                print(f"Failed to load extension {extension}: {e}")
                print("Are you sure SAM is installed? Try running the script using `uv run --with dist/sam-x.x.x.tar.gz main.py` where x.x.x is the version.")


# ! Requires us to build and pip install sam or run using `uv run --with dist/sam-0.1.0.tar.gz main.py`
initial_extensions = [
    "sam",
]

bot = DemoBot(
    prefix, intents=discord.Intents.all(), initial_extensions=initial_extensions
)


@bot.event
async def on_ready():
    print(f"We have logged in as {bot.user}")
    await bot.change_presence(
        activity=discord.Activity(
            type=discord.ActivityType.watching, name=f"{bot.command_prefix}help"
        )
    )


bot.run(token, log_handler=None)
