
import logging

from pyrogram import Client

from anony.core.bot import AnonyBot
from anony.core.userbot import Userbot
from anony.core.dir import dirr
from anony.core.mongo import Mongo
from anony.core.clients import AutoCall
from anony.misc import SUDOERS
from anony.platforms import YouTube

# LOGGER

logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s - %(levelname)s] - %(name)s - %(message)s",
)

logger = logging.getLogger("anony")

# DATABASE

db = Mongo()

# BOT CLIENT

app = AnonyBot()

# USERBOT

userbot = Userbot()

# GROUP CALL CLIENT

anon = AutoCall()

# YOUTUBE

youtube = YouTube()

# THUMB

thumb = dirr

# STOP FUNCTION

async def stop(ignore_cleanup_errors: bool = False):
    try:
        await app.stop()

    except Exception as e:
        if not ignore_cleanup_errors:
            logger.error(e)

    try:
        await userbot.stop()

    except Exception as e:
        if not ignore_cleanup_errors:
            logger.error(e)

    try:
        await anon.stop()

    except Exception as e:
        if not ignore_cleanup_errors:
            logger.error(e)