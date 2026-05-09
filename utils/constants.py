import os
import logging
from typing import Optional

import discord
from dotenv import load_dotenv


load_dotenv()

logger = logging.getLogger("utils.constants")

# Load development guild ID from environment and expose a discord.Object for guild-scoped commands
DEV_GUILD_ID = os.getenv("DEV_GUILD_ID")
MY_GUILD: Optional[discord.Object]

if DEV_GUILD_ID:
    try:
        MY_GUILD = discord.Object(id=int(DEV_GUILD_ID))
        logger.info(f"Loaded DEV_GUILD_ID={DEV_GUILD_ID}")
    except Exception:
        logger.exception("Failed to create discord.Object for DEV_GUILD_ID; ignoring")
        MY_GUILD = None
else:
    MY_GUILD = None
